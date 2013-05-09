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
# Definimos algunas variables que describen el entorno de trabajo y librerias
# opcionales.
#############################################################################
_HOME = path.expanduser("~")
_AMULESIG = "".join([_HOME, "/.aMule/amulesig.dat"])
_VUZESTATS = "".join([_HOME, "/.azureus/Azureus_Stats.xml"])
_TRANSMISSIONSTATS = "".join([_HOME, "/.config/transmission/stats.json"])


##############################################################################
# Inicializamos el modulo
##############################################################################


##############################################################################
## Definimos las funciones para mostrar informacion P2P
##############################################################################
def amule_cb(word, word_eol, userdata):
    """Lee el archivo onlinesig (firma online) de amule y muestra parte de la
    informacion en el canal activo.
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook (ignorado)
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    if path.exists(_AMULESIG):
        archivo = file(_AMULESIG, "r")
        lineas_amule = archivo.readlines()
        archivo.close()
        if lineas_amule[0] == "0":
            auxiliar.gprint("No estas conectado a aMule")
        else:
            vdescarga = (lineas_amule[6])[0:-1]
            vsubida = (lineas_amule[7])[0:-1]
            total_descarga = auxiliar.unidades(int(lineas_amule[11]), 1024)
            version = lineas_amule[13][0:-1]
            xchat.command("".join(["say ( aMule ", version, " )",
                                   " Descarga: ", vdescarga, "KB/s -",
                                   " Subida: ", vsubida, "KB/s -"
                                   " Total descargado: ", total_descarga]))
    else:
        parte1 = "No existe el archivo {0}, compruebe que ".format(_AMULESIG)
        parte2 = "esté activada la firma online en la configuracion de aMule."
        auxiliar.gprint("{0}{1}".format(parte1, parte2))
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
    """Reads transmission's stats file and show some of the statistics in the
    active channel
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
def help():
    """Returns the help information"""
    messages = [
    "",
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
# Conectamos los "lanzadores" de xchat con las funciones que hemos definido
# para ellos
#############################################################################
# Peer to Peer
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
