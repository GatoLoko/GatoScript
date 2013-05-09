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
Modulo P2P del GatoScript.

Este modulo contiene las funciones para acceder a informacion de clientes P2P
desde el GatoScript.
"""

__module_name__ = "GatoScript P2P"
__module_description__ = "Modulo P2P para el GatoScript"
__module_autor__ = "GatoLoko"

# Cargamos la libreria y funciones que necesitamos
import xchat
from os import path
import auxiliar
import xml.dom.minidom

#############################################################################
# Definimos algunas variables que describen el entorno de trabajo y librerias
# opcionales.
#############################################################################
_HOME = path.expanduser("~")
_AMULESIG = "".join([_HOME, "/.aMule/amulesig.dat"])
_AZUREUSSTATS = "".join([_HOME, "/.azureus/Azureus_Stats.xml"])
_TRANSMISSIONSTATSOLD = "".join([_HOME, "/.transmission/stats.benc"])
_TRANSMISSIONSTATSNEW = "".join([_HOME, "/.config/transmission/stats.json"])


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


def azureus_cb(word, word_eol, userdata):
    """Lee el archivo Azureus_Stats.xml (estadisticas) de azureus y muestra
    parte de la informacion en el canal activo.
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook (ignorado)
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    if path.exists(_AZUREUSSTATS):
        dom1 = xml.dom.minidom.parse(_AZUREUSSTATS)
        stats = dom1.getElementsByTagName('STATS')[0]
        glob = stats.getElementsByTagName('GLOBAL')[0]
        descarga = glob.getElementsByTagName('DOWNLOAD_SPEED')[0]
        vdescarga = descarga.getElementsByTagName('TEXT')[0].firstChild.data
        subida = glob.getElementsByTagName('UPLOAD_SPEED')[0]
        vsubida = subida.getElementsByTagName('TEXT')[0].firstChild.data
        xchat.command("".join(["say ( Azureus ) Descarga: ", vdescarga, " - ",
                               "Subida: ", vsubida]))
        del descarga, vdescarga, subida, vsubida, glob, stats, dom1
    else:
        auxiliar.gprint("".join(["No existe el archivo ", _AZUREUSSTATS, ",",
                                 " compruebe su configuración de Azureus"]))
    return xchat.EAT_ALL


def transmission_cb(word, word_eol, userdata):
    """Lee el archivo stats.benc (estadisticas) de Transmission y muestra parte
    de la informacion en el canal activo.
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook (ignorado)
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    if path.exists(_TRANSMISSIONSTATSOLD):
        textos = [[1, 3], [17, 3], [12, 3], [15, 3], [14, 3], [15, 2]]
        parte = []
        archivo = file(_TRANSMISSIONSTATSOLD, "r")
        partes = archivo.readline().split(':')
        #print partes
        archivo.close()
        for i in range(1, len(partes)):
            parte.append(partes[i][textos[i][0]:-textos[i][1]])
        descargado = auxiliar.unidades(int(parte[0]), 1024)
        subido = auxiliar.unidades(int(parte[4]), 1024)
        xchat.command("".join(["say ( Transmission ) Descargado: ", descargado,
                               " - Subido: ", subido]))
    elif path.exists(_TRANSMISSIONSTATSNEW):
        archivo = file(_TRANSMISSIONSTATSNEW, "r")
        lineas = archivo.readlines()
        archivo.close()
        descargado = auxiliar.unidades(int(lineas[1].split(":")[1][1:-3]), 1024)
        subido = auxiliar.unidades(int(lineas[5].split(":")[1][1:-1]), 1024)
        xchat.command("".join(["say ( Transmission ) Descargado: ", descargado,
                               " - Subido: ", subido]))
    else:
        auxiliar.gprint("".join(["No existe el archivo de estadísticas en sus",
                        " ubicaciones habituales. Por favor, compruebe su",
                        " configuración de Transmission."]))
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
    "    /azureus:           Shows Azureus stats",
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
    xchat.unhook(HOOKAZUREUS)
    xchat.unhook(HOOKTRANSMISSION)


#############################################################################
# Conectamos los "lanzadores" de xchat con las funciones que hemos definido
# para ellos
#############################################################################
# Peer to Peer
HOOKAMULE = xchat.hook_command('amule', amule_cb)
HOOKAZUREUS = xchat.hook_command('azureus', azureus_cb)
HOOKTRANSMISSION = xchat.hook_command('transmission', transmission_cb)


#############################################################################
# Añadimos las opciones del menu
#############################################################################
xchat.command('menu ADD "GatoScript/Descargas"')
xchat.command('menu ADD "GatoScript/Descargas/aMule" "amule"')
xchat.command('menu ADD "GatoScript/Descargas/Azureus" "azureus"')
xchat.command('menu ADD "GatoScript/Descargas/Transmission" "transmission"')
