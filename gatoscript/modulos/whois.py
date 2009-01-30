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
Modulo principal del GatoScript.

Este modulo se encarga de cargar e interconectar otras partes del GatoScript.
"""

__module_name__ = "GatoScript WhoIs"
__module_version__ = "1.0"
__module_description__ = "Modulo WhoIs para GatoScript"
__module_autor__ = "GatoLoko"

# Cargamos la libreria de funciones de X-Chat
import xchat
# Importamos la funcion para unir directorios de forma portable
from os.path import join
# Importamos el modulo de funciones auxiliares
import auxiliar

# Definimos algunas variables de entorno para poder trabajar comodamente
scriptdir = xchat.get_info("xchatdir")
gatodir = join(scriptdir, "gatoscript")
moddir = join(gatodir, "modulos")
gatoconf = join(scriptdir, "gatoscript.conf")
gatodb = join(gatodir, "gatoscript.db")

## Cargamos las librerias y funciones que necesitamos
#import xchat, re, datetime, xml.dom.minidom, commands
#from os import popen3, path, system
#from random import randint
#from ConfigParser import ConfigParser
#from urllib import urlopen




##############################################################################
## Definimos las funciones de informacion y ayuda sobre el manejo del script
##############################################################################
#def gato_cb(word, word_eol, userdata):
    #"""Muestra la ayuda del GatoScript
    #Argumentos:
    #word     -- array de palabras que envia xchat a cada hook
    #word_eol -- array de cadenas que envia xchat a cada hook
    #userdata -- variable opcional que se puede enviar a un hook (ignorado)
    #"""
    #info_param = len(word_eol)
    #if info_param > 2:
        #mensajes = [
        #"",
        #"Solo se puede usar un parametro cada vez",
        #""]
    #else:
        #if word[1] == "-g":
            #mensajes = [
            #"",
            #"Informacion:",
            #"    /gato:               Muestra esta informacion",
            #"    /ginfo:              Muestra en el canal activo la publicidad sobre el script",
            #""]
        #else:
            #mensajes = [
            #"",
            #"Parametro no soportado",
            #""]
    #return mensajes


