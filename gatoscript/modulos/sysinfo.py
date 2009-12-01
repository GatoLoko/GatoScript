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
from os import path
#importamos la funcion para ejecutar comandos externos
from subprocess import Popen, PIPE
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
        xchat.command("say Uptime: %s horas y %s minutos" %(horas, minutos))
    else:
        if dias > 1:
            cadena_dias = "dias"
        else:
            cadena_dias = "dia"
        horas = int(resto_dias / 3600)
        resto_horas = int(resto_dias % 3600)
        minutos = int(resto_horas / 60)
        xchat.command("say Uptime: %s %s, %s horas y %s minutos" \
                      %(dias, cadena_dias, horas, minutos))
    return xchat.EAT_ALL

def sistema_cb(word, word_eol, userdata):
    """Muestra en el canal activo informacion sobre el sistema operativo que
    estamos usando.
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook (ignorado)
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    if path.exists("/etc/lsb-release"):
        lsb = file("/etc/lsb-release", "r")
        lineas_lsb = lsb.readlines()
        lsb.close()
        distro = (lineas_lsb[0])[11:len(lineas_lsb[0])-1]
        version = (lineas_lsb[1])[16:len(lineas_lsb[1])-1]
        codigo = (lineas_lsb[2])[17:len(lineas_lsb[2])-1]
        uname = Popen("uname -r", shell=True, stdout=PIPE, stderr=PIPE)
        error = uname.stderr.readlines()
        if len(error) > 0:
            auxiliar.gprint(error)
        else:
            kernel = uname.stdout.readlines()
            kernel2 = kernel[0][:-1]
        xchat.command("say Distribucion: %s  - Version: %s %s  - Kernel: %s" \
                      %(distro, version, codigo, kernel2))
    else:
        auxiliar.gprint("La distribucion no cumple con LSB")
    return xchat.EAT_ALL

def software_cb(word, word_eol, userdata):
    """Muestra en el canal activo informacion sobre las versiones de KERNEL,
    LIBC, X11 y GCC.
    
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook (ignorado)
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    uname = Popen("uname -sr", shell=True, stdout=PIPE, stderr=PIPE)
    error = uname.stderr.readlines()
    if len(error) > 0:
        for i in range(len(error)):
            auxiliar.gprint(error[i])
        sistema = "Indeterminable"
    else:
        sistema = uname.stdout.readlines()[0][:-1]
    glibc = Popen("/lib/libc.so.6", shell=True, stdout=PIPE, stderr=PIPE)
    error = glibc.stderr.readlines()
    salida = glibc.stdout.readlines()
    if len(error) > 0:
        for i in range(len(error)):
            auxiliar.gprint(error[i])
        libc = "Indeterminable"
    else:
        if salida[0].split()[0] == "GNU":
            licencia = "GLIBC"
        libc = licencia + " " + salida[0].split()[6][:-1]
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
        x11 = xversion + " " + servidor[len(servidor)-1]
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
    xchat.command("say Kernel: %s  - LIBC: %s  - X11: %s  - GCC: %s" \
                  %(sistema, libc, x11, gcc))
    del glibc, xdpyinfo, gcc, uname, salida, error, x_version, xversion, x11
    del sistema
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
        xchat.command("say %s" % (fecha2[0][:-1]))
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
    parte1 = "[Informacion del PC] CPU: %s  - Velocidad: %sMHz  - Memoria " \
             % (cpu, velocidad)
    parte2 = "instalada: %s%s  - Memoria usada: %s%s" % (memoria, unidad, \
                                                        str(libre), unidad)
    mensaje = "%s%s" % (parte1, parte2)
    xchat.command("say " + mensaje)
    return xchat.EAT_ALL

def red_cb(word, word_eol, userdata):
    """Muestra en el canal activo, informacion sobre la red.
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook (ignorado)
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    archivo = file("/etc/hostname")
    hostname = archivo.read()
    archivo.close()
    auxiliar.gprint("( Hostname ) " + hostname)
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
        "    /gsoft:  Muestra en el canal la version de los programas mas importantes",
        "    /gpc:    Muestra en el canal informacion sobre el hardware del pc",
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