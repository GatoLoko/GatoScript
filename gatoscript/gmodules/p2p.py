#!/usr/bin/python
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
P2P module for GatoScript.

This module contains function to interact with P2P clients.
"""

__module_name__ = "GatoScript P2P"
__module_description__ = "P2P module for GatoScript"
__module_autor__ = "GatoLoko"

# Load all needed libraries
import xchat
from os import path
import helper
import xml.dom.minidom

#############################################################################
# Define some environment variables
#############################################################################
_HOME = path.expanduser("~")
_AMULESIG = "".join([_HOME, "/.aMule/amulesig.dat"])
_VUZESTATS = "".join([_HOME, "/.azureus/Azureus_Stats.xml"])
_TRANSMISSIONSTATS = "".join([_HOME, "/.config/transmission/stats.json"])


##############################################################################
# Module initialization
##############################################################################


#############################################################################
# Define internal use functions
#############################################################################
def amule_cb(word, word_eol, userdata):
    """Read aMule's onlinesig file and shows up/down speeds and total
    downloaded in the active channel.
    Arguments:
    word     -- array of strings sent by HexChat/X-Chat to every hook (ignored)
    word_eol -- array of strings sent by HexChat/X-Chat to every hook (ignored)
    userdata -- optional variable that can be sent to a hook (ignored)
    """
    if path.exists(_AMULESIG):
        lines = open(_AMULESIG, "r").readlines()
        if lines[0] == "0":
            helper.gprint("aMule isn't connected")
        else:
            down_speed = (lines[6])[0:-1]
            up_speed = (lines[7])[0:-1]
            total_down = helper.units(int(lines[11]), 1024)
            version = lines[13][0:-1]
            xchat.command("".join(["say ( aMule ", version, " )",
                                   " Download: ", down_speed, "KB/s -",
                                   " Upload: ", up_speed, "KB/s -"
                                   " Downloaded: ", total_down]))
    else:
        helper.gprint([_AMULESIG, " file does not exist, check whether you",
                       " have 'Online signature' enabled in your aMule",
                       " settings"])
    return xchat.EAT_ALL


def vuze_cb(word, word_eol, userdata):
    """Read Vuze's statistics file and shows Upload and Download speed in the
    active channel.
    Arguments:
    word     -- array of strings sent by HexChat/X-Chat to every hook (ignored)
    word_eol -- array of strings sent by HexChat/X-Chat to every hook (ignored)
    userdata -- optional variable that can be sent to a hook (ignored)
    """
    if path.exists(_VUZESTATS):
        dom1 = xml.dom.minidom.parse(_VUZESTATS)
        stats = dom1.getElementsByTagName('STATS')[0]
        glob = stats.getElementsByTagName('GLOBAL')[0]
        down = glob.getElementsByTagName('DOWNLOAD_SPEED')[0]
        down_speed = down.getElementsByTagName('TEXT')[0].firstChild.data
        up = glob.getElementsByTagName('UPLOAD_SPEED')[0]
        up_speed = up.getElementsByTagName('TEXT')[0].firstChild.data
        xchat.command("".join(["say ( Vuze ) Download: ", down_speed, " - ",
                               "Upload: ", up_speed]))
        del down, down_speed, up, up_speed, glob, stats, dom1
    else:
        helper.gprint("".join([_VUZESTATS, " file does not exist, check your",
                               " Vuze settings"]))
    return xchat.EAT_ALL


def transmission_cb(word, word_eol, userdata):
    """Reads transmission's stats file and show total Upload and Download in
    the active channel
    Arguments:
    word     -- array of strings sent by HexChat/X-Chat to every hook (ignored)
    word_eol -- array of strings sent by HexChat/X-Chat to every hook (ignored)
    userdata -- optional variable that can be sent to a hook (ignored)
    """
    if path.exists(_TRANSMISSIONSTATS):
        lines = open(_TRANSMISSIONSTATS, "r").readlines()
        downloaded = helper.units(int(lines[1].split(":")[1][1:-3]), 1024)
        uploaded = helper.units(int(lines[5].split(":")[1][1:-1]), 1024)
        xchat.command("".join(["say ( Transmission ) Downloaded: ", downloaded,
                               " - Uploaded: ", uploaded]))
    else:
        helper.gprint("".join(["There is no stats file. Please, check your",
                               " Transmission setting"]))
    return xchat.EAT_ALL


##############################################################################
# Define the help function
##############################################################################
def ghelp():
    """Returns the help information"""
    messages = ["",
                "P2P:",
                "    /amule:             Shows aMule stats",
                "    /vuze:              Shows Vuze stats",
                "    /transmission:      Shows Transmission stats",
                ""]
    return messages


#############################################################################
# Define the function to unload this module. This should be called from the
# main module unload function
#############################################################################
def unload():
    """This function disconects all module functions"""
    xchat.unhook(HOOKAMULE)
    xchat.unhook(HOOKVUZE)
    xchat.unhook(HOOKTRANSMISSION)


#############################################################################
# Hook all callbacks with their respective commands
#############################################################################
HOOKAMULE = xchat.hook_command('amule', amule_cb)
HOOKVUZE = xchat.hook_command('vuze', vuze_cb)
HOOKTRANSMISSION = xchat.hook_command('transmission', transmission_cb)


#############################################################################
# Add menu options
#############################################################################
xchat.command('menu ADD "GatoScript/Downloads"')
xchat.command('menu ADD "GatoScript/Downloads/aMule" "amule"')
xchat.command('menu ADD "GatoScript/Downloads/Vuze" "vuze"')
xchat.command('menu ADD "GatoScript/Downloads/Transmission" "transmission"')
