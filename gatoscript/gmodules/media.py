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
import xchat
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
        "",
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
        xchat.command(command)
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
    return xchat.EAT_ALL


#############################################################################
# Define the function to unload this module. This should be called from the
# main module unload function
#############################################################################
def unload():
    """This function disconnects all module functions"""
    xchat.unhook(hookhearing)
    xchat.unhook(hookplayer)
    xchat.unhook(hooknext)
    xchat.unhook(hookprevious)
    xchat.unhook(hookplay)
    xchat.unhook(hookpause)
    xchat.unhook(hookstop)
    xchat.command('menu del "GatoScript/Options/Multimedia"')
    xchat.command('menu del "GatoScript/Options/Player"')
    xchat.command('menu del "GatoScript/Multimedia"')


#############################################################################
# Hook all callbacks with their respective commands
#############################################################################
# Media
hookhearing = xchat.hook_command('hearing', media_cb,
                                 userdata="hearing")
hookplayer = xchat.hook_command('player', media_cb,
                                userdata="player")
hooknext = xchat.hook_command('next', media_cb, userdata="next")
hookprevious = xchat.hook_command('previous', media_cb, userdata="previous")
hookplay = xchat.hook_command('play', media_cb, userdata="play")
hookpause = xchat.hook_command('pause', media_cb, userdata="pause")
hookstop = xchat.hook_command('stop', media_cb, userdata="stop")


#############################################################################
# Add menu options
#############################################################################
xchat.command("".join(['menu -t1 ADD "GatoScript/Options/Multimedia"',
                       ' "options media enabled 1"',
                       ' "options media enabled 0"']))
xchat.command('menu ADD "GatoScript/Options/Player"')
xchat.command("".join(['menu ADD "GatoScript/Option/Player/Rhythmbox"',
                       ' "options media player rhythmbox"']))
xchat.command("".join(['menu ADD "GatoScript/Option/Player/Banshee"',
                       ' "options media player banshee"']))
xchat.command("".join(['menu ADD "GatoScript/Option/Player/Amarok"',
                       ' "options media player amarok"']))
xchat.command("".join(['menu ADD "GatoScript/Option/Player/Exaile"',
                       ' "options media player exaile"']))
xchat.command("".join(['menu ADD "GatoScript/Option/Player/Audacious"',
                       ' "options media player audacious"']))
xchat.command('menu ADD "GatoScript/Multimedia"')
xchat.command('menu ADD "GatoScript/Multimedia/Current song" "hearing"')
xchat.command('menu ADD "GatoScript/Multimedia/Player" "player"')
xchat.command('menu ADD "GatoScript/Multimedia/Previous" "previous"')
xchat.command('menu ADD "GatoScript/Multimedia/Next" "next"')
xchat.command('menu ADD "GatoScript/Multimedia/Stop" "stop"')
xchat.command('menu ADD "GatoScript/Multimedia/Play" "play"')
