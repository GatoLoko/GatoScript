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
SysInfo module for GatoScript.

This module contains functions to show system information.
"""

__module_name__ = "GatoScript SysInfo"
__module_description__ = "SysInfo module for GatoScript"
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
# Importamos el modulo datetime para obtener la fecha y hora
import datetime
import helper


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
        comando = "".join(["say Uptime: ", str(horas), " horas y ",
            str(minutos), "minutos"])
        xchat.command(comando)
    else:
        if dias > 1:
            cadena_dias = "dias"
        else:
            cadena_dias = "dia"
        horas = int(resto_dias / 3600)
        resto_horas = int(resto_dias % 3600)
        minutos = int(resto_horas / 60)
        comando = "".join(["say Uptime: ", str(dias), " ", cadena_dias, ", ",
            str(horas), " horas y ", str(minutos), " minutos"])
        xchat.command(comando)
    return xchat.EAT_ALL


def os_cb(word, word_eol, userdata):
    """Shows information about the operating system on the current channel.
    Arguments:
    word     -- array of strings sent by HexChat/X-Chat to every hook (ignored)
    word_eol -- array of strings sent by HexChat/X-Chat to every hook (ignored)
    userdata -- optional variable that can be sent to a hook (ignored)
    """
    data = platform.linux_distribution()
    distribution = data[0]
    version = " ".join(data[1:3])
    kernel = " ".join([platform.system(), platform.release()])
    command = "".join(["say [ System ] Distribution: ", distribution,
                       "  - Version: ", version, "  - Kernel: ", kernel])
    xchat.command(command)
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
    sistema = " ".join([partes[0], partes[2]])
    libc = " ".join(platform.libc_ver()[0:2])
    xdpyinfo = Popen("xdpyinfo | grep version:", shell=True, stdout=PIPE,
         stderr=PIPE)
    error = xdpyinfo.stderr.readlines()
    if len(error) > 0:
        for i in range(len(error)):
            auxiliar.gprint(error[i])
        x11 = "Indeterminable"
    else:
        servidor = xdpyinfo.stdout.readlines()[0].split()[-1]
    xdpyinfo = Popen('xdpyinfo | grep "vendor string"', shell=True,
         stdout=PIPE, stderr=PIPE)
    error = xdpyinfo.stderr.readlines()
    if len(error) > 0:
        for i in range(len(error)):
            auxiliar.gprint(error[i])
        xversion = "Indeterminable"
    else:
        x_version = xdpyinfo.stdout.readlines()
        xversion = x_version[0].split()[3]
        x11 = "".join([xversion, " ", servidor])
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
            gcc = partes[-1]
    comando = "".join(["say [ Software ] Kernel: ", sistema, "  - LIBC: ",
        libc, "  - X11: ", x11, "  - GCC: ", gcc])
    xchat.command(comando)
    del partes, sistema, libc, xdpyinfo, gcc, salida, error, x_version
    del xversion, x11
    return xchat.EAT_ALL


def date_cb(word, word_eol, userdata):
    """Shows the current date on the active channel.
    Arguments:
    word     -- array of strings sent by HexChat/X-Chat to every hook (ignored)
    word_eol -- array of strings sent by HexChat/X-Chat to every hook (ignored)
    userdata -- optional variable that can be sent to a hook (ignored)
    """
    date = datetime.datetime.now()
    xchat.command("".join(["say [ Date/Time ] ", str(date.isoformat())]))
    del date
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
    memoria = partes[-2]
    unidad = partes[-1]
    # Free
    partes = meminfo[1].split(":")[1][:-1].split(" ")
    freemem = partes[-2]
    # Buffer
    partes = meminfo[2].split(":")[1][:-1].split(" ")
    bufmem = partes[-2]
    # Cache
    partes = meminfo[3].split(":")[1][:-1].split(" ")
    cachemem = partes[-2]
    # Usada y libre
    usada = int(freemem) + int(bufmem) + int(cachemem)
    libre = int(memoria) - usada
    # Mensaje
    comando = "".join(["say [ Informacion del PC ] CPU: ", cpu,
        "  - Velocidad: ", velocidad, "MHz  - Memoria instalada: ",
        str(memoria), unidad, "  - Memoria usada: ", str(libre), unidad])
    xchat.command(comando)
    return xchat.EAT_ALL


def red_cb(word, word_eol, userdata):
    """Muestra en el canal activo, informacion sobre la red.
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook (ignorado)
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    red = re.compile('eth|ath|wlan|ra([0-9]):')
    hostname = platform.node()
    for linea in file("/proc/net/dev"):
        if red.search(linea):
            dispositivo = linea.split(":")[0].split()[-1]
            partes = linea[:-1].split(":")[1].split()
            recibido = auxiliar.unidades(int(partes[0]), 1024)
            enviado = auxiliar.unidades(int(partes[8]), 1024)
            comando = "".join(["say [ Red ] Hostname: ", hostname,
                "  - Dispositivo: ", dispositivo, "  - Recibidos: ", recibido,
                "  - Enviado: ", enviado])
            xchat.command(comando)
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
    datos = Popen("xdpyinfo | grep dimensions", shell=True, stdout=PIPE,
        stderr=PIPE)
    error = datos.stderr.readlines()
    if len(error) > 0:
        auxiliar.gprint(error)
        resolucion = "No se pudo determinar el modelo"
    else:
        resolucion = datos.stdout.readlines()[0].split(":    ")[1][:-1]
    xchat.command("".join(["say [ Graficos ] Dispositivo: ", grafica, "  - ",
                           "Resolucion: ", resolucion]))
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
    xchat.unhook(HOOKGPC)
    xchat.unhook(HOOKDATE)
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
HOOKGOS = xchat.hook_command('gos', os_cb)
HOOKGSOFT = xchat.hook_command('gsoft', software_cb)
HOOKGPC = xchat.hook_command('gpc', pc_cb)
HOOKNET = xchat.hook_command('gnet', red_cb)
HOOKGRAF = xchat.hook_command('ggraf', graficos_cb)
# Descarga del script
HOOKSYSINFO = xchat.hook_unload(unload_cb)
HOOKDATE = xchat.hook_command('gdate', date_cb)


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
