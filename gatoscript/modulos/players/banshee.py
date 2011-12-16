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
This module controls Banshee.
"""

__module_name__ = "GatoScript MultiMedia - Banshee"
__module_description__ = "Banshee module for GatoScript"
__module_autor__ = "GatoLoko"


from os import system
from commands import getoutput

class Player:
    def name(self):
        return "Banshee"
    
    def listening(self):
        information = (getoutput('banshee --query-artist --query-title --query-duration')).split("\n")
        if information[2].split(": ")[1] == "":
            length = "Radio"
        else:
            try:
                time = int(information[2].split(": ")[1].split(',')[0])
            except:
                time = int(information[2].split(": ")[1].split('.')[0])
            minutes = int(time/60)
            seconds = time-(minutes*60)
            length = "{0}m{1}s".format(str(minutes), str(seconds))
        title = information[1].split(": ")[1]
        artist = information[0].split(": ")[1]
        return title, artist, length
    
    def previous(self):
        system("banshee --previous")
        
    def next(self):
        system("banshee --next")
        
    def pause(self):
        system("banshee --pause")
        
    def play(self):
        system("banshee --play")
        
    def stop(self):
        system("banshee --pause")
