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
Modulo SysInfo del GatoScript.

Este modulo se contiene funciones para mostrar informacion del sistema
facilmente en GatoScript.
"""

__module_name__ = "GatoScript SysInfo"
__module_description__ = "Modulo SysInfo para el GatoScript"
__module_autor__ = "GatoLoko"

# Cargamos la libreria de funciones de X-Chat
import xchat
# Importamos la funcion para unir directorios de forma portable
#from os import path
#importamos la funcion para ejecutar comandos externos
from subprocess import Popen, PIPE
import re
# Importamos el modulo platform para sacar informacion del sistema
import platform
# Importamos el modulo de funciones auxiliares
import auxiliar


#############################################################################
# Definimos algunas variables que describen el entorno de trabajo y librerias
# opcionales.
#############################################################################


#############################################################################
# Inicializamos el modulo
#############################################################################


#############################################################################
# Definimos las funciones de uso interno en el modulo
#############################################################################


#############################################################################
# Definimos las funciones para obtener la informacion del sistema
#############################################################################
def uptime_cb(word, word_eol, userdata):
    """Muestra en el canal activo el uptime del pc.
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook (ignorado)
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    archivo_uptime = file("/proc/uptime", "r")
    lineas_uptime = archivo_uptime.readline()
    archivo_uptime.close()
    uptime = eval((lineas_uptime.split())[0])
    resto_dias = uptime % 86400
    dias = int(uptime / 86400)
    if dias < 1:
        horas = int(uptime / 3600)
        resto_horas = int(uptime % 3600)
        minutos = int(resto_horas / 60)
        parte1 = "say Uptime: {0} horas ".format(horas)
        parte2 = "y {0} minutos".format(minutos)
        xchat.command("{0}{1}".format(parte1, parte2))
    else:
        if dias > 1:
            cadena_dias = "dias"
        else:
            cadena_dias = "dia"
        horas = int(resto_dias / 3600)
        resto_horas = int(resto_dias % 3600)
        minutos = int(resto_horas / 60)
        parte1 = "say Uptime: {0} {1}, ".format(dias, cadena_dias)
        parte2 = "{0} horas y {1} minutos".format(horas, minutos)
        xchat.command("{0}{1}".format(parte1, parte2))
    return xchat.EAT_ALL

def sistema_cb(word, word_eol, userdata):
    """Muestra en el canal activo informacion sobre el sistema operativo que
    estamos usando.
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook (ignorado)
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    datos = platform.linux_distribution()
    distro = datos[0]
    version = datos[1]
    codigo = datos[2]
    kernel = platform.uname()[2]
    parte1 = "say [ Sistema ] Distribucion: {0}  - ".format(distro)
    parte2 = "Version: {0} {1}  - Kernel: {2}".format(version, codigo, kernel)
    xchat.command("{0}{1}".format(parte1, parte2))
    return xchat.EAT_ALL

def software_cb(word, word_eol, userdata):
    """Muestra en el canal activo informacion sobre las versiones de KERNEL,
    LIBC, X11 y GCC.
    
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook (ignorado)
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    partes = platform.uname()
    sistema = "{0} {1}".format(partes[0], partes[2])
    partes = platform.libc_ver()
    libc = "{0} {1}".format(partes[0], partes[1])
    xdpyinfo = Popen("xdpyinfo | grep version:", shell=True, stdout=PIPE, \
                     stderr=PIPE)
    error = xdpyinfo.stderr.readlines()
    if len(error) > 0:
        for i in range(len(error)):
            auxiliar.gprint(error[i])
        x11 = "Indeterminable"
    else:
        servidor = xdpyinfo.stdout.readlines()[0].split()
    xdpyinfo = Popen('xdpyinfo | grep "vendor string"', shell=True, \
                     stdout=PIPE, stderr=PIPE)
    error = xdpyinfo.stderr.readlines()
    if len(error) > 0:
        for i in range(len(error)):
            auxiliar.gprint(error[i])
        xversion = "Indeterminable"
    else:
        x_version = xdpyinfo.stdout.readlines()
        xversion = x_version[0].split()[3]
        x11 = "{0} {1}".format(xversion, servidor[len(servidor)-1])
    gcc = Popen("gcc --version", shell=True, stdout=PIPE, stderr=PIPE)
    error = gcc.stderr.readlines()
    if len(error) > 0:
        for i in range(len(error)):
            auxiliar.gprint(error[i])
        gcc = "Indeterminable"
    else:
        salida = gcc.stdout.readlines()
        if salida[0] == "bash: gcc: command not found":
            gcc = "No instalado"
        else:
            partes = salida[0].split()
            gcc = partes[2]
    parte1 = "say [ Software ] Kernel: {0}  - ".format(sistema)
    parte2 = "LIBC: {0}  - X11: {1}  - GCC: {2}".format(libc, x11, gcc)
    xchat.command("{0}{1}".format(parte1, parte2))
    del partes, sistema, libc, xdpyinfo, gcc, salida, error, x_version
    del xversion, x11
    return xchat.EAT_ALL

