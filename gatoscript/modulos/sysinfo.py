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

# Load all needed libraries
import xchat
from subprocess import Popen, PIPE
import re
import platform
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
    """Show system uptime in the active channel.
    Arguments:
    word     -- array of strings sent by HexChat/X-Chat to every hook (ignored)
    word_eol -- array of strings sent by HexChat/X-Chat to every hook (ignored)
    userdata -- optional variable that can be sent to a hook (ignored)
    """
    uptime_data = file("/proc/uptime", "r").readlines()
    uptime = float(uptime_data[0].split()[0])
    days_remainder = uptime % 86400
    days = int(uptime / 86400)
    if days < 1:
        hours = int(uptime / 3600)
        hours_remainder = int(uptime % 3600)
        minutes = int(hours_remainder / 60)
        command = "".join(["say Uptime: ", str(hours), " hours and ",
                           str(minutes), "minutes"])
    else:
        if days > 1:
            days_string = "days"
        else:
            days_string = "day"
        hours = int(days_remainder / 3600)
        hours_remainder = int(days_remainder % 3600)
        minutes = int(hours_remainder / 60)
        command = "".join(["say [ Uptime ] ", str(days), " ", days_string,
                           ", ", str(hours), " hours and ", str(minutes),
                           " minutes"])
    xchat.command(command)
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
    """Shows information about the current kernel, LIBC, X11 and GCC on the
    current channel.

    Arguments:
    word     -- array of strings sent by HexChat/X-Chat to every hook (ignored)
    word_eol -- array of strings sent by HexChat/X-Chat to every hook (ignored)
    userdata -- optional variable that can be sent to a hook (ignored)
    """
    # Find kernel and libc
    data = platform.uname()
    kernel = " ".join([data[0], data[2]])
    libc = " ".join(platform.libc_ver()[0:2])
    # Find X11 server and version
    xdpyinfo = Popen("xdpyinfo | grep version:", shell=True, stdout=PIPE,
                     stderr=PIPE)
    error = xdpyinfo.stderr.readlines()
    if len(error) > 0:
        for i in range(len(error)):
            helper.gprint(error[i])
        x11 = "Unknown"
    else:
        xserver = xdpyinfo.stdout.readlines()[0].split()[-1]
    xdpyinfo = Popen('xdpyinfo | grep "vendor string"', shell=True,
                     stdout=PIPE, stderr=PIPE)
    error = xdpyinfo.stderr.readlines()
    if len(error) > 0:
        for i in range(len(error)):
            helper.gprint(error[i])
        xversion = "Unknown"
    else:
        x_version = xdpyinfo.stdout.readlines()
        xversion = x_version[0].split()[3]
        x11 = "".join([xversion, " ", xserver])
    # Find GCC version
    gcc = Popen("gcc --version", shell=True, stdout=PIPE, stderr=PIPE)
    error = gcc.stderr.readlines()
    if len(error) > 0:
        for i in range(len(error)):
            helper.gprint(error[i])
        gcc = "Unknown"
    else:
        gcc_output = gcc.stdout.readlines()
        if gcc_output[0] == "bash: gcc: command not found":
            gcc = "Not installed"
        else:
            data = gcc_output[0].split()
            gcc = data[-1]
    command = "".join(["say [ Software ] Kernel: ", kernel, "  - LIBC: ",
                       libc, "  - X11: ", x11, "  - GCC: ", gcc])
    xchat.command(command)
    del data, kernel, libc, xdpyinfo, gcc, gcc_output, error, x_version
    del xversion, x11, xserver
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


