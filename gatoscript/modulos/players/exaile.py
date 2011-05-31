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
This module controls Exaile.
"""

__module_name__ = "GatoScript MultiMedia - Exaile"
__module_description__ = "Exaile module for GatoScript"
__module_autor__ = "GatoLoko"


from os import system
from commands import getoutput


class Player:
    def name(self):
        return "Exaile"
    
    def listening(self):
        title = getoutput("exaile --get-title")
        artist = getoutput("exaile --get-artist")
        time = int(getoutput("exaile --get-length").split(".")[0])
        minutes = int(time/60)
        seconds = time-(minutes*60)
        length = str(minutes) + "m" + str(seconds) + "s"
        return title, artist, length
    
    def previous(self):
        system("exaile --prev")
    
    def next(self):
        system("exaile --next")
    
    def pause(self):
        system("exaile --play-pause")
    
    def play(self):
        system("exaile --play-pause")
    
    def stop(self):
        system("exaile --stop")
