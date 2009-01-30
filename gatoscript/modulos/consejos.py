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
# Importamos el modulo antispam
import antispam



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
        #"    -c         Comandos para uso de los Consejos del Gato",
        #"",
        #"Por ejemplo: /gato -s",
        #""]
    #else:
        #if word[1] == "-g":
            #mensajes = [
            #"",
            #"Informacion:",
            #"    /gato:               Muestra esta informacion",
            #"    /ginfo:              Muestra en el canal activo la publicidad sobre el script",
            #""]
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
## Definimos las funciones para el modulo "Consejos del Gato"
##############################################################################
#def consejo_aleatorio_cb(word, word_eol, userdata):
    #"""Muestra en el canal activo una linea aleatoria del archivo de consejos.
    #Argumentos:
    #word     -- array de palabras que envia xchat a cada hook (ignorado)
    #word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    #userdata -- variable opcional que se puede enviar a un hook (ignorado)
    #"""
    #if path.exists(consejos_path):
        #archivo = file(consejos_path, "r")
        #consejos = archivo.readlines()
        #archivo.close()
        #lin = len(consejos)
        #aleatorio = randint(0, lin -1)
        #consejo = consejos[aleatorio]
        #xchat.command("say %s" %consejo[0:len(consejo)-1])
    #else:
        #gprint("Falta el archivo de consejos")
    #return xchat.EAT_ALL

#def consejo_cb(word, word_eol, userdata):
    #""" Muestra consejos en funcion de un parametro o, a falta de este,
    #aleatoriamente.
    #Argumentos:
    #word     -- array de palabras que envia xchat a cada hook
    #word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    #userdata -- variable opcional que se puede enviar a un hook (ignorado)
    #"""
    #if len(word_eol) > 1:
        #if word[1] == "preguntar":
            #linea = 0
        #elif word[1] == "ayudar":
            #linea = 1
        #elif word[1] == "noayudar":
            #linea = 2
        #elif word[1] == "planteamiento":
            #linea = 3
        #elif word[1] == "manual":
            #linea = 4
        #elif word[1] == "manual2":
            #linea = 5
        #elif word[1] == "manual3":
            #linea = 6
        #elif word[1] == "manual4":
            #linea = 7
        #elif word[1] == "buscador":
            #linea = 8
        #else:
            #linea = "no"
        #if path.exists(consejos_path):
            #archivo = file(consejos_path, "r")
            #consejos = archivo.readlines()
            #archivo.close()
            #if linea == "no":
                #gprint("No hay ningun consejo que concuerde")
            #else:
                #consejo = (consejos[linea])[0:len(consejos[linea])-1]
                #xchat.command("say %s" %consejo)
        #else:
            #gprint("Falta el archivo de consejos")
    #else:
        #gprint("No ha especificado un consejo")
    #return xchat.EAT_ALL

#def preguntar_cb(word, word_eol, userdata):
    #xchat.command("say Consejos del Gato Nº1: No preguntes si puedes preguntar, plantea tu duda y si alguien sabe la solucion y tiene ganas te la dira")
    #return xchat.EAT_ALL

#def ayudar_cb(word, word_eol, userdata):
    #xchat.command("say Consejos del Gato Nº1.1: No preguntes si alguien te puede ayudar, plantea tu problema y si alguien sabe y tiene ganas te ayudara")
    #return xchat.EAT_ALL

#def noayudar_cb(word, word_eol, userdata):
    #xchat.command("say Consejos del Gato Nº2: Si preguntas y nadie te contesta no te pongas a repetir, o nadie sabe la respuesta o nadie tiene ganas de responder. Repitiendo solo molestas.")
    #return xchat.EAT_ALL

#def planteamiento_cb(word, word_eol, userdata):
    #xchat.command("say Consejos del Gato Nº3: Cuando planteas un problema o una duda, procura hacerte entender lo mas claramente posible, incluyendo toda la informacion que puedas y expresandote bien (nada de 'q' o 'k' en vez de 'que' y mierdas asi). Procura indicar los mensajes de error EXACTOS, no lo que crees que significan.")
    #return xchat.EAT_ALL

#def privado_cb(word, word_eol, userdata):
    #xchat.command("say No atiendo privados a menos que seas una tia buenorra o rica dispuesta a casarte conmigo")
    #return xchat.EAT_ALL

#def web_cb(word, word_eol, userdata):
    #xchat.command("say http://www.gatoloko.org")
    #return xchat.EAT_ALL

#def repos_cb(word, word_eol, userdata):
    #xchat.command("say deb http://www.gatoloko.org/repositorio/ VERSION RAMAS")
    #xchat.command("say donde VERSION puede ser 'dapper', 'edgy' o 'feisty'")
    #xchat.command("say donde RAMAS puede ser una o mas de: 'estable', 'inestable'")
    #return xchat.EAT_ALL

#def autent_cb(word, word_eol, userdata):
    #xchat.command("say gpg --keyserver subkeys.pgp.net --recv-keys B3B042E7")
    #xchat.command("say gpg --armor --export B3B042E7 | sudo apt-key add -")
    #xchat.command("say sudo apt-get update")
    #return xchat.EAT_ALL


##############################################################################
## Definimos la funcion para la descarga del programa
##############################################################################
#def unload_cb(userdata):
    #"""Esta funcion debe desenlazar todas las funciones del GatoScript al descargarse el script
    #Argumentos:
    #userdata -- variable opcional que se puede enviar a un hook (ignorado)
    #"""
    ## Desconectamos los comandos
    ## Consejos
    #xchat.unhook(hookconsejos)
    #xchat.unhook(hookconsejo)
    #xchat.unhook(hookpreguntar)
    #xchat.unhook(hookayudar)
    #xchat.unhook(hooknoayudar)
    #xchat.unhook(hookplanteamiento)
    #xchat.unhook(hookprivado)
    #xchat.unhook(hookweb)
    #xchat.unhook(hookrepos)
    #xchat.unhook(hookautent)


##############################################################################
## Conectamos los "lanzadores" de xchat con las funciones que hemos definido
## para ellos
##############################################################################

## Consejos
#hookconsejos = xchat.hook_command('consejos', consejo_aleatorio_cb)
#hookconsejo = xchat.hook_command('consejo', consejo_cb)
#hookpreguntar = xchat.hook_command('preguntar', preguntar_cb)
#hookayudar = xchat.hook_command('ayudar', ayudar_cb)
#hooknoayudar = xchat.hook_command('noayudar', noayudar_cb)
#hookplanteamiento = xchat.hook_command('planteamiento', planteamiento_cb)
#hookprivado = xchat.hook_command('privado', privado_cb)
#hookweb = xchat.hook_command('web', web_cb)
#hookrepos = xchat.hook_command('repos', repos_cb)
#hookautent = xchat.hook_command('autent', autent_cb)