def hardware_cb(word, word_eol, userdata):
    """Shows information about the computer on the active channel.
    Arguments:
    word     -- array of strings sent by HexChat/X-Chat to every hook (ignored)
    word_eol -- array of strings sent by HexChat/X-Chat to every hook (ignored)
    userdata -- optional variable that can be sent to a hook (ignored)
    """
    # CPU
    data = file("/proc/cpuinfo")
    cpuinfo = data.readlines()
    data.close()
    cpu = cpuinfo[4].split(":")[1][1:-1]
    speed = cpuinfo[6].split(":")[1][1:-1]
    # Memory
    data = file("/proc/meminfo")
    meminfo = data.readlines()
    memparts = meminfo[0].split(":")[1][:-1].split(" ")
    data.close()
    memory = memparts[-2]
    units = memparts[-1]
    ## Free
    memparts = meminfo[1].split(":")[1][:-1].split(" ")
    freemem = memparts[-2]
    ## Buffer
    memparts = meminfo[2].split(":")[1][:-1].split(" ")
    bufmem = memparts[-2]
    ## Cache
    memparts = meminfo[3].split(":")[1][:-1].split(" ")
    cachemem = memparts[-2]
    ## Used and free
    used = int(freemem) + int(bufmem) + int(cachemem)
    free = int(memory) - used
    # Message
    command = "".join(["say [ Hardware ] CPU: ", cpu, "  - Speed: ", speed,
                       "MHz  - Installed Memory: ", str(memory), units,
                       "  - Used Memory: ", str(free), units])
    xchat.command(command)
    return xchat.EAT_ALL


def network_cb(word, word_eol, userdata):
    """Shows network information on the active channel.
    Arguments:
    word     -- array of strings sent by HexChat/X-Chat to every hook (ignored)
    word_eol -- array of strings sent by HexChat/X-Chat to every hook (ignored)
    userdata -- optional variable that can be sent to a hook (ignored)
    """
    # Find all devices and show a line for each one
    net = re.compile('eth|ath|wlan|ra([0-9]):')
    hostname = platform.node()
    for line in file("/proc/net/dev"):
        if net.search(line):
            device = line.split(":")[0].split()[-1]
            parts = line[:-1].split(":")[1].split()
            received = helper.units(int(parts[0]), 1024)
            sent = helper.units(int(parts[8]), 1024)
            command = "".join(["say [ Red ] Device: ", device,
                               "  - Hostname: ", hostname, "  - Received: ",
                               received, "  - Sent: ", sent])
            xchat.command(command)
    return xchat.EAT_ALL


def graphics_cb(word, word_eol, userdata):
    """Shows graphics devices information on the current channel.
    Arguments:
    word     -- array of strings sent by HexChat/X-Chat to every hook (ignored)
    word_eol -- array of strings sent by HexChat/X-Chat to every hook (ignored)
    userdata -- optional variable that can be sent to a hook (ignored)
    """
    # Find a list of devices
    data = Popen("lspci | grep VGA", shell=True, stdout=PIPE, stderr=PIPE)
    error = data.stderr.readlines()
    if len(error) > 0:
        for line in error:
            helper.gprint(line)
        devices = ["Unknown device"]
    else:
        devices = []
        for line in data.stdout:
            devices.append(line.split(": ")[1][:-1])
    # Show a line for each device found
    for device in devices:
        xchat.command("".join(["say ", "[ Graphics ] Device: ", device]))
    # Find the screen resolution for all active screen
    data = Popen("xdpyinfo | grep dimensions", shell=True, stdout=PIPE,
                 stderr=PIPE)
    error = data.stderr.readlines()
    if len(error) > 0:
        for line in error:
            helper.gprint(line)
        resolutions = ["Unknown resolution"]
    else:
        resolutions = []
        for line in data.stdout:
            resolutions.append(line.split(":    ")[1][:-1])
    # Show a line for each active screen
    for resolution in resolutions:
        xchat.command("".join(["say ", "[ Graphics ] Screen: ", resolution]))
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
    xchat.unhook(HOOKDATE)
    xchat.unhook(HOOKGHARD)
    xchat.unhook(HOOKNET)
    # Descarga
    xchat.unhook(HOOKSYSINFO)
    xchat.unhook(HOOKGRAPH)


#############################################################################
# Conectamos los "lanzadores" de xchat con las funciones que hemos definido
# para ellos
#############################################################################
# Informacion del sistema
HOOKGUP = xchat.hook_command('gup', uptime_cb)
HOOKGOS = xchat.hook_command('gos', os_cb)
HOOKGSOFT = xchat.hook_command('gsoft', software_cb)
# Descarga del script
HOOKSYSINFO = xchat.hook_unload(unload_cb)
HOOKDATE = xchat.hook_command('gdate', date_cb)
HOOKGHARD = xchat.hook_command('ghard', hardware_cb)
HOOKNET = xchat.hook_command('gnet', network_cb)
HOOKGRAPH = xchat.hook_command('ggraph', graphics_cb)


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
