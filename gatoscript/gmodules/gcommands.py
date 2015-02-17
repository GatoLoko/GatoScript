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
# along with GatoScript; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

"""
GatoInfo module for GatoScript.

This module contains informational functions about GatoScript itself.
"""

__module_name__ = "GatoScript Commands"
__module_version__ = "2.0-alpha"
__module_description__ = "Commands module for GatoScript"
__module_autor__ = "GatoLoko"

# Load all needed libraries
import xchat
from . import helper

#############################################################################
# Define some environment variables
#############################################################################

#############################################################################
# Initialize the module
#############################################################################


#############################################################################
# Define functions for GatoScript
#############################################################################
def options_cb(word, word_eol, userdata):
    """This function shows and modifies the script settings.
    Arguments:
    word     -- array of strings sent by HexChat/X-Chat to every hook
    word_eol -- array of strings sent by HexChat/X-Chat to every hook
    userdata -- optional variable that can be sent to a hook (ignored)
    """
    param_num = len(word_eol)
    if param_num == 1:
        helper.conf_show()
    # elif param_num > 1 and param_num < 4:
    elif 1 < param_num < 4:
        helper.gprint('Wrong parameters count')
        helper.gprint("".join(['Usage: OPTIONS <option> <value> <section>,',
                               ' changes GatoScripts settings. If no section',
                               ' is specified, "common" is used by default.']))
    elif param_num == 4:
        helper.conf_write(word[1], word[2], word[3])
    else:
        helper.gprint("Don't show anything")
    return xchat.EAT_ALL


def gato_info_cb(word, word_eol, userdata):
    """Shows GatoScript publicity
    Arguments:
    word     -- array of strings sent by HexChat/X-Chat to every hook
    word_eol -- array of strings sent by HexChat/X-Chat to every hook
    userdata -- optional variable that can be sent to a hook (ignored)
    """
    if 'hexchat' in helper.scriptdirs()[0]:
        client = 'HexChat'
    else:
        client = 'X-Chat'
    version = xchat.get_info('version')
    xchat.command("".join(["say ( ", client, " ) ", version,
                           " ( Script ) GatoScript ", __module_version__,
                           " python script for HexChat/X-Chat ",
                           "(http://catsskein.wordpress.com)"]))
    return xchat.EAT_ALL


def kbtemp_cb(word, word_eol, userdata):
    """Temporarily expels an user on the active channel (must be OP).
    Arguments:
    word     -- array of strings sent by HexChat/X-Chat to every hook
    word_eol -- array of strings sent by HexChat/X-Chat to every hook
    userdata -- optional variable that can be sent to a hook (ignored)
    """
    if len(word_eol) > 1:
        xchat.command("".join(["ban ", word[1], "!*@*"]))
        if len(word_eol) > 2:
            xchat.command("".join(["kick ", word[1], " Banned for 5 minutes (",
                                   word_eol[2], ")"]))
        else:
            xchat.command("".join(["kick ", word[1], " Banned for 5 minutes"]))
        xchat.command("".join(["timer -repeat 1 300 unban ", word[1], "!*@*"]))
    else:
        helper.gprint("You must specify a nick to kick/ban")
    return xchat.EAT_ALL


#############################################################################
# Define the help function
#############################################################################
def ghelp():
    """Returns the help information."""
    messages = [
        "Commands:",
        "  /KBTEMP <nick> <optional_message>: bans and kick the selected nick",
        "      from the actual channel, then activates a 5 minutes countdown,",
        "      after which the ban is removed. If a message is added, it's",
        "      used as the kick reason. (You must be channel operator)",
        "  /GINFO: shows GatoScript's spam",
        "  /OPTIONS <option> <value> <section>: changes GatoScripts settings.",
        "      If no section is specified, \"common\" is used by default."]
    return messages


#############################################################################
# Define the function to unload this module. This should be called from the
# main module unload function
#############################################################################
def unload():
    """This function disconnects all module functions"""
    # Script options
    xchat.unhook(HOOKOPTIONS)
    # Script information
    xchat.unhook(HOOKGINFO)
    # Temporary KickBan
    xchat.unhook(HOOKKBTEMP)


#############################################################################
# Connect all HexChat/X-Chat hooks with the functions defined for them
#############################################################################
# Script options
options_usage = "".join(['Usage: OPTIONS <option> <value> <section>, changes',
                         ' GatoScripts settings. If no section is specified,',
                         '"common" is used by default.'])
HOOKOPTIONS = xchat.hook_command('options', options_cb, help=options_usage)
# Script information
HOOKGINFO = xchat.hook_command('ginfo', gato_info_cb)
# Temporary KickBan
kbtemp_usage = "".join([
    'Usage: KBTEMP <nick> <optional_message>, bans and kicks the selected',
    ' nick from the actual channel, then activates a 5 minutes countdown,',
    ' after wich the ban is removed. If a message is added, it\'s used as',
    ' the kick reason. (You must be channel operator)'])
HOOKKBTEMP = xchat.hook_command('kbtemp', kbtemp_cb, help=kbtemp_usage)


#############################################################################
# Add Information and Options menus
#############################################################################
xchat.command('menu ADD "GatoScript/Information" "ginfo"')
xchat.command('menu ADD "GatoScript/-"')
xchat.command('menu ADD "GatoScript/Options"')
xchat.command('menu ADD "GatoScript/Options/Python" "py console"')
