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
_AMULESIG = _HOME + "/.aMule/amulesig.dat"
_AZUREUSSTATS = _HOME + "/.azureus/Azureus_Stats.xml"
_TRANSMISSIONSTATS = _HOME + "/.transmission/stats.benc"

##############################################################################
# Inicializamos el modulo
##############################################################################

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
        #"    -d         Comandos para informacion de Descargas",
        #"",
        #"Por ejemplo: /gato -s",
        #""]
    #else:
        #if word[1] == "-d":
            #mensajes = [
            #"",
            #"Descargas",
            #"    /amule:             Muestra la informacion de aMule",
            #"    /azureus:           Muestra la informacion de Azureus",
            #""]
        #else:
            #mensajes = [
            #"",
            #"Parametro no soportado",
            #""]
    #auxiliar.priv_imprime(mensajes)
    #return xchat.EAT_ALL


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
            total_descargado = auxiliar.unidades(int(lineas_amule[11]))
            version = lineas_amule[13][0:-1]
            parte1 = "say ( aMule %s ) Descarga: %sKB/s - Subida: %sKB/s " \
                     % (version, vdescarga, vsubida)
            parte2 = "- Total descargado: %s" % total_descargado
            xchat.command("%s%s" % (parte1, parte2))
    else:
        parte1 = "No existe el archivo %s, compruebe que activada" % _AMULESIG
        parte2 = " la firma online en la configuracion de aMule."
        auxiliar.gprint("%s%s" % (parte1, parte2))
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
        xchat.command("say ( Azureus ) Descarga: %s - Subida: %s" \
                      % (vdescarga, vsubida))
        del descarga, vdescarga, subida, vsubida, glob, stats, dom1
    else:
        parte1 = "No existe el archivo %s, compruebe su configuracion de" \
                 % _AZUREUSSTATS
        parte2 =  " Azureus."
        auxiliar.gprint("%s%s" % (parte1, parte2))
    return xchat.EAT_ALL

def transmission_cb(word, word_eol, userdata):
    """Lee el archivo stats.benc (estadisticas) de Transmission y muestra parte
    de la informacion en el canal activo.
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook (ignorado)
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    if path.exists(_TRANSMISSIONSTATS):
        textos = [[1, 3], [17, 3], [12, 3], [15, 3], [14, 3], [15, 2]]
        parte = []
        archivo = file(_TRANSMISSIONSTATS, "r")
        partes = archivo.readline().split(':')
        #print partes
        archivo.close()
        for i in range(1, len(partes)):
            parte.append(partes[i][textos[i][0]:-textos[i][1]])
        #print parte
        #print "Descargados " + parte[0] + "Bytes"
        #print "Subidos     " + parte[4] + "Bytes"
        #print "Trabajados  " + parte[2] + "Segundos"
        descargado = auxiliar.unidades(int(parte[0]))
        subido = auxiliar.unidades(int(parte[4]))
        xchat.command("say ( Transmission ) Descargado: %s - Subido: %s" \
                      % (descargado, subido))
    else:
        parte1 = "No existe el archivo %s, compruebe su " % _TRANSMISSIONSTATS
        parte2 = "configuracion de Transmission."
        auxiliar.gprint("%s%s" % (parte1, parte2))
    

#############################################################################
# Definimos la funcion para la descarga del programa
#############################################################################
def unload_cb(userdata):
    """Esta funcion debe desenlazar todas las funciones del modulo al
    descargarse el script
    Argumentos:
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    # Desconectamos los comandos
    # Peer to Peer
    xchat.unhook(HOOKAMULE)
    xchat.unhook(HOOKAZUREUS)
    xchat.unhook(HOOKTRANSMISSION)
    # Descarga
    xchat.unhook(HOOKP2P)


#############################################################################
# Conectamos los "lanzadores" de xchat con las funciones que hemos definido
# para ellos
#############################################################################
# Peer to Peer
HOOKAMULE = xchat.hook_command('amule', amule_cb)
HOOKAZUREUS = xchat.hook_command('azureus', azureus_cb)
HOOKTRANSMISSION = xchat.hook_command('transmission', transmission_cb)
# Descarga del script
HOOKP2P = xchat.hook_unload(unload_cb)


#############################################################################
# Añadimos las opciones del menu
#############################################################################
xchat.command('menu ADD "GatoScript/Descargas"')
xchat.command('menu ADD "GatoScript/Descargas/aMule" "amule"')
xchat.command('menu ADD "GatoScript/Descargas/Azureus" "azureus"')
xchat.command('menu ADD "GatoScript/Descargas/Transmission" "transmission"')
