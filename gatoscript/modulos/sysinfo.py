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
        #"    -s         Comandos para informacion del Sistema",
        #"",
        #"Por ejemplo: /gato -s",
        #""]
    #else:
        #if word[1] == "-s":
            #mensajes = [
            #"",
            #"Informacion del sistema:",
            #"    /gup:                Muestra el uptime del sistema",
            #"    /gos:                Muestra la distribucion y su version",
            #"    /gsoft:              Muestra en el canal la version de los programas mas importantes",
            #"    /gpc:                Muestra en el canal informacion sobre el hardware del pc",
            #"    /hora:               Muestra en el canal la hora del sistema",
            #""]
        #else:
            #mensajes = [
            #"",
            #"Parametro no soportado",
            #""]
    #priv_imprime(mensajes)
    #return xchat.EAT_ALL


##############################################################################
## Definimos las funciones para obtener la informacion del sistema
##############################################################################
#def uptime_cb(word, word_eol, userdata):
    #"""Muestra en el canal activo el uptime del pc.
    #Argumentos:
    #word     -- array de palabras que envia xchat a cada hook (ignorado)
    #word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    #userdata -- variable opcional que se puede enviar a un hook (ignorado)
    #"""
    #archivo_uptime = file("/proc/uptime", "r")
    #lineas_uptime = archivo_uptime.readline()
    #archivo_uptime.close()
    #uptime = eval((lineas_uptime.split())[0])
    #resto_dias = uptime % 86400
    #dias = int(uptime / 86400)
    #if dias < 1:
        #horas = int(uptime / 3600)
        #resto_horas = int(uptime % 3600)
        #minutos = int(resto_horas / 60)
        #xchat.command("say ( Uptime ) %s horas y %s minutos" %(horas, minutos))
    #else:
        #if dias > 1:
            #cadena_dias = "dias"
        #else:
            #cadena_dias = "dia"
        #horas = int(resto_dias / 3600)
        #resto_horas = int(resto_dias % 3600)
        #minutos = int(resto_horas / 60)
        #xchat.command("say ( Uptime ) %s %s, %s horas y %s minutos" %(dias, cadena_dias, horas, minutos))
    #return xchat.EAT_ALL

#def sistema_cb(word, word_eol, userdata):
    #"""Muestra en el canal activo informacion sobre el sistema operativo que usamos.
    #Argumentos:
    #word     -- array de palabras que envia xchat a cada hook (ignorado)
    #word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    #userdata -- variable opcional que se puede enviar a un hook (ignorado)
    #"""
    #if path.exists("/etc/lsb-release"):
        #LSB = file("/etc/lsb-release", "r")
        #lineas_LSB = LSB.readlines()
        #LSB.close()
        #distro = (lineas_LSB[0])[11:len(lineas_LSB[0])-1]
        #version = (lineas_LSB[1])[16:len(lineas_LSB[1])-1]
        #codigo = (lineas_LSB[2])[17:len(lineas_LSB[2])-1]
        #entrada, salida, error = popen3("uname -r", "r")
        #error2 = error.readlines()
        #if len(error2) > 0:
            #gprint(error2)
        #else:
            #kernel = salida.readlines()
            #kernel2 = (kernel[0])[0:len(kernel[0])-1]
        #xchat.command("say ( Distribucion ) %s   ( Version ) %s %s   ( Kernel ) %s" %(distro, version, codigo, kernel2))
    #else:
        #gprint("La distribucion no cumple con LSB")
    #return xchat.EAT_ALL

#def software_cb(word, word_eol, userdata):
    #"""Muestra en el canal activo informacion sobre las versiones del software basico.
    #Argumentos:
    #word     -- array de palabras que envia xchat a cada hook (ignorado)
    #word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    #userdata -- variable opcional que se puede enviar a un hook (ignorado)
    #"""
    #entrada, salida, error = popen3("uname -sr", "r")
    #error2 = error.readlines()
    #if len(error2) > 0:
        #for i in range(len(error2)):
            #gprint(error2[i])
        #sistema = "Indeterminable"
    #else:
        #uname = salida.readlines()
        #sistema = (uname[0])[0:len(uname[0])-1]
    #entrada, salida, error = popen3("/lib/libc.so.6", "r")
    #error2 = error.readlines()
    #if len(error2) > 0:
        #for i in range(len(error2)):
            #gprint(error2[i])
        #libc = "Indeterminable"
    #else:
        #libc_text = salida.readlines()
        #if libc_text[0].split()[0] == "GNU":
            #licencia = "GLIBC"
        #libc = licencia + " " + libc_text[0].split()[6][:-1]
    #entrada, salida, error = popen3("xdpyinfo | grep version:", "r")
    #error2 = error.readlines()
    #if len(error2) > 0:
        #for i in range(len(error2)):
            #gprint(error2[i])
        #X11 = "Indeterminable"
    #else:
        #xserver = salida.readlines()
        #servidor = xserver[0].split()
    #entrada, salida, error = popen3('xdpyinfo | grep "vendor string"', "r")
    #error2 = error.readlines()
    #if len(error2) > 0:
        #for i in range(len(error2)):
            #gprint(error2[i])
        #xversion = "Indeterminable"
    #else:
        #x_version = salida.readlines()
        #xversion = x_version[0].split()
        #X11 = xversion[3] + " " + servidor[len(servidor)-1]
    #entrada, salida, error = popen3("gcc --version", "r")
    #error2 = error.readlines()
    #if len(error2) > 0:
        #for i in range(len(error2)):
            #gprint(error2[i])
        #gcc = "Indeterminable"
    #else:
        #gcc_out = salida.readlines()
        #if gcc_out[0] == "bash: gcc: command not found":
            #gcc = "No instalado"
        #else:
            #gcc_partes = gcc_out[0].split()
            #gcc = gcc_partes[2]
    #xchat.command("say ( Sistema ) %s - ( LIBC ) %s - ( X11 ) %s - ( GCC ) %s" %(sistema, libc, X11, gcc))
    #del entrada, salida, error
    #return xchat.EAT_ALL

