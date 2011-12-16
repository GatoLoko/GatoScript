# -*- coding: UTF8 -*-

# CopyRight (C) 2011 GatoLoko
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
This module controls all the media modules
"""

__module_name__ = "GatoScript MultiMedia - Main"
__module_description__ = "Main MultiMedia module for GatoScript"
__module_autor__ = "GatoLoko"

# Load the X-Chat function library
import xchat
# Importamos la funcion para unir directorios de forma portable
from os import popen3, system
from commands import getoutput
import sys
# Importamos el modulo de funciones auxiliares
import auxiliar


gatodirs = auxiliar.scriptdirs()
# Incluimos el directorio de modulos en el path
sys.path.append(gatodirs[3])


#############################################################################
# Load the module for the active player
#############################################################################
repro_activo = auxiliar.lee_conf("media", "activo")
if (repro_activo == "1"):
    repro = __import__(auxiliar.lee_conf("media", "reproductor"))
    player = repro.Player()


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
        #"    -m         Comandos para informacion de reproductores Multimedia",
        #"",
        #"Por ejemplo: /gato -s",
        #""]
    #else:
        #if word[1] == "-m":
            #mensajes = [
            #"",
            #"Multimedia:",
            #"    /escuchando:         Muestra en el canal activo la cancion que se esta reproduciendo",
            #"    /reproductor:        Nos informa del reproductor seleccionado",
            #"    /siguiente:          Cambia a la cancion siguiente",
            #"    /anterior:           Cambia a la cancion anterior",
            #"    /pausa:              Pausa la reproduccion",
            #"    /play:               Reanuda la reproduccion",
            #"    /stop:               Detiene la reproduccion",
            #""]
        #else:
            #mensajes = [
            #"",
            #"Parametro no soportado",
            #""]
    #auxiliar.priv_imprime(mensajes)
    #return xchat.EAT_ALL


##############################################################################
## Definimos las funciones para el control de multimedia
##############################################################################
def media_cb(word, word_eol, userdata):
    """Muestra en el canal activo informacion sobre la cancion que estamos
    escuchando.
    Toma del archivo de configuracion el reproductor a usar.

    Argumentos:
    word     -- array de palabras que envia xchat a cada hook (ignorado)
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    if (userdata == "escuchando"):
        titulo, artista, longitud = player.listening()
        comando = "me esta escuchando: {0} - {1} ({2})".format(titulo, artista,
                                                               longitud)
        xchat.command(comando)
    elif (userdata == "reproductor"):
        print("The selected media player is {0}".format(player.name()))
    elif (userdata == "siguiente"):
        player.next()
    elif (userdata == "anterior"):
        player.previous()
    elif (userdata == "play"):
        player.play()
    elif (userdata == "pausa"):
        player.pause()
    elif (userdata == "stop"):
        player.stop()
    else:
        mensaje = "La funcion {0} no esta implementada".format(userdata)
        auxiliar.gprint(mensaje)
    return xchat.EAT_ALL


#############################################################################
# Definimos la funcion para la descarga del programa
#############################################################################
def unload_cb(userdata):
    """Esta funcion debe desenlazar todas las funciones del GatoScript al
    descargarse el script.
    
    Argumentos:
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    # Media
    xchat.unhook(hookescuchando)
    xchat.unhook(hookreproductor)
    xchat.unhook(hooksiguiente)
    xchat.unhook(hookanterior)
    xchat.unhook(hookplay)
    xchat.unhook(hookpausa)
    xchat.unhook(hookstop)
    # Descarga
    xchat.unhook(hookunload)


#############################################################################
# Conectamos los "lanzadores" de xchat con las funciones que hemos definido
# para ellos
#############################################################################
# Media
hookescuchando = xchat.hook_command('escuchando', media_cb,
                                    userdata="escuchando")
hookreproductor = xchat.hook_command('reproductor', media_cb,
                                     userdata="reproductor")
hooksiguiente = xchat.hook_command('siguiente', media_cb, userdata="siguiente")
hookanterior = xchat.hook_command('anterior', media_cb, userdata="anterior")
hookplay = xchat.hook_command('play', media_cb, userdata="play")
hookpausa = xchat.hook_command('pausa', media_cb, userdata="pausa")
hookstop = xchat.hook_command('stop', media_cb, userdata="stop")
# Descarga del script
hookunload = xchat.hook_unload(unload_cb)


#############################################################################
# Añadimos las opciones del menu
#############################################################################
xchat.command('menu -t1 ADD "GatoScript/Opciones/Multimedia" "opciones media activo 1" "opciones media activo 0"')
xchat.command('menu ADD "GatoScript/Opciones/Reproductor"')
xchat.command('menu ADD "GatoScript/Opciones/Reproductor/Rhythmbox" "opciones media reproductor rhythmbox"')
xchat.command('menu ADD "GatoScript/Opciones/Reproductor/Rhythmbox (Metodo antiguo)" "opciones media reproductor rhythmbox-dbus"')
xchat.command('menu ADD "GatoScript/Opciones/Reproductor/Banshee" "opciones media reproductor banshee"')
xchat.command('menu ADD "GatoScript/Opciones/Reproductor/Amarok" "opciones media reproductor amarok"')
xchat.command('menu ADD "GatoScript/Opciones/Reproductor/Exaile" "opciones media reproductor exaile"')
xchat.command('menu ADD "GatoScript/Opciones/Reproductor/Audacious" "opciones media reproductor audacious"')
xchat.command('menu ADD "GatoScript/Multimedia"')
xchat.command('menu ADD "GatoScript/Multimedia/Cancion actual" "escuchando"')
xchat.command('menu ADD "GatoScript/Multimedia/Reproductor" "reproductor"')
xchat.command('menu ADD "GatoScript/Multimedia/Anterior" "anterior"')
xchat.command('menu ADD "GatoScript/Multimedia/Siguiente" "siguiente"')
xchat.command('menu ADD "GatoScript/Multimedia/Stop" "stop"')
xchat.command('menu ADD "GatoScript/Multimedia/Play" "play"')
