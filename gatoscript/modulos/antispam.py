
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
Modulo AntiSpam del GatoScript.

Este modulo contiene las funciones AntiSpam para el GatoScript.
"""

__module_name__ = "GatoScript AntiSpam"
__module_version__ = "1.0"
__module_description__ = "Modulo AntiSpam para el GatoScript"
__module_autor__ = "GatoLoko"

# Cargamos las librerias y funciones que necesitamos
import xchat
import re
from os import path
import sqlite3
import auxiliar

#############################################################################
# Definimos algunas variables que describen el entorno de trabajo y librerias
# opcionales.
#############################################################################

_SCRIPTDIR = xchat.get_info("xchatdir")
_GATODIR = _SCRIPTDIR + "/gatoscript/"
_GATODB_PATH = _GATODIR + "gatoscript.db"
_FILTROS_PATH = _GATODIR + "antispam.conf"
_HOME = path.expanduser("~")

#############################################################################
# Inicializamos el modulo
#############################################################################
# Conectamos a la base de datos
if path.exists(_GATODB_PATH):
    CONEXIONDB = sqlite3.connect(_GATODB_PATH)
    CURSOR = CONEXIONDB.cursor()
    _CONECTADO = 1
else:
    _CONECTADO = 0
# Cargamos la lista de filtros para el antispam
if _CONECTADO == 1:
    ANTISPAM = 1
    if auxiliar.lee_conf("protecciones", "spambots") == "1":
        SPAMBOTS = 1
else:
    print("No se puede cargar la lista de filtros, AntiSpam desactivado")
    ANTISPAM = 0
    SPAMBOTS = 0


#############################################################################
# Definimos las funciones de uso interno en el modulo
#############################################################################
def antispam_reload():
    """Recarga la lista de filtros antispam para aplicar los cambios o
    retomar una lista anterior
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook (ignorado)
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    # Utilizamos las variables globales porque esto modifica el
    # funcionamiento del modulo completo
    global ANTISPAM
    global SPAMBOTS
    if _CONECTADO == 1:
        ANTISPAM = 1
        if auxiliar.lee_conf("protecciones", "spambots") == "1":
            SPAMBOTS = 1
    else:
        auxiliar.gprint("No se pueden cargar los filtros, AntiSpam desactivado")
        ANTISPAM = 0
        SPAMBOTS = 0


#############################################################################
# Definimos la funcion antispam para filtrado de mensajes privados.
# El sistema antispam eliminara todas las lineas que contengan alguna de las
# cadenas definidas en el archivo antispam.conf
#############################################################################
def antispam_cb(word, word_eol, userdata):
    """Compara las lineas que se reciben con una lista de filtros y elimina
    aquellas que coincidan. Ademas, de forma opcional, expulsa a los spambots.
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook (ignorado)
    word_eol -- array de cadenas que envia xchat a cada hook
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    filtros = CURSOR.execute("SELECT filtro FROM filtros")
    if auxiliar.lee_conf("protecciones", "spam") == "1":
        #chanspam = auxiliar.lee_conf("protecciones", "chanspam").split(",")
        #for i in range(len(chanspam)):
            #if word_eol[3].find(chanspam[i]) > 0:
        for filtro in filtros:
            spam_exp = re.compile(".*" + filtro[0] + ".*", re.IGNORECASE)
            if (spam_exp.search(word_eol[3][1:])):
                ban = "1"
                mensaje = " Spam"
                auxiliar.expulsa(mensaje, ban, word)
    # Si esta activada la gestion de bots spammers...
    if SPAMBOTS == 1:
        # Comprobamos si el mensaje se ha recibido en un privado o en alguno
        # de nuestros canales protegidos
        if (word[2] in CURSOR.execute("SELECT canales FROM canales")) or \
                (word[2] == xchat.get_info("nick")):
            # Si es asi, comprobamos si el mensaje contiene spam
            for filtro in filtros:
                spam_exp = re.compile(".*" + filtro[0] + ".*", re.IGNORECASE)
                if (spam_exp.search(word_eol[3][1:])):
                    # Si contiene spam, expulsamos al bot responsable
                    auxiliar.expulsa(" Bot spammer", "1", word)
                    # Y quitamos su nick de la lista de niños buenos
                    nick = word[0].split("!")[0].split(":")[1]
                    if nick in CURSOR.execute("SELECT goodboy FROM goodboys"):
                        CURSOR.execute("DELETE FROM goodboys WHERE goodboy \
                            IN (?)", (nick,))
                        CONEXIONDB.commit()
    # Comprobamos si esta activada la funcion anti spam
    if (ANTISPAM == 1):
        # Si esta activada, comprobamos si el texto recibido contiene spam y
        # si es asi, ignoramos la linea      
        for filtro in filtros: 
            spam_exp = re.compile(".*" + filtro[0] + ".*", re.IGNORECASE)
            if (spam_exp.search(word_eol[3][1:])):
                return xchat.EAT_ALL


def antispam_add_cb(word, word_eol, userdata):
    """Añade un nuevo filtro al final de la lista para usarse con el sistema
    antispam. Esta funcion no comprueba si el nuevo filtro ya existe,
    simplemente lo añade al final.
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    if _CONECTADO == 1:
        CURSOR.execute("INSERT INTO filtros VALUES (null, ?)", (word[1],))
        CONEXIONDB.commit()
        mensaje = "Se ha añadido '" + word[1] + "' a la lista de filtros"
        auxiliar.priv_linea(mensaje)
        del mensaje
        antispam_reload()
    else:
        auxiliar.gprint("Active el sistema AntiSpam antes de quitar filtros")
    return xchat.EAT_ALL


