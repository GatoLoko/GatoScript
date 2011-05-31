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
This module controls Audacious player.
"""

__module_name__ = "GatoScript MultiMedia - Audacious"
__module_description__ = "Audacious module for GatoScript"
__module_autor__ = "GatoLoko"


from os import system
from commands import getoutput

class Player:
    def name(self):
        return "Audacious"

    def listening(self):
        title = getoutput("audtool2 current-song")
        artist = getoutput("audtool2 current-song-tuple-data artist")
        length = getoutput("audtool2 current-song-length")
        return title, artist, length
        
    def previous(self):
        system("audtool2 playlist-reverse")
        
    def next(self):
        system("audtool2 playlist-advance")
        
    def pause(self):
        system("audtool2 playback-pause")
        
    def play(self):
        system("audtool2 playback-play")
        
    def stop(self):
        system("audtool2 playback-stop")

