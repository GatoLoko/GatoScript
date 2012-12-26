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
This module controls Rhythmbox.
"""

__module_name__ = "GatoScript MultiMedia - Rhythmbox"
__module_description__ = "Rhythmbox module for GatoScript"
__module_autor__ = "GatoLoko"


from os import system
from commands import getoutput


# The following code access rhythmbx without using dbus, but this needs a
# recent release of "rhythmbox-client". It must work since rhythmbox 0.11.6.
# The bugreport and patch I sent to make it provide part of the information we
# use is available at: http://bugzilla.gnome.org/show_bug.cgi?id=541725
class Player:
    def name(self):
        return "Rhythmbox"

    def listening(self):
        # %st means "stream title" in files, in most radios means artist + title
        # %tt means "track title" in files, in most radios means radio name
        # %ta means "track artist", nonexistent on most radios
        # %td means "track duration", "Unknown" on radios

        length = getoutput('rhythmbox-client --no-present --print-playing-format %td')
        if length == "Desconocido" or length == "Unknown":
            title = getoutput('rhythmbox-client --no-present --print-playing-format "%st"')
            artist = getoutput('rhythmbox-client --no-present --print-playing-format "%tt"')
            # It wasn't possible to get the bitrate through rhythmbox-client, so
            # I created another bugreport with it corresponding patch. It must
            # work with recent releases. The bugreport and patch are availables
            # at: http://bugzilla.gnome.org/show_bug.cgi?id=545930
            length = getoutput('rhythmbox-client --no-present --print-playing-format "%tbKb/s - Radio"')
        else:
            title = getoutput('rhythmbox-client --no-present --print-playing-format "%tt"')
            artist = getoutput('rhythmbox-client --no-present --print-playing-format "%ta"')
        return title, artist, length

    def previous(self):
        system("rhythmbox-client --previous")

    def next(self):
        system("rhythmbox-client --next")

    def pause(self):
        system("rhythmbox-client --pause")

    def play(self):
        system("rhythmbox-client --play")

    def stop(self):
        system("rhythmbox-client --stop")