#############################################################################
# Definimos la funcion para redireccion y formateo de respuestas al whois
#############################################################################
# Respuesta al whois: Informacion de usuario
def whois_cb(word, word_eol, userdata):
    """Redirecciona las respuestas al "whois" hacia la ventana activa, al tiempo que modifica el formato de salida.
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook
    word_eol -- array de cadenas que envia xchat a cada hook
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    whois_activo = auxiliar.lee_conf("comun", "whois")
    if (whois_activo == "1"):
        if (word[1] == "301"):
            # Respuesta al whois: AwayMessage
            print '\0033[No disponible   ]\003 ' + word_eol[4][1:]
        elif (word[1] == "311"):
            # Respuesta al whois: Usuario
            nick = word[3]
            host = word[4] + "@" + word[5]
            nombre = word_eol[7][1:]
            print '\0033[Nick            ]\003 ' + nick
            print '\0033[Direccion       ]\003 ' + host
            print '\0033[Nombre real     ]\003 ' + nombre
        elif (word[1] == "312"):
            # Respuesta al whois: Servidor
            print '\0033[Servidor        ]\003 ' + word_eol[4]
        elif (word[1] == "317"):
            # Respuesta al whois: IDLE
            horas = int(word[4])/3600
            minutos = (int(word[4])-horas*3600)/60
            segundos = int(word[4])-((horas*3600)+(minutos*60))
            tiempo = str(horas) + ' horas, ' + str(minutos) + ' minutos y ' + str(segundos)
            print '\0033[IDLE            ]\003 ' + tiempo + ' segundos'
        elif (word[1] == "318"):
            # Respuesta al whois: Fin del whois
            print '\0033Fin del WHOIS\003'
        elif (word[1] == "319"):
            # Respuesta al whois: Canales
            print '\0033[Canales         ]\003 ' + word_eol[4][1:]
        elif (word[1] == "320"):
            # Respuesta al whois: Especial
            espacios = 15 - len(word[3])
            cadena = " "
            for i in range(espacios):
                cadena = cadena + " "
            print '\0033[' + word[3] + cadena + ']\003 ' + word_eol[4][1:]
        elif (word[1] == "335"):
            # Respuesta al whois: Bot
            print '\0033' + word_eol[0] + '\003'
        elif (word[1] == "307"):
            # Respuesta al whois: RegNick
            espacios = 15 - len(word[3])
            cadena = " "
            #if (espacios > 1):
            for i in range(espacios):
                cadena = cadena + " "
            print '\0033[' + word[3] + cadena + '] \003' + word_eol[4][1:]
        elif (word[1] == "342"):
            # Respuesta al whois: Solo admite privados de usuarios registrados
            espacios = 15 - len(word[3])
            cadena = " "
            #if (espacios > 1):
            for i in range(espacios):
                cadena = cadena + " "
            print '\0033[' + word[3] + cadena + '] \003' + word_eol[4][1:]
        elif (word[1] == "378"):
            # Respuesta al whois: VHOST
            print '\0033[VHost           ]\003 ' + word_eol[6]
        elif (word[1] == "379"):
            # Respuesta al whois: whoismodes
            print '\0033[Modos           ]\003 ' + word_eol[4][1:]
        elif (word[1] == "401"):
            # Respuesta al whois: No such nick
            print '\0033El nick ' + word[3] + ' no existe o no esta conectado\003'
        else:
            # Raw no definido
            print '\0033El raw ' + word[1] + ' no esta definido'
        return xchat.EAT_ALL
    else:
        return xchat.EAT_NONE


#############################################################################
# Definimos la funcion para la descarga del programa
#############################################################################
def unload_cb(userdata):
    """Esta funcion debe desenlazar todas las funciones del GatoScript al descargarse el script
    Argumentos:
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    # Desconectamos los comandos
    # Whois
    xchat.unhook(raw301)
    xchat.unhook(raw307)
    xchat.unhook(raw310)
    xchat.unhook(raw311)
    xchat.unhook(raw312)
    xchat.unhook(raw313)
    xchat.unhook(raw316)
    xchat.unhook(raw317)
    xchat.unhook(raw318)
    xchat.unhook(raw319)
    xchat.unhook(raw320)
    xchat.unhook(raw335)
    xchat.unhook(raw342)
    xchat.unhook(raw378)
    xchat.unhook(raw379)
    xchat.unhook(raw401)
    # Descarga
    xchat.unhook(hookunload)


#############################################################################
# Conectamos los "lanzadores" de xchat con las funciones que hemos definido
# para ellos
#############################################################################
# Whois
raw301 = xchat.hook_server('301', whois_cb, userdata=None, priority=10) # Mensaje de AWAY
raw307 = xchat.hook_server('307', whois_cb, userdata=None, priority=10) # whoisregnick
raw310 = xchat.hook_server('310', whois_cb, userdata=None, priority=10) # whoishelpop
raw311 = xchat.hook_server('311', whois_cb, userdata=None, priority=10) # whoisuser
raw312 = xchat.hook_server('312', whois_cb, userdata=None, priority=10) # whoisserver
raw313 = xchat.hook_server('313', whois_cb, userdata=None, priority=10) # whoisoperator
raw316 = xchat.hook_server('316', whois_cb, userdata=None, priority=10) # whoischanop
raw317 = xchat.hook_server('317', whois_cb, userdata=None, priority=10) # whoisidle
raw318 = xchat.hook_server('318', whois_cb, userdata=None, priority=10) # endofwhois
raw319 = xchat.hook_server('319', whois_cb, userdata=None, priority=10) # whoischannels
raw320 = xchat.hook_server('320', whois_cb, userdata=None, priority=10) # whoisspecial
raw335 = xchat.hook_server('335', whois_cb, userdata=None, priority=10) # whoisbot
raw342 = xchat.hook_server('342', whois_cb, userdata=None, priority=10) # Solo admite privados de usuarios registrados
raw378 = xchat.hook_server('378', whois_cb, userdata=None, priority=10) # whoishost (ip virtual)
raw379 = xchat.hook_server('379', whois_cb, userdata=None, priority=10) # whoismodes
raw401 = xchat.hook_server('401', whois_cb, userdata=None, priority=10) # No such nick

# Descarga del script
hookunload = xchat.hook_unload(unload_cb)
