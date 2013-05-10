# -*- coding: UTF8 -*-

# CopyRight (C) 2006-2013 GatoLoko
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
# along with GatoScript; if not, see <http://www.gnu.org/licenses/>.

"""
GatoScript's main module.
"""

__module_name__ = "GatoScript"
__module_description__ = "GatoScript for HexChat and X-Chat "
__module_autor__ = "GatoLoko"

# To interact with X-Chat/HexChat
import xchat
# To manage folders
from os.path import join
import sys

# Define environment variables
scriptdir = xchat.get_info("xchatdir")
moddir = join(scriptdir, "gatoscript")

# Incluide out modules directory in the path
sys.path.append(moddir)

xchat.command('menu -p4 ADD "GatoScript"')

# Load all the script modules
import gmodules
__module_version__ = gmodules.helper.__module_version__


def help_cb(word, word_eol, userdata):
    gmodules.helper.gprint("GatoScript help:")
    for entry in dir(gmodules):
        if "__" not in entry:
            command = ''.join(["gmodules.", entry, ".ghelp()"])
            messages = eval(command)
            for message in messages:
                gmodules.helper.gprint(message)


#############################################################################
# Script unloading function.
#############################################################################
def unload_cb(userdata):
    xchat.unhook(HOOKGHELP)
    for entry in dir(gmodules):
        if "__" not in entry:
            command = ''.join(["gmodules.", entry, ".unload()"])
            messages = eval(command)
            for message in messages:
                print(message)
    xchat.unhook(HOOKUNLOAD)
    xchat.command('menu del GatoScript')
    print("".join(["GatoScript ", __module_version__, " has been unloaded"]))


#############################################################################
# Hooks for all functions provided by this module
#############################################################################
help_usage = "Usage: ghelp, shows GatoScript help"
HOOKGHELP = xchat.hook_command("gatohelp", help_cb, help=help_usage)
HOOKUNLOAD = xchat.hook_unload(unload_cb)


# If this point is reached, it means the script has been loaded succefully, so
# we anounce it.
message = "".join(["GatoScript ", __module_version__, " has been loaded."])
gmodules.helper.gprint(message)
