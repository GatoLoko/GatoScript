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

# Load all needed libraries
import hexchat
import sys
from . import helper


gatodirs = helper.scriptdirs()
# Include our module's directory in the path
sys.path.append(gatodirs[3])


#############################################################################
# Load the module for the active player
#############################################################################
player_enabled = int(helper.conf_read("enabled", "media"))
if player_enabled:
    player_module = __import__(helper.conf_read("player", "media"))
    player = player_module.Player()


##############################################################################
# Define the help function
##############################################################################
def ghelp():
    """Returns the help information."""
    messages = [
        "Multimedia:",
        "".join(
            ["    /hearing:       Shows in the active channel the song we",
             " are hearing currently playing"]),
        "    /player:        Shows the chosen player",
        "    /next:          Jumps to the next song",
        "    /prev:          Jumps to the previous song",
        "    /pause:         Pauses the music",
        "    /play:          Plays the music",
        "    /stop:          Stops the music",
        ""]
    return messages


##############################################################################
# Define functions for multimedia control
##############################################################################
def media_cb(word, word_eol, userdata):
    """Shows in the active channel information about the song we are hearing.
    Gets from the settings file the player to use.

    Arguments:
    word     -- array of words sent by HexChat/X-chat to every hook (ignored)
    word_eol -- array of strings sent by HexChat/X-chat to every hook (ignored)
    userdata -- optional variable sent to a hook. Here we get what to do.
    """
    if userdata == "hearing":
        title, artist, songlength = player.listening()
        command = "me is hearing: {0} - {1} ({2})".format(title, artist,
                                                          songlength)
        hexchat.command(command)
    elif userdata == "player":
        print("The selected media player is {0}".format(player.name()))
    elif userdata == "next":
        player.next()
    elif userdata == "previous":
        player.previous()
    elif userdata == "play":
        player.play()
    elif userdata == "pause":
        player.pause()
    elif userdata == "stop":
        player.stop()
    else:
        message = "The {0} function is not implemented".format(userdata)
        helper.gprint(message)
    return hexchat.EAT_ALL


#############################################################################
# Define the function to unload this module. This should be called from the
# main module unload function
#############################################################################
def unload():
    """This function disconnects all module functions"""
    hexchat.unhook(hookhearing)
    hexchat.unhook(hookplayer)
    hexchat.unhook(hooknext)
    hexchat.unhook(hookprevious)
    hexchat.unhook(hookplay)
    hexchat.unhook(hookpause)
    hexchat.unhook(hookstop)
    hexchat.command('menu del "GatoScript/Options/Multimedia"')
    hexchat.command('menu del "GatoScript/Options/Player"')
    hexchat.command('menu del "GatoScript/Multimedia"')


#############################################################################
# Hook all callbacks with their respective commands
#############################################################################
# Media
hookhearing = hexchat.hook_command('hearing', media_cb,
                                   userdata="hearing")
hookplayer = hexchat.hook_command('player', media_cb,
                                  userdata="player")
hooknext = hexchat.hook_command('next', media_cb, userdata="next")
hookprevious = hexchat.hook_command('previous', media_cb, userdata="previous")
hookplay = hexchat.hook_command('play', media_cb, userdata="play")
hookpause = hexchat.hook_command('pause', media_cb, userdata="pause")
hookstop = hexchat.hook_command('stop', media_cb, userdata="stop")


#############################################################################
# Add menu options
#############################################################################
hexchat.command("".join(['menu -t1 ADD "GatoScript/Options/Multimedia"',
                         ' "options media enabled 1"',
                         ' "options media enabled 0"']))
hexchat.command('menu ADD "GatoScript/Options/Player"')
hexchat.command("".join(['menu ADD "GatoScript/Option/Player/Rhythmbox"',
                         ' "options media player rhythmbox"']))
hexchat.command("".join(['menu ADD "GatoScript/Option/Player/Banshee"',
                         ' "options media player banshee"']))
hexchat.command("".join(['menu ADD "GatoScript/Option/Player/Amarok"',
                         ' "options media player amarok"']))
hexchat.command("".join(['menu ADD "GatoScript/Option/Player/Exaile"',
                         ' "options media player exaile"']))
hexchat.command("".join(['menu ADD "GatoScript/Option/Player/Audacious"',
                         ' "options media player audacious"']))
hexchat.command("".join(['menu ADD "GatoScript/Option/Player/gmusicbrowser"',
                         ' "options media player gmusicbrowser"']))
hexchat.command('menu ADD "GatoScript/Multimedia"')
hexchat.command('menu ADD "GatoScript/Multimedia/Current song" "hearing"')
hexchat.command('menu ADD "GatoScript/Multimedia/Player" "player"')
hexchat.command('menu ADD "GatoScript/Multimedia/Previous" "previous"')
hexchat.command('menu ADD "GatoScript/Multimedia/Next" "next"')
hexchat.command('menu ADD "GatoScript/Multimedia/Stop" "stop"')
hexchat.command('menu ADD "GatoScript/Multimedia/Play" "play"')
