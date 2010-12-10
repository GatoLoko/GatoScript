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
Modulo principal del GatoScript.

Este modulo se encarga de cargar e interconectar otras partes del GatoScript.
"""

__module_name__ = "GatoScript MultiMedia"
__module_description__ = "Modulo MultiMedia para el GatoScript"
__module_autor__ = "GatoLoko"

# Cargamos la libreria de funciones de X-Chat
import xchat
# Importamos la funcion para unir directorios de forma portable
from os.path import join
from os import popen3, system
from commands import getoutput
# Importamos el modulo de funciones auxiliares
import auxiliar


# Definimos algunas variables de entorno para poder trabajar comodamente
scriptdir = xchat.get_info("xchatdir")
gatodir = join(scriptdir, "gatoscript")
moddir = join(gatodir, "modulos")
gatoconf = join(scriptdir, "gatoscript.conf")
gatodb = join(gatodir, "gatoscript.db")


#############################################################################
# Definimos algunas variables que describen el entorno de trabajo y librerias
# opcionales.
#############################################################################

NoDBus = 0
global DBusIniciado
DBusIniciado = 0
global rbplayerobj
global rbplayer
global rbshellobj
global rbshell

#############################################################################
# Cargamos los modulos para la gestion multimedia
#############################################################################
repro_activo = auxiliar.lee_conf("media", "activo")
if (repro_activo == "1"):
    repro = auxiliar.lee_conf("media", "reproductor")
    if (repro == "rhythmbox-dbus"):
        try:
            import dbus
            DBUS_START_REPLY_SUCCESS = 1
            DBUS_START_REPLY_ALREADY_RUNNING = 2
            bus = dbus.SessionBus()
        except ImportError:
            NoDBus = 1
            auxiliar.gprint("No se pudo cargar la libreria 'dbus', no \
                            funcionaran los controles de Rhythmbox-DBUS")
    elif (repro == "banshee"):
        try:
            import dbus
        except ImportError:
            NoDBus = 1
            auxiliar.gprint("No se pudo cargar la libreria 'dbus', no \
                            funcionaran los controles de Banshee")


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
    """Muestra en el canal activo informacion sobre la cancion que estamos escuchando.
    Toma del archivo de configuracion el reproductor a usar.

    Argumentos:
    word     -- array de palabras que envia xchat a cada hook (ignorado)
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    media_activo = auxiliar.lee_conf("media", "activo")
    if (media_activo == "1"):
        reproductor = auxiliar.lee_conf("media", "reproductor")
        if (reproductor == "rhythmbox-dbus"):
            global DBusIniciado
            global rbplayerobj
            global rbplayer
            global rbshellobj
            global rbshell
            if (NoDBus == 1):
                auxiliar.gprint("No esta disponible la libreria de acceso a Rhythmbox")
            else:
                if DBusIniciado == 0:
                    bus = dbus.SessionBus()
                    rbplayerobj = bus.get_object('org.gnome.Rhythmbox', '/org/gnome/Rhythmbox/Player')
                    rbplayer = dbus.Interface(rbplayerobj, 'org.gnome.Rhythmbox.Player')
                    rbshellobj = bus.get_object('org.gnome.Rhythmbox', '/org/gnome/Rhythmbox/Shell')
                    rbshell = dbus.Interface(rbshellobj, 'org.gnome.Rhythmbox.Shell')
                    auxiliar.gprint("Conectando con Rhythmbox, por favor intentelo otra vez")
                    DBusIniciado = 1
                else:
                    try:
                        sonando = int(rbplayer.getPlaying())
                    except:
                        sonando = 0
                    if (userdata == "escuchando"):
                        if sonando == 0:
                            auxiliar.gprint("El reproductor esta parado")
                        else:
                            detalles = rbshell.getSongProperties(rbplayer.getPlayingUri())
                            #for prop in detalles:
                                #print "%s: %s" % (prop, detalles[prop])
                            titulo = detalles['title'].encode('utf-8')
                            artista = detalles['artist'].encode('utf-8')
                            #album = detalles['album'].encode('utf-8')
                            tiempo = detalles['duration']
                            if tiempo <= 0:
                                bitrate = detalles['bitrate']
                                longitud = "Radio - " + str(bitrate) + "Kbit/s"
                                #URL = rbplayer.getPlayingUri()
                                artista = detalles['rb:stream-song-title'].encode('utf-8')
                            else:
                                minutos = int(tiempo/60)
                                segundos = tiempo-(minutos*60)
                                longitud = str(minutos) + "m" + str(segundos) + "s"
                            xchat.command("me esta escuchando: %s - %s (%s) - Rhythmbox" %(artista, titulo, longitud))
                    elif (userdata == "reproductor"):
                        auxiliar.gprint("Esta utilizando Rhythmbox")
                    elif (userdata == "siguiente"):
                        if sonando == 0:
                            auxiliar.gprint("El reproductor esta parado")
                        else:
                            rbplayer.next()
                    elif (userdata == "anterior"):
                        if sonando == 0:
                            auxiliar.gprint("El reproductor esta parado")
                        else:
                            rbplayer.previous()
                    #elif (userdata == "play" or userdata == "pausa"):
                        #rbplayer.playPause()
                    #elif (userdata == "stop"):
                        #auxiliar.gprint("Esta funcion no esta implementada")
                    else:
                        mensaje = "La funcion " + userdata + " no esta implementada"
                        auxiliar.gprint(mensaje)
        # El siguiente codigo accede a rhythmbox sin necesidad de usar dbus, 
        # pero necesita una version reciente de "rhythmbox-client". Debe
        # funcionar a partir de rhythmbox 0.11.6.
        # El bugreport y el parche que envie para que proporcionase parte de la
        # informacion que usamos esta disponible en:
        # http://bugzilla.gnome.org/show_bug.cgi?id=541725
        elif reproductor == "rhythmbox":
            if userdata == "reproductor":
                auxiliar.gprint("Está utilizando Rhythmbox")
            elif userdata == "escuchando":
                duracion = getoutput('rhythmbox-client --no-present --print-playing-format %td')
                if duracion == "Desconocido":
                    duracion = "Radio"
                    # No es posible obtener el bitrate mediante rhythmbox-client, asi que he creado
                    # otro bugreport con su correspondiente parche, a ver si tambien lo aceptan:
                    # http://bugzilla.gnome.org/show_bug.cgi?id=545930
                    informacion = getoutput('rhythmbox-client --no-present --print-playing-format "%st - %tt (%tb kbits/s)"')
                    # Mientras no este disponible el bitrate, continuamos sin el.
                    # Las emisoras de radio unen el grupo y el titulo en el campo %st y meten el nombre de la emisora en %tt
                    #informacion = getoutput('rhythmbox-client --no-present --print-playing-format "%st - %tt"')
                else:
                    # En etiquetas id3, %ta representa al artista/grupo y %tt al titulo
                    informacion = getoutput('rhythmbox-client --no-present --print-playing-format "%ta - %tt"')
                xchat.command("me esta escuchando: %s (%s) - Rhythmbox" %(informacion, duracion))
                #xchat.command("me esta escuchando: %s (%s) - Rhythmbox" %(informacion.split("\n")[2], duracion.split("\n")[2]) )
            elif userdata == "anterior":
                system("rhythmbox-client --previous")
            elif userdata == "siguiente":
                system("rhythmbox-client --next")
            elif userdata == "pausa":
                system("rhythmbox-client --pause")
            elif userdata == "play":
                system("rhythmbox-client --play")
            elif userdata == "stop":
                system("rhythmbox-client --stop")
            else:
                auxiliar.gprint("Funcion no soportada")
        elif reproductor == "banshee":
            if userdata == "reproductor":
                auxiliar.gprint("Está utilizando Banshee")
            elif userdata == "escuchando":
                informacion = (getoutput('banshee --query-artist --query-title --query-duration')).split("\n")
                tiempo = int(informacion[0].split(": ")[1])
                minutos = int(tiempo/60)
                segundos = tiempo-(minutos*60)
                duracion = str(minutos) + "m" + str(segundos) + "s"
                #duracion = segundos
                titulo = informacion[1].split(": ")[1]
                artista = informacion[2].split(": ")[1]
                xchat.command("me está escuchando: %s - %s (%s) - Banshee" %(artista, titulo, duracion))
            elif userdata == "anterior":
                system("banshee --previous")
            elif userdata == "siguiente":
                system("banshee --next")
            elif userdata == "pausa":
                system("banshee --pause")
            elif userdata == "play":
                system("banshee --play")
            elif userdata == "stop":
                system("banshee --pause")
            else:
                auxiliar.gprint("Funcion no soportada")
        elif reproductor == "amarok":
            if userdata == "reproductor":
                auxiliar.gprint("Está utilizando Amarok")
            elif userdata == "escuchando":
                duracion = getoutput("dcop amarok player totalTime")
                titulo = getoutput("dcop amarok player title")
                artista = getoutput("dcop amarok player artist")
                xchat.command("me esta escuchando: %s - %s (%s) - Amarok" %(artista, titulo, duracion))
            elif userdata == "anterior":
                system("dcop amarok player prev")
            elif userdata == "siguiente":
                system("dcop amarok player next")
            elif userdata == "pausa":
                system("dcop amarok player pause")
            elif userdata == "play":
                system("dcop amarok player play")
            elif userdata == "stop":
                system("dcop amarok player stop")
            else:
                auxiliar.gprint("Funcion no soportada")
        elif reproductor == "exaile":
            if userdata == "reproductor":
                auxiliar.gprint("Está utilizando Exaile")
            elif userdata == "escuchando":
                tiempo = int(getoutput("exaile --get-length").split(".")[0])
                minutos = int(tiempo/60)
                segundos = tiempo-(minutos*60)
                duracion = str(minutos) + "m" + str(segundos) + "s"
                titulo = getoutput("exaile --get-title")
                artista = getoutput("exaile --get-artist")
                xchat.command("me esta escuchando: %s - %s (%s) - Exaile" %(artista, titulo, duracion))
            elif userdata == "anterior":
                system("exaile --prev")
            elif userdata == "siguiente":
                system("exaile --next")
            elif userdata == "pausa":
                system("exaile --play-pause")
            elif userdata == "play":
                system("exaile --play-pause")
            elif userdata == "stop":
                system("exaile --stop")
            else:
                auxiliar.gprint("Funcion no soportada")
        elif reproductor == "audacious":
            if userdata == "reproductor":
                auxiliar.gprint("Está utilizando Audacious")
            elif userdata == "escuchando":
                duracion = getoutput("audtool2 current-song-length")
                titulo = getoutput("audtool2 current-song")
                artista = getoutput("audtool2 current-song-tuple-data artist")
                xchat.command("me esta escuchando: %s - %s (%s) - Audacious" %(artista, titulo, duracion))
            elif userdata == "anterior":
                system("audtool2 playlist-reverse")
            elif userdata == "siguiente":
                system("audtool2 playlist-advance")
            elif userdata == "pausa":
                system("audtool2 playback-pause")
            elif userdata == "play":
                system("audtool2 playback-play")
            elif userdata == "stop":
                system("audtool2 playback-stop")
            else:
                auxiliar.gprint("Funcion no soportada")
    else:
        auxiliar.gprint("Los controles multimedia estan desactivados")
    return xchat.EAT_ALL


#############################################################################
# Definimos la funcion para la descarga del programa
#############################################################################
def unload_cb(userdata):
    """Esta funcion debe desenlazar todas las funciones del GatoScript al descargarse el script
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
hookescuchando = xchat.hook_command('escuchando', media_cb, userdata="escuchando")
hookreproductor = xchat.hook_command('reproductor', media_cb, userdata="reproductor")
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
xchat.command('menu ADD "GatoScript/Multimedia"')
xchat.command('menu ADD "GatoScript/Multimedia/Cancion actual" "escuchando"')
xchat.command('menu ADD "GatoScript/Multimedia/Reproductor" "reproductor"')
xchat.command('menu ADD "GatoScript/Multimedia/Anterior" "anterior"')
xchat.command('menu ADD "GatoScript/Multimedia/Siguiente" "siguiente"')
xchat.command('menu ADD "GatoScript/Multimedia/Stop" "stop"')
xchat.command('menu ADD "GatoScript/Multimedia/Play" "play"')