#def fecha_cb(word, word_eol, userdata):
    #"""Muestra, en la pestaña "GatoScript", todas las lineas de la lista de filtros antispam.
    #Argumentos:
    #word     -- array de palabras que envia xchat a cada hook (ignorado)
    #word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    #userdata -- variable opcional que se puede enviar a un hook (ignorado)
    #"""
    #entrada, salida, error = popen3("date")
    #error2 = error.readlines()
    #if len(error2) > 0:
        #for i in range(len(error2)):
            #gprint(error2[i])
    #else:
        #fecha = salida.readlines()
        #xchat.command("say %s" % (fecha[0][:-1]))
    #del entrada, salida, error
    #return xchat.EAT_ALL

#def pc_cb(word, word_eol, userdata):
    #"""Muestra en el canal activo, informacion sobre el pc.
    #Argumentos:
    #word     -- array de palabras que envia xchat a cada hook (ignorado)
    #word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    #userdata -- variable opcional que se puede enviar a un hook (ignorado)
    #"""
    ## CPU
    #archivo = file("/proc/cpuinfo")
    #cpuinfo = archivo.readlines()
    #archivo.close()
    #cpu = cpuinfo[4].split(":")[1][1:-1]
    #velocidad = cpuinfo[6].split(":")[1][1:-1]
    ## Memoria
    #archivo = file("/proc/meminfo")
    #meminfo = archivo.readlines()
    #archivo.close()
    #partes = meminfo[0].split(":")[1][:-1].split(" ")
    #memoria = partes[len(partes)-2]
    #unidad = partes[len(partes)-1]
    ## Free
    #partes = meminfo[1].split(":")[1][:-1].split(" ")
    #freemem = partes[len(partes)-2]
    ## Buffer
    #partes = meminfo[2].split(":")[1][:-1].split(" ")
    #bufmem = partes[len(partes)-2]
    ## Cache
    #partes = meminfo[3].split(":")[1][:-1].split(" ")
    #cachemem = partes[len(partes)-2]
    ## Usada y libre
    #usada = int(freemem) + int(bufmem) + int(cachemem)
    #libre = int(memoria) - usada
    ## Mensaje
    #mensaje = "[Informacion del PC] CPU: " + cpu + " - Velocidad: " + velocidad + "MHz - Memoria instalada: " + memoria + unidad + " - Memoria usada: " + str(libre) + unidad
    #xchat.command("say " + mensaje)
    #return xchat.EAT_ALL

#def red_cb(word, word_eol, userdata):
    #"""Muestra en el canal activo, informacion sobre la red.
    #Argumentos:
    #word     -- array de palabras que envia xchat a cada hook (ignorado)
    #word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    #userdata -- variable opcional que se puede enviar a un hook (ignorado)
    #"""
    #archivo = file("/etc/hostname")
    #hostname = archivo.read()
    #archivo.close()
    #gprint("( Hostname ) " + hostname)


##############################################################################
## Definimos la funcion para la descarga del programa
##############################################################################
#def unload_cb(userdata):
    #"""Esta funcion debe desenlazar todas las funciones del GatoScript al descargarse el script
    #Argumentos:
    #userdata -- variable opcional que se puede enviar a un hook (ignorado)
    #"""
    ## Desconectamos los comandos
    ## Informacion del sistema
    #xchat.unhook(hookgup)
    #xchat.unhook(hookgos)
    #xchat.unhook(hookgsoft)
    #xchat.unhook(hookfecha)
    #xchat.unhook(hookpc)
    #xchat.unhook(hooknet)
    ## Descarga
    #xchat.unhook(hookunload)


##############################################################################
## Conectamos los "lanzadores" de xchat con las funciones que hemos definido
## para ellos
##############################################################################
## Informacion del sistema
#hookgup = xchat.hook_command('gup', uptime_cb)
#hookgos = xchat.hook_command('gos', sistema_cb)
#hookgsoft = xchat.hook_command('gsoft', software_cb)
#hookfecha = xchat.hook_command('fecha', fecha_cb)
#hookpc = xchat.hook_command('gpc', pc_cb)
#hooknet = xchat.hook_command('gnet', red_cb)
## Descarga del script
#hookunload = xchat.hook_unload(unload_cb)
