#!/usr/bin/python
# -*- coding: UTF8 -*-

# CopyRight (C) 2006-2009 GatoLoko
#
# This file is part of GatoScript
#
# GatoScript is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# GatoScript is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GatoScript; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

"""
Modulo Protecciones del GatoScript.

Este modulo contiene las funciones de proteccion para el GatoScript.
"""

__module_name__ = "GatoScript Protecciones"
__module_version__ = "1.0"
__module_description__ = "Modulo Protecciones para el GatoScript"
__module_autor__ = "GatoLoko"

# Cargamos la libreria de funciones de X-Chat
import xchat
# Importamos las librerias externas
from os.path import join
import sys
import sqlite3
import re
# Importamos la libreria de funciones auxiliares
import auxiliar

##############################################################################
# Definimos algunas variables que describen el entorno de trabajo y librerias
# opcionales
##############################################################################
_SCRIPTDIR = xchat.get_info("xchatdir")
_GATODIR = join(_SCRIPTDIR, "gatoscript")
_GATODB_PATH = join(_SCRIPTDIR, "gatoscript.conf")
_GATODB = join(_GATODIR, "gatoscript.db")

# Incluimos el directorio de modulos en el path
#sys.path.append(moddir)

# Importamos el modulo de funciones auxiliares
import auxiliar
# Importamos el modulo antispam
import antispam

num_abusos_mayus = []
num_abusos_colores = []

##############################################################################
# Definimos las funciones de uso interno del modulo
##############################################################################

##############################################################################
# Definimos las funciones de proteccion
##############################################################################
def anti_ctcp_cb(word, word_eol, userdata):
    """Detecta el envio de CTCPs a canales protegidos y expulsa al autor.
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    if auxiliar.lee_conf("protecciones", "ctcps") == "1":
        for canal in auxiliar.lee_conf( "protecciones", "canales" ).split( ',' ):
            if canal.lower() == word[2].lower():
                ctcp = re.compile("\.*\", re.IGNORECASE)
                canales = auxiliar.lee_conf("protecciones", "canales").split(',')
                if ctcp.search(word[3]):
                    for canal in canales:
                        canal_re = re.compile(canal[1:], re.IGNORECASE)
                        if canal_re.search(word[2]):
                            gprint("Se ha recibido un CTCP al canal " + word[2])
                            partes = word[0][1:].split("@")
                            comando = "ban *!*@" + partes[len(partes)-1]
                            xchat.command(comando)
                            partes = word[0][1:].split("!")
                            comando = "kick " + partes[0] + " Putos scriptkidies...."
                            xchat.command(comando)
    return xchat.EAT_NONE
    
def anti_notice_cb(word, word_eol, userdata):
    """Detecta el envio de NOTICEs a canales protegidos y expulsa al autor.
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    """
    #>> :Anti_Bots!GatoBot@BvW8Qj.CtqRtH.virtual NOTICE #gatoscript :hola
    canales = auxiliar.lee_conf("protecciones", "canales").split(',')
    for canal in canales:
        if word[2].lower() == canal.lower():
            partes = word[0][1:].split("!")
            comando = "kickban " + partes[0] + " Putos scriptkidies...."
            xchat.command(comando)
    return xchat.EAT_NONE

def anti_hoygan_cb(word, word_eol, userdata):
    """Detecta la palabra "hoygan" en los canales y banea al autor
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    if auxiliar.lee_conf("protecciones", "hoygan") == "1":
        for canal in auxiliar.lee_conf( "protecciones", "canales" ).split( ',' ):
            if canal.lower() == word[2].lower():
                hoyga = re.compile('hoyga|h 0 y g 4 n', re.IGNORECASE)
                if hoyga.search(word_eol[3]):
                    partes = word[0][1:].split("@")
                    xchat.command("ban *!*@" + partes[len(partes)-1])
                    partes = word[0][1:].split("!")
                    xchat.command("kick " + partes[0] + " Los hoygan son la version electronica del payaso de la clase y no son graciosos")
    return xchat.EAT_NONE

def anti_mayusculas_cb(word, word_eol, userdata):
    """Detecta el abuso de mayusculas en los canales y banea al autor
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook
    word_eol -- array de cadenas que envia xchat a cada hook
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    if auxiliar.lee_conf("protecciones", "mayusculas") == "1":
        for canal in auxiliar.lee_conf( "protecciones", "canales" ).split( ',' ):
            if canal.lower() == word[2].lower():
                mensaje = ""
                cadena = word_eol[3][1:]
                accion = re.compile('^\ACTION')
                if accion.match(cadena):
                    cadena = cadena[7:]
                letrasre = re.compile('[a-zA-Z]')
                letras = letrasre.findall(cadena)
                abuso = True
                for letra in letras:
                    if letra.islower() == True:
                        abuso = False
                if (len(letras)) > 10 and abuso == True:
                    host = word[0][1:].split("@")[1]
                    if host in num_abusos_mayus:
                        num_abusos_mayus.remove(host)
                        mensaje = " Escribir todo en mayusculas va contra las normas y estabas avisado."
                        auxiliar.expulsa(mensaje, "1", word)
                    else:
                        num_abusos_mayus.append(host)
                        xchat.command("msg " + word[2] + " " + word[0][1:].split("!")[0] + ": no escribas todo en mayusculas, va contra las normas. La proxima vez seras expulsado.")
    return xchat.EAT_NONE

def anti_colores_cb(word, word_eol, userdata):
    """Detecta el envio de mensajes con colores o realzados en los canales
    protegidos, avisa al autor en la primera ocasion y lo expulsa si reincide
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook
    word_eol -- array de cadenas que envia xchat a cada hook
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    if auxiliar.lee_conf("protecciones", "colores") == "1":
        for canal in auxiliar.lee_conf( "protecciones", "canales" ).split( ',' ):
            if canal.lower() == word[2].lower():
                mensaje = ""
                cadena = word_eol[3][1:]
                accion = re.compile('^\ACTION')
                if accion.match(cadena):
                    cadena = cadena[7:]
                colores = re.compile('\\x02|\\x16|\\x1f|\\x03(([0-9]{1,2})?(,[0-9]{1,2})?)?')
                if colores.search(cadena):
                    host = word[0][1:].split("@")[1]
                    if host in num_abusos_colores:
                        num_abusos_colores.remove(host)
                        mensaje = " El uso de colores va contra las normas y estabas avisado."
                        auxiliar.expulsa(mensaje, "1", word)
                    else:
                        num_abusos_colores.append(host)
                        xchat.command("msg " + word[2] + " " + word[0][1:].split("!")[0] + ": no uses colores/negrillas/subrallado en este canal, va contra las normas. La proxima vez seras expulsado. Para desactivarlos escribe: /remote off")
    return xchat.EAT_NONE

