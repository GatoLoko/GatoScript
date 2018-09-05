# -*- coding: UTF8 -*-

# CopyRight (C) 2006-2013 GatoLoko
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
import hexchat
from subprocess import Popen, PIPE
import re
import platform
import datetime
from . import helper


#############################################################################
# Define some environment variables
#############################################################################


#############################################################################
# Initialize the module
#############################################################################


#############################################################################
# Define internal use functions
#############################################################################
def uptime_cb(word, word_eol, userdata):
    """Show system uptime in the active channel.
    Arguments:
    word     -- array of strings sent by HexChat/X-Chat to every hook (ignored)
    word_eol -- array of strings sent by HexChat/X-Chat to every hook (ignored)
    userdata -- optional variable that can be sent to a hook (ignored)
    """
    uptime_data = open("/proc/uptime", "r").readlines()
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
    hexchat.command(command)
    return hexchat.EAT_ALL


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
    hexchat.command(command)
    return hexchat.EAT_ALL


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
        x11 = "%s %s" % (xversion.decode(), xserver.decode())
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
            gcc = data[-2].decode()
    command = "say [ Software ] Kernel: %s  - LIBC: %s  - X11: %s  - GCC: " \
              "%s" % (kernel, libc, x11, gcc)
    hexchat.command(command)
    del data, kernel, libc, xdpyinfo, gcc, gcc_output, error, x_version
    del xversion, x11, xserver
    return hexchat.EAT_ALL


def date_cb(word, word_eol, userdata):
    """Shows the current date on the active channel.
    Arguments:
    word     -- array of strings sent by HexChat/X-Chat to every hook (ignored)
    word_eol -- array of strings sent by HexChat/X-Chat to every hook (ignored)
    userdata -- optional variable that can be sent to a hook (ignored)
    """
    date = datetime.datetime.now()
    hexchat.command("".join(["say [ Date/Time ] ", str(date.isoformat())]))
    del date
    return hexchat.EAT_ALL


def hardware_cb(word, word_eol, userdata):
    """Shows information about the computer on the active channel.
    Arguments:
    word     -- array of strings sent by HexChat/X-Chat to every hook (ignored)
    word_eol -- array of strings sent by HexChat/X-Chat to every hook (ignored)
    userdata -- optional variable that can be sent to a hook (ignored)
    """
    # CPU
    with open("/proc/cpuinfo") as data:
        cpuinfo = data.readlines()
    # Fin the lines with "name", take the first one, split out the name
    cpu = [x for x in cpuinfo if "name" in x][0].split(":")[1][1:-1]
    speed = [x for x in cpuinfo if "MHz" in x][0].split(":")[1][1:-1]
    # Memory
    with open("/proc/meminfo", 'r') as data:
        meminfo = data.readlines()
    for line in meminfo:
        if "MemTotal" in line:
            memory, units = line.split(":")[1].strip().split(" ")
        if "MemFree" in line:
            memfree = line.split(":")[1].strip().split(" ")[0]
        if "Buffers" in line:
            bufmem = line.split(":")[1].strip().split(" ")[0]
        if "Cached" in line:
            cachemem = line.split(":")[1].strip().split(" ")[0]
    # Used and free
    used = int(memory) - int(memfree) - int(bufmem) - int(cachemem)
    # Message:
    command = "".join(["say [ Hardware ] CPU: ", cpu, "  - Speed: ", speed,
                       "MHz  - Installed Memory: ", str(memory), units,
                       "  - Used Memory: ", str(used), units])
    hexchat.command(command)
    return hexchat.EAT_ALL


def network_cb(word, word_eol, userdata):
    """Shows network information on the active channel.
    Arguments:
    word     -- array of strings sent by HexChat/X-Chat to every hook (ignored)
    word_eol -- array of strings sent by HexChat/X-Chat to every hook (ignored)
    userdata -- optional variable that can be sent to a hook (ignored)
    """
    # Find all devices and show a line for each one
    netre = '((eth|ath|wlan|ra|(en[spo]([0-9])+s)|vtnet)([0-9])+)|enx([0-9a-f])+:'
    net = re.compile(netre, re.IGNORECASE)
    hostname = platform.node()
    for line in open("/proc/net/dev"):
        if net.search(line):
            device = line.split(":")[0].split()[-1]
            parts = line[:-1].split(":")[1].split()
            received = helper.units(int(parts[0]), 1024)
            sent = helper.units(int(parts[8]), 1024)
            command = "".join(["say [ Network ] Device: ", device,
                               "  - Hostname: ", hostname, "  - Received: ",
                               received, "  - Sent: ", sent])
            hexchat.command(command)
    return hexchat.EAT_ALL


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
            devices.append(line.decode().split(": ")[1][:-1])
    # Show a line for each device found
    for device in devices:
        hexchat.command("".join(["say ", "[ Graphics ] Device: ", device]))
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
            resolutions.append(line.decode().split(":    ")[1][:-1])
    # Show a line for each active screen
    for resolution in resolutions:
        hexchat.command("".join(["say ", "[ Graphics ] Screen: ", resolution]))
    return hexchat.EAT_ALL


#############################################################################
# Define the help function
#############################################################################
def ghelp():
    """Returns the help information."""
    messages = [
        "System information:",
        "  /gup:    Shows current system uptime",
        "  /gos:    Shows current operating system",
        "  /gsoft:  Shows most relevant software versions",
        "  /ghard:  Shows some hardware information",
        "  /gnet:   Shows network(s) information",
        "  /ggraph: Shows graphic card(s) and screen(s) resolution(s)",
        "  /gdate:  Shows the current system time and date",
        ""]
    return messages


#############################################################################
# Define the function to unload this module. This should be called from the
# main module unload function
#############################################################################
def unload():
    """This function disconects all module functions"""
    hexchat.unhook(HOOKGUP)
    hexchat.unhook(HOOKGOS)
    hexchat.unhook(HOOKGSOFT)
    hexchat.unhook(HOOKDATE)
    hexchat.unhook(HOOKGHARD)
    hexchat.unhook(HOOKNET)
    hexchat.unhook(HOOKGRAPH)


#############################################################################
# Hook all callbacks with their respective commands
#############################################################################
HOOKGUP = hexchat.hook_command('gup', uptime_cb)
HOOKGOS = hexchat.hook_command('gos', os_cb)
HOOKGSOFT = hexchat.hook_command('gsoft', software_cb)
HOOKDATE = hexchat.hook_command('gdate', date_cb)
HOOKGHARD = hexchat.hook_command('ghard', hardware_cb)
HOOKNET = hexchat.hook_command('gnet', network_cb)
HOOKGRAPH = hexchat.hook_command('ggraph', graphics_cb)


#############################################################################
# Add menu options
#############################################################################
hexchat.command('menu ADD "GatoScript/System"')
hexchat.command('menu ADD "GatoScript/System/Uptime" "gup"')
hexchat.command('menu ADD "GatoScript/System/System" "gos"')
hexchat.command('menu ADD "GatoScript/System/Software" "gsoft"')
hexchat.command('menu ADD "GatoScript/System/Hardware" "ghard"')
hexchat.command('menu ADD "GatoScript/System/Date" "gdate"')
hexchat.command('menu ADD "GatoScript/System/Network" "gnet"')
hexchat.command('menu ADD "GatoScript/System/Graphics" "ggraph"')
