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
This module controls Amarok player.
"""

__module_name__ = "GatoScript MultiMedia - Amarok"
__module_description__ = "Amarok control for GatoScript"
__module_autor__ = "GatoLoko"


from os import system
from commands import getoutput


class Player:
    """Amarok player main class"""
    def name(self):
        """Returns the player name"""
        return "Amarok"
    
    def listening(self):
        """Returns information from the currently playing song"""
        title = getoutput("dcop amarok player title")
        artist = getoutput("dcop amarok player artist")
        length = getoutput("dcop amarok player totalTime")
        return title, artist, length
    
    def previous(self):
        """Jumps to the previous song in the playlist"""
        system("dcop amarok player prev")
        
    def next(self):
        """Jumps to the next song in the playlist"""
        system("dcop amarok player next")
        
    def pause(self):
        """Pauses the media player"""
        system("dcop amarok player pause")
        
    def play(self):
        """Plays the current song in the playlist"""
        system("dcop amarok player play")
        
    def stop(self):
        """Stops the media player"""
        system("dcop amarok player stop")
