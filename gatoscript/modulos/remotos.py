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

__module_name__ = "GatoScript"
__module_version__ = "0.80alpha1"
__module_description__ = "GatoScript para XChat"
__module_autor__ = "GatoLoko"

# Cargamos la libreria de funciones de X-Chat
import xchat
# Importamos la funcion para unir directorios de forma portable
from os.path import join
# Importamos la funcion que nos permite definir nuestro directorio de modulos
import sys

# Definimos algunas variables de entorno para poder trabajar comodamente
scriptdir = xchat.get_info("xchatdir")
gatodir = join(scriptdir, "gatoscript")
moddir = join(gatodir, "modulos")
gatoconf = join(scriptdir, "gatoscript.conf")
gatodb = join(gatodir, "gatoscript.db")

# Incluimos el directorio de modulos en el path
sys.path.append(moddir)

# Importamos el modulo de funciones auxiliares
import auxiliar

## Cargamos las librerias y funciones que necesitamos
#import xchat, re, datetime, xml.dom.minidom, commands
#from os import popen3, path, system
#from random import randint
#from ConfigParser import ConfigParser
#from urllib import urlopen


##############################################################################
## Definimos algunas variables que describen el entorno de trabajo y librerias
## opcionales.
##############################################################################

#scriptdir = xchat.get_info("xchatdir")
#gatodir = scriptdir + "/gatoscript/"
#filtros_path = gatodir + "antispam.conf"
#consejos_path = gatodir + "consejos.txt"
#configfile = gatodir + "gatoscript.conf"
#rssfile = gatodir + "rss.conf"
##home = xchat.get_info("xchatdir")[0:len(xchat.get_info("xchatdir"))-7]
#home = path.expanduser("~")
#amulesig = home + "/.aMule/amulesig.dat"
#azureusstats = home + "/.azureus/Azureus_Stats.xml"
#cp = ConfigParser()
#num_abusos_mayus = []
#num_abusos_colores = []
#NoXmms = 0
#NoDBus = 0
#global DBusIniciado
#DBusIniciado = 0
#global rbplayerobj
#global rbplayer
#global rbshellobj
#global rbshell


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
    #elif info_param < 2:
        #mensajes = [
        #"",
        #"Añada uno de los siguientes parametros en funcion del tipo de ayuda que quiera",
        #"    -g         Comandos para informacion del GatoScript",
        #"    -a         Comandos para Antispam",
        #"    -m         Comandos para informacion de reproductores Multimedia",
        #"    -s         Comandos para informacion del Sistema",
        #"    -c         Comandos para uso de los Consejos del Gato",
        #"    -d         Comandos para informacion de Descargas",
        #"    -u         Comandos para control de Usuarios",
        #"    -o         Comandos para establecer las Opciones",
        #"    -r         Comandos para gestion RSS",
        #"",
        #"Por ejemplo: /gato -s",
        #""]
    #else:
        #elif word[1] == "-c":
            #mensajes = [
            #"",
            #"Consejos:",
            #"    /consejos:           Muestra un consejo aleatorio",
            #"    /consejo <opcion>:   Muestra el consejo que concuerde con la opcion especificada",
            #"        Las opciones disponibles son: preguntar, ayudar, noayudar, planteamiento, manual, manual2, manual3, manual4 y buscador",
            #""]
        #else:
            #mensajes = [
            #"",
            #"Parametro no soportado",
            #""]
    #priv_imprime(mensajes)
    #return xchat.EAT_ALL


##############################################################################
## Definimos las funcion de controles remotos
##############################################################################
#def remoto_cb(word, word_eol, userdata):
    #"""Esta funcion revisa los mensajes recibidos en busca de comandos remotos
    #y cuando los encuentra, actua en consecuencia.
    #Argumentos:
    #word     -- array de palabras que envia xchat a cada hook
    #word_eol -- array de cadenas que envia xchat a cada hook
    #userdata -- variable opcional que se puede enviar a un hook (ignorado)
    #"""
    #remotos_activo = lee_conf("comun", "remotos")
    #if (remotos_activo == "1"):
        ##Definimos la expresion regular que actuara como activador
        #consejo_rem = re.compile("!consejo", re.IGNORECASE)
        #hola_rem = re.compile("!hola", re.IGNORECASE)
        #version_rem = re.compile("!version", re.IGNORECASE)
        ##Si se ha encontrado actuamos
        #if consejo_rem.search(word[1]):
            #consejo_aleatorio_cb("0", "0", "0")
        #elif hola_rem.search(word[1]):
            #xchat.command("say Hola %s!!" %word[0])
        #elif version_rem.search(word[1]):
            #software_cb("", "", "")
            #xchat.command("say (GatoScript) %s" % __module_version__)


##############################################################################
## Definimos la funcion para la descarga del programa
##############################################################################
#def unload_cb(userdata):
    #"""Esta funcion debe desenlazar todas las funciones del GatoScript al descargarse el script
    #Argumentos:
    #userdata -- variable opcional que se puede enviar a un hook (ignorado)
    #"""
    ## Desconectamos los comandos
    ## Controles remotos
    #xchat.unhook(hookremoto)
    ## Descarga
    #xchat.unhook(hookunload)


##############################################################################
## Conectamos los "lanzadores" de xchat con las funciones que hemos definido
## para ellos
##############################################################################

## Controles remotos
#hookremoto = xchat.hook_print('Channel Message', remoto_cb)
## Descarga del script
#hookunload = xchat.hook_unload(unload_cb)