def fecha_cb(word, word_eol, userdata):
    """Muestra en el canal activo la fecha actual.
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook (ignorado)
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    fecha = Popen("date", shell=True, stdout=PIPE, stderr=PIPE)
    error = fecha.stderr.readlines()
    if len(error) > 0:
        for i in range(len(error)):
            auxiliar.gprint(error[i])
    else:
        fecha2 = fecha.stdout.readlines()
        xchat.command("say {0}".format(fecha2[0][:-1]))
    del fecha, fecha2, error
    return xchat.EAT_ALL

def pc_cb(word, word_eol, userdata):
    """Muestra en el canal activo, informacion sobre el pc.
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook (ignorado)
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    # CPU
    archivo = file("/proc/cpuinfo")
    cpuinfo = archivo.readlines()
    archivo.close()
    cpu = cpuinfo[4].split(":")[1][1:-1]
    velocidad = cpuinfo[6].split(":")[1][1:-1]
    # Memoria
    archivo = file("/proc/meminfo")
    meminfo = archivo.readlines()
    archivo.close()
    partes = meminfo[0].split(":")[1][:-1].split(" ")
    memoria = partes[len(partes)-2]
    unidad = partes[len(partes)-1]
    # Free
    partes = meminfo[1].split(":")[1][:-1].split(" ")
    freemem = partes[len(partes)-2]
    # Buffer
    partes = meminfo[2].split(":")[1][:-1].split(" ")
    bufmem = partes[len(partes)-2]
    # Cache
    partes = meminfo[3].split(":")[1][:-1].split(" ")
    cachemem = partes[len(partes)-2]
    # Usada y libre
    usada = int(freemem) + int(bufmem) + int(cachemem)
    libre = int(memoria) - usada
    # Mensaje
    parte1 = "[Informacion del PC] CPU: {0}  - ".format(cpu)
    parte2 = "Velocidad: {0}MHz  - ".format(velocidad)
    parte3 = "Memoria instalada: {0}{1}  - ".format(memoria, unidad)
    parte4 = "Memoria usada: {0}{1}".format(str(libre), unidad)
    mensaje = "{0}{1}{2}{3}".format(parte1, parte2, parte3, parte4)
    xchat.command("say {0}".format(mensaje))
    return xchat.EAT_ALL