def proteccion_cb(word, word_eol, userdata):
    """Detecta el envio de SPAM a canales y expulsa al autor
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    if auxiliar.lee_conf("protecciones", "spam") == "1":
        chanspam = auxiliar.lee_conf("protecciones", "chanspam").split(",")
        for i in range(len(chanspam)):
            if word_eol[3].find(chanspam[i]) > 0:
                ban = "1"
                mensaje = " Spam"
                auxiliar.expulsa(mensaje, ban, word)
    return xchat.EAT_NONE

# Anti ClonerX  (on JOIN)
def anti_clonerx_cb(word, word_eol, userdata):
    """Detecta nicks que entran al canal con un indent que concuerde con los de ClonerX y los banea para evitar el flood
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    bots = re.compile("^[a-z]{1}(\d){2,4}$")
    ident = word[0][1:].split("!")[1].split("@")[0]
    if bots.search(ident):
        canal = word[2][1:]
        contexto = xchat.find_context(channel=canal)
        host = word[0].split("@")[1]
        comando = "ban *!*@" + host
        contexto.command(comando)
        mensaje = "Ident de ClonerX en " + canal
        gprint(mensaje)
    return xchat.EAT_NONE

def anti_drone_cb(word, word_eol, userdata):
    #print word_eol[0]
    return xchat.EAT_NONE
    
def anti_away_cb(word, word_eol, userdata):
    """Detecta mensajes de ausencia en el canal y expulsa al usuario
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se envia a un hook (ignorado)
    """
    if auxiliar.lee_conf("protecciones", "away") == "1":
        awaystr = auxiliar.lee_conf("protecciones", "awaystr").split(",")
        for i in range(len(awaystr)):
            if word_eol[3].find(awaystr[i]) > 0:
                ban = "1"
                mensaje = " Quita los mensajes de away automaticos, si no estas callate"
                auxiliar.expulsa(mensaje, ban, word)
    return xchat.EAT_NONE


##############################################################################
# Definimos la funcion de informacion y ayuda sobre el manejo del modulo
##############################################################################
def ayuda():
    """Muestra la ayuda de las funciones  de proteccion para GatoScript"""
    mensajes = [
    "",
    "Protecciones:",
    "    Este modulo no ofrece comandos interactivos",
    ""]
    auxiliar.priv_imprime(mensajes)
    return xchat.EAT_ALL


##############################################################################
## Definimos la funcion para la descarga del programa
##############################################################################
def unload_cb(userdata):
    """Esta funcion debe desconectar todas las funciones del modulo al
    descargarse el script
    Argumentos:
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    # Desconectamos las funciones de proteccion
    xchat.unhook(HOOKPROTECCION)
    xchat.unhook(HOOKANTINOTICE)
    xchat.unhook(HOOKANTICLONERX)
    xchat.unhook(HOOKANTIDRONE)
    xchat.unhook(HOOKANTICTCP)
    xchat.unhook(HOOKANTIHOYGAN)
    xchat.unhook(HOOKANTIMAYUSCULAS)
    xchat.unhook(HOOKANTICOLORES)
    xchat.unhook(HOOKANTIAWAY)
    # Descargamos el
    xchat.unhook(HOOKUNLOAD)


##############################################################################
# Conectamos los "lanzadores" de xchat con las funciones que hemos definido
# para ellos
##############################################################################

# Protecciones
HOOKPROTECCION = xchat.hook_server('PRIVMSG', proteccion_cb, userdata=None, priority=10)
HOOKANTINOTICE = xchat.hook_server('NOTICE', anti_notice_cb, userdata=None)
HOOKANTICLONERX = xchat.hook_server('JOIN', anti_clonerx_cb, userdata=None)
HOOKANTIDRONE = xchat.hook_server('JOIN', anti_drone_cb, userdata=None)
HOOKANTICTCP = xchat.hook_server('PRIVMSG', anti_ctcp_cb, userdata=None)
HOOKANTIHOYGAN = xchat.hook_server('PRIVMSG', anti_hoygan_cb, userdata=None)
HOOKANTIMAYUSCULAS = xchat.hook_server('PRIVMSG', anti_mayusculas_cb, userdata=None)
HOOKANTICOLORES = xchat.hook_server('PRIVMSG', anti_colores_cb, userdata=None)
HOOKANTIAWAY = xchat.hook_server('PRIVMSG', anti_away_cb, userdata=None)
# Descargamos el modulo
HOOKUNLOAD = xchat.hook_unload(unload_cb)
