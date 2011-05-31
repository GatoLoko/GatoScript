#!/usr/bin/python
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
Modulo principal del GatoScript.

Este modulo se encarga de cargar e interconectar otras partes del GatoScript.
"""

__module_name__ = "GatoScript MultiMedia"
__module_description__ = "Modulo MultiMedia para el GatoScript"
__module_autor__ = "GatoLoko"


try:
    import dbus
    DBUS_START_REPLY_SUCCESS = 1
    DBUS_START_REPLY_ALREADY_RUNNING = 2
except:
    NoDBus = 1


#############################################################################
# Definimos algunas variables que describen el entorno de trabajo y librerias
# opcionales.
#############################################################################

class Player:
    def __init__(self):
        self.bus = dbus.SessionBus()
        self.rbplayerobj = bus.get_object('org.gnome.Rhythmbox', '/org/gnome/Rhythmbox/Player')
        self.rbplayer = dbus.Interface(rbplayerobj, 'org.gnome.Rhythmbox.Player')
        self.rbshellobj = bus.get_object('org.gnome.Rhythmbox', '/org/gnome/Rhythmbox/Shell')
        self.rbshell = dbus.Interface(rbshellobj, 'org.gnome.Rhythmbox.Shell')
    
    def name(self):
        return "Rhythmbox"
    
    def listening(self):
        if int(self.rbplayer.getPlaying()):
            data = rbshell.getSongProperties(rbplayer.getPlayingUri())
            title = data['title']
            artist = data['artist']
            time = date['duration']
            if time <= 0:
                bitrate = data['bitrate']
                length = "%sKb/s - Radio" % str(bitrate)
                artist = data['rb:stram-song-title']
            else:
                minutes = int(time/60)
                seconds = time-(minutes*60)
                length = "%sm%ss" %(munites, seconds)
            return title, artist, length
    
    def previous(self):
        if int(self.rbplayer.getPlaying()):
            self.rbplayer.previous()
    
    def next(self):
        if int(self.rbplayer.getPlaying()):
            self.rbplayer.next()
    
    def pause(self):
        self.rbplayer.playPause()
    
    def play(self):
        self.rbplayer.playPause()
    
    def stop(self):
        self.rbplayer.stop()
                    