def antispam_del_cb(word, word_eol, userdata):
    """Elimina un filtro de la lista que se usa con el sistema antispam.
    Esta funcion no verifica si hay duplicados, elimina todas las ocurrencias
    del filtro.
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook (ignorado)
    word_eol -- array de cadenas que envia xchat a cada hook
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    if _CONECTADO == 1:
        CURSOR.execute("DELETE FROM filtros WHERE filtro IN (?)", \
                (word_eol[1],))
        CONEXIONDB.commit()        
        mensaje = "Se ha eliminado '%s' de la lista de filtros" % word_eol[1]
        auxiliar.priv_linea(mensaje)
        del mensaje
        antispam_reload()
    else:
        auxiliar.gprint("Active el sistema AntiSpam antes de añadir filtros")
    return xchat.EAT_ALL


def antispam_list_cb(word, word_eol, userdata):
    """Muestra, en la pestaña "GatoScript", todas las lineas de la lista de
    filtros antispam.
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook (ignorado)
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    for filtro in CURSOR.execute("SELECT * FROM filtros"):
        mensaje = "Filtro %s: %s" % (filtro.id, filtro.filtro)
        auxiliar.priv_linea(mensaje)
    #global filtros
    #cuenta_lineas = 1
    #auxiliar.priv_linea("\nLista de filtros:")
    #for filtro in filtros[0:len(filtros)-1]:
    #    mensaje = "Filtro %s: %s" % (cuenta_lineas, filtro)
    #    auxiliar.priv_linea(mensaje)
    #    cuenta_lineas = cuenta_lineas + 1
    #auxiliar.priv_linea("")
    del mensaje
    #del cuenta_lineas
    return xchat.EAT_ALL


def testspam_cb(word, word_eol, userdata):
    """Envia un mensaje a todos los usuarios del canal que no esten en la
    lista de niños buenos para ver si responden con spam.
    """
    userlist = xchat.get_list("users")
    goodboys = []
    for row in CURSOR.execute("SELECT goodboy FROM goodboys"):
        goodboys.append(row[0])
    for usuario in userlist:
        if usuario.nick not in goodboys:
            #print usuario.nick
            contexto = xchat.find_context(channel=usuario.nick)
            if contexto == None:
                xchat.command("query -nofocus %s" %usuario.nick)
                contexto = xchat.find_context(channel=usuario.nick)
            contexto.command("say %s" %auxiliar.lee_conf("protecciones", \
                    "botmensaje"))
            CURSOR.execute("INSERT INTO goodboys VALUES (null, ?)", \
                    (usuario.nick,))
    CONEXIONDB.commit()
    return xchat.EAT_NONE


#############################################################################
# Definimos la funcion de informacion y ayuda sobre el manejo del modulo 
#############################################################################
def ayuda():
    """Muestra la ayuda de las funciones antispam para GatoScript"""
    mensajes = [
    "",
    "Antispam:",
    "    /antiadd <cadena>: Añade una cadena al filtro AntiSpam",
    "    /antidel <cadena>: Elimina una cadena del filtro AntiSpam",
    "    /antilist:     Muestra la lista de filtros",
    ""]
    return mensajes


#############################################################################
# Definimos la funcion para la descarga del programa
#############################################################################
def unload_cb(userdata):
    """Esta funcion debe desconectar todas las funciones del modulo al
    descargarse el script
    Argumentos:
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    # Guardamos los cambios en la base de datos
    CONEXIONDB.commit()
    # Desconectamos las funciones AntiSpam
    xchat.unhook(HOOKANTISPAM)
    xchat.unhook(HOOKANTIADD)
    xchat.unhook(HOOKANTILIST)
    xchat.unhook(HOOKANTIDEL)
    xchat.unhook(HOOKTEST)
    # Descargamos el 
    xchat.unhook(HOOKUNLOAD)


#############################################################################
# Conectamos los "lanzadores" de xchat con las funciones que hemos definido
# para ellos
#############################################################################

# Antispam
HOOKANTISPAM = xchat.hook_server('PRIVMSG', antispam_cb, userdata=None)
HOOKANTIADD = xchat.hook_command('antiadd', antispam_add_cb)
HOOKANTILIST = xchat.hook_command('antilist', antispam_list_cb)
HOOKANTIDEL = xchat.hook_command('antidel', antispam_del_cb)
HOOKTEST = xchat.hook_command('test2', testspam_cb)
# Descarga del modulo
HOOKUNLOAD = xchat.hook_unload(unload_cb)