def red_cb(word, word_eol, userdata):
    """Muestra en el canal activo, informacion sobre la red.
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook (ignorado)
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    red = re.compile('eth|ath|wlan|ra([0-9]):')
    hostname = file("/etc/hostname").readline().split("\n")[0]
    for linea in file("/proc/net/dev"):
        if red.search(linea):
            dispositivo = linea.split(":")[0].split()[-1]
            partes = linea[:-1].split(":")[1].split()
            recibido = auxiliar.unidades(int(partes[0]), 1024)
            enviado = auxiliar.unidades(int(partes[8]), 1024)
            parte1 = "[ Red ] Hostname: {0}  - ".format(hostname)
            parte2 = "Dispositivo: {0}  - ".format(dispositivo)
            parte3 = "Recibidos: {0}  - ".format(recibido)
            parte4 = "Enviados: {0}".format(enviado)
            mensaje = "{0}{1}{2}{3}".format(parte1, parte2, parte3, parte4)
            xchat.command("say {0}".format(mensaje))
    return xchat.EAT_ALL

def graficos_cb(word, word_eol, userdata):
    """Muestra en el canal activo, informacion sobre la interfaz grafica.
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook (ignorado)
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    datos = Popen("lspci | grep VGA", shell=True, stdout=PIPE, stderr=PIPE)
    error = datos.stderr.readlines()
    if len(error) > 0:
        auxiliar.gprint(error)
        grafica = "No se pudo determinar el modelo"
    else:
        grafica = datos.stdout.readlines()[0].split(": ")[1][:-1]
    datos = Popen("xdpyinfo | grep dimensions", shell=True, stdout=PIPE, \
                  stderr=PIPE)
    error = datos.stderr.readlines()
    if len(error) > 0:
        auxiliar.gprint(error)
        resolucion = "No se pudo determinar el modelo"
    else:
        resolucion = datos.stdout.readlines()[0].split(":    ")[1][:-1]
    parte1 = "say [ Graficos ] Dispositivo: {0}  - ".format(grafica)
    parte2 = "Resolucion: {0}  - ".format(resolucion)
    xchat.command("{0}{1}".format(parte1, parte2))
    return xchat.EAT_ALL

#############################################################################
# Definimos las funciones de informacion y ayuda sobre el manejo del script
#############################################################################
def ayuda():
    """Muestra la ayuda de sysinfo"""
    mensajes = [
        "",
        "Informacion del sistema:",
        "    /gup:    Muestra el uptime del sistema",
        "    /gos:    Muestra la distribucion y su version",
        "    /gsoft:  Muestra en el canal la version de los programas mas",
        "             importantes",
        "    /gpc:    Muestra en el canal informacion sobre el hardware del pc",
        "    /gnet:   Muestra en el canal informacion sobre la red",
        "    /ggraf:  Muestra en el canal la tarjeta grafica y la resolucion",
        "    /hora:   Muestra en el canal la hora del sistema",
        ""]
    return mensajes


#############################################################################
# Definimos la funcion para la descarga del programa
#############################################################################
def unload_cb():
    """Esta funcion debe desconectar todas las funciones del modulo al
    descargarse el script
    Argumentos:
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    # Desconectamos los comandos
    xchat.unhook(HOOKGUP)
    xchat.unhook(HOOKGOS)
    xchat.unhook(HOOKGSOFT)
    xchat.unhook(HOOKFECHA)
    xchat.unhook(HOOKGPC)
    xchat.unhook(HOOKNET)
    xchat.unhook(HOOKGRAF)
    # Descarga
    xchat.unhook(HOOKSYSINFO)


#############################################################################
# Conectamos los "lanzadores" de xchat con las funciones que hemos definido
# para ellos
#############################################################################
# Informacion del sistema
HOOKGUP = xchat.hook_command('gup', uptime_cb)
HOOKGOS = xchat.hook_command('gos', sistema_cb)
HOOKGSOFT = xchat.hook_command('gsoft', software_cb)
HOOKFECHA = xchat.hook_command('fecha', fecha_cb)
HOOKGPC = xchat.hook_command('gpc', pc_cb)
HOOKNET = xchat.hook_command('gnet', red_cb)
HOOKGRAF = xchat.hook_command('ggraf', graficos_cb)
# Descarga del script
HOOKSYSINFO = xchat.hook_unload(unload_cb)


#############################################################################
# Añadimos las opciones del menu
#############################################################################
xchat.command('menu ADD "GatoScript/Sistema"')
xchat.command('menu ADD "GatoScript/Sistema/Uptime" "gup"')
xchat.command('menu ADD "GatoScript/Sistema/Sistema" "gos"')
xchat.command('menu ADD "GatoScript/Sistema/Software" "gsoft"')
xchat.command('menu ADD "GatoScript/Sistema/Hardware" "gpc"')
xchat.command('menu ADD "GatoScript/Sistema/Fecha" "fecha"')
xchat.command('menu ADD "GatoScript/Sistema/Red" "gnet"')
xchat.command('menu ADD "GatoScript/Sistema/Graficos" "ggraf"')
