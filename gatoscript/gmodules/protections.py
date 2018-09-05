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
Protections module for GatoScript.

This module contains protections functions for GatoScript
"""

__module_name__ = "GatoScript Protections"
__module_description__ = "Protections module for GatoScript"
__module_autor__ = "GatoLoko"

# Load all needed libraries
import hexchat
import re
from . import helper

#############################################################################
# Define some environment variables
#############################################################################
_HOSTS_ABUSING_CAPS = []
_HOSTS_ABUSING_COLORS = []
# Compile some regular expresion once to use them many times
_COLORS_RE = re.compile("".join(['\\x02|\\x16|\\x1f|\\x03(([0-9]{1,2})?',
                                 '(,[0-9]{1,2})?)?']))
_DRONE_RE = re.compile("^[a-z]{4,}_[a-z]{1,2}$", re.IGNORECASE)
_CTCP_RE = re.compile("\.*\", re.IGNORECASE)
_ACTION_RE = re.compile('^[\+,-]?\ACTION')

##############################################################################
# Define internal use functions
##############################################################################


##############################################################################
# Define protection functions
##############################################################################
def anti_ctcp_cb(word, word_eol, userdata):
    """Detect CTCPs sent to protected channels and kick/ban the author.
    Arguments:
    word     -- array of strings sent by HexChat/X-Chat to every hook
    word_eol -- array of strings sent by HexChat/X-Chat to every hook (ignored)
    userdata -- optional variable that can be sent to a hook (ignored)
    """
    if helper.conf_read("ctcps", "protections") == "1":
        channels = helper.conf_read("channels", "protections").split(',')
        for channel in channels:
            if channel.lower() == word[2].lower():
                if _CTCP_RE.search(word[3]):
                    message = "".join(["Received a CTCP to channel ", word[2]])
                    helper.gprint(message)
                    host = word[0][1:].split("@")[-1]
                    hexchat.command("".join(["ban *!*@", host]))
                    nick = word[0][1:].split("!")[0]
                    hexchat.command("".join(["kick ", nick,
                                             "CTCPs to channel"]))
    return hexchat.EAT_NONE


def anti_notice_cb(word, word_eol, userdata):
    """Detects NOTICEs sent to protected channels and kick/ban the author.
    Arguments:
    word     -- array of strings sent by HexChat/X-Chat to every hook
    word_eol -- array of strings sent by HexChat/X-Chat to every hook (ignored)
    userdata -- optional variable that can be sent to a hook (ignored)
    """
    # >> :Anti_Bots!GatoBot@BvW8Qj.CtqRtH.virtual NOTICE #gatoscript :hello
    # >> :CHaN!-@- NOTICE #canal :nick añade en #canal a nick2 con nivel 499
    if helper.conf_read("notices", "protections") == "1":
        channels = helper.conf_read("channels", "protections").split(',')
        for channel in channels:
            if (word[2].lower() == channel.lower()) and \
               (word[0].lower() != ":chan!-@-"):  # Exception for IRC-Hispano
                print(word[0])
                print("This ban is for sending notices")
                hexchat.command("".join(["kickban ", word[0][1:].split("!")[0],
                                       " Notices to channel are NOT allowed"]))
    return hexchat.EAT_NONE


def anti_hoygan_cb(word, word_eol, userdata):
    """Detects messages containing the word "hoygan" on protected channels and
    bans the author.
    Arguments:
    word     -- array of strings sent by HexChat/X-Chat to every hook
    word_eol -- array of strings sent by HexChat/X-Chat to every hook (ignored)
    userdata -- optional variable that can be sent to a hook (ignored)
    """
    # >> :nick!ident@host PRIVMSG #channel :message
    if helper.conf_read("hoygan", "protections") == "1":
        for channel in helper.conf_read("channels", "protections").split(','):
            if channel.lower() == word[2].lower():
                hoygan_re = re.compile('hoyga|h 0 y g 4 n', re.IGNORECASE)
                if hoygan_re.search(word_eol[3]):
                    host = word[0][1:].split("@")[-1]
                    hexchat.command("".join(["ban *!*@", host]))
                    nick = word[0][1:].split("!")[0]
                    hexchat.command("".join(["kick ", nick, " Hoygan are the",
                                           " electronic version of the class",
                                           " clown, and they are NOT funny."]))
                    del host, nick
    return hexchat.EAT_NONE


def anti_caps_cb(word, word_eol, userdata):
    """Detects caps abuse in protected channels, warns the user the first time
    and expels repeat offenders
    Arguments:
    word     -- array of strings sent by HexChat/X-Chat to every hook
    word_eol -- array of strings sent by HexChat/X-Chat to every hook
    userdata -- optional variable that can be sent to a hook (ignored)
    """
    if helper.conf_read("caps", "protections") == "1":
        for channel in helper.conf_read("channels", "protections").split(','):
            if channel.lower() == word[2].lower():
                string = word_eol[3][1:]
                if _ACTION_RE.match(string):
                    string = string[7:]
                if string.isupper() and len(string) > 10:
                    host = word[0][1:].split("@")[1]
                    nick = word[0][1:].split("!")[0]
                    if host in _HOSTS_ABUSING_CAPS:
                        _HOSTS_ABUSING_CAPS.remove(host)
                        message = "".join([" Writing in all caps is against",
                                           " the rules and you were warned."])
                        helper.expel(message, "1", word)
                    else:
                        _HOSTS_ABUSING_CAPS.append(host)
                        message = "".join(["msg ", word[2], " ", nick, ":",
                                           " do not write in all caps, it is",
                                           " against the rules. Next time you",
                                           " will be expelled."])
                    hexchat.command(message)
    return hexchat.EAT_NONE


def anti_colors_cb(word, word_eol, userdata):
    """Detects messages containing colors/bold/underline on protected channels,
    warns the author the first time and expels repeat ofenders.
    Arguments:
    word     -- array of strings sent by HexChat/X-Chat to every hook
    word_eol -- array of strings sent by HexChat/X-Chat to every hook
    userdata -- optional variable that can be sent to a hook (ignored)
    """
    # Only act on protected channels
    if word[2].lower() in helper.conf_read("channels",
                                           "protections").split(","):
        string = word_eol[3][1:]
        if _ACTION_RE.match(string):
            string = string[7:]
        if _COLORS_RE.search(string):
            # If we are banning colors, expel the author
            if helper.conf_read("ban_colors", "protections") == "1":
                host = word[0][1:].split("@")[1]
                if host in _HOSTS_ABUSING_COLORS:
                    _HOSTS_ABUSING_COLORS.remove(host)
                    message = "".join([" Using colors is against the",
                                       " rules and you were warned."])
                    helper.expel(message, "1", word)
                else:
                    _HOSTS_ABUSING_COLORS.append(host)
                    message = "".join(["msg ", word[2], " ",
                                       word[0][1:].split("!")[0], ": do NOT",
                                       " use colors/bold/underline in",
                                       " this channel, it is against the",
                                       " rules. Next time you will be",
                                       " expelled."])
                    hexchat.command(message)
            # If we are ignoring messages containing colors
            if helper.conf_read("ignore_colors", "protections") == "1":
                helper.gprint("".join(["Message from ",
                                       word[0][1:].split("!")[0],
                                       " ignored because it contains",
                                       " colors."]))
                return hexchat.EAT_ALL
    return hexchat.EAT_NONE


def anti_drone_cb(word, word_eol, userdata):
    """Detects users joining the channel with nick/indent matching those used
    by Drone and expels them before they can spam us.
    Arguments:
    word     -- array of strings sent by HexChat/X-Chat to every hook
    word_eol -- array of strings sent by HexChat/X-Chat to every hook (ignored)
    userdata -- optional variable that can be sent to a hook (ignored)
    """
    # print word_eol[0]
    if helper.conf_read("drones", "protections") == "1":
        nick = word[0][1:].split("!")[0]
        ident = word[0][1:].split("!")[1].split("@")[0]
        if _DRONE_RE.search(nick) and _DRONE_RE.search(ident):
            context = hexchat.get_context()
            host = word[0].split("@")[1]
            context.command("".join(["ban *!*@", host]))
            context.command("".join(["kick ", nick, " Bot"]))
    return hexchat.EAT_NONE


def anti_away_cb(word, word_eol, userdata):
    """Detects away messages in protected channels and expels the author
    Arguments:
    word     -- array of strings sent by HexChat/X-Chat to every hook
    word_eol -- array of strings sent by HexChat/X-Chat to every hook (ignored)
    userdata -- optional variable that can be sent to a hook (ignored)
    """
    if helper.conf_read("away", "protections") == "1":
        if word[2].lower() in helper.conf_read("channels",
                                               "protections").split(','):
            awaystr = helper.conf_read("awaystr", "protections").split(",")
            for i in range(len(awaystr)):
                if word_eol[3].find(awaystr[i]) > 0:
                    ban = "1"
                    message = "".join([" Disable automatic away messages,",
                                       " if you are out, just shut up"])
                    helper.expel(message, ban, word)
    return hexchat.EAT_NONE


##############################################################################
# Define the help function
##############################################################################
def ghelp():
    """This module doesn't provide any interactive command"""
    return []


##############################################################################
# Define the function to unload this module. This should be called from the
# main module unload function
##############################################################################
def unload():
    """This function disconects all module functions"""
    hexchat.unhook(HOOKANTINOTICE)
    hexchat.unhook(HOOKANTIDRONE)
    hexchat.unhook(HOOKANTICTCP)
    hexchat.unhook(HOOKANTIHOYGAN)
    hexchat.unhook(HOOKANTICAPS)
    hexchat.unhook(HOOKANTICOLORS)
    hexchat.unhook(HOOKANTIAWAY)


##############################################################################
# Hook all callbacks with their respective commands
##############################################################################
HOOKANTINOTICE = hexchat.hook_server('NOTICE', anti_notice_cb, userdata=None)
HOOKANTIDRONE = hexchat.hook_server('JOIN', anti_drone_cb, userdata=None)
HOOKANTICTCP = hexchat.hook_server('PRIVMSG', anti_ctcp_cb, userdata=None)
HOOKANTIHOYGAN = hexchat.hook_server('PRIVMSG', anti_hoygan_cb, userdata=None)
HOOKANTICAPS = hexchat.hook_server('PRIVMSG', anti_caps_cb, userdata=None)
HOOKANTICOLORS = hexchat.hook_server('PRIVMSG', anti_colors_cb, userdata=None)
HOOKANTIAWAY = hexchat.hook_server('PRIVMSG', anti_away_cb, userdata=None)


#############################################################################
# Add menu options
#############################################################################
hexchat.command('menu ADD "GatoScript/Options/Protections"')
hexchat.command("".join(['menu -t', helper.conf_read("away", "protections"),
                       ' ADD "GatoScript/Options/Protections/Away"',
                       ' "options protections away 1"',
                       ' "options protections away 0"']))
hexchat.command("".join(['menu -t', helper.conf_read("ban", "protections"),
                       ' ADD "GatoScript/Options/Protections/Ban"',
                       ' "options protections ban 1"',
                       ' "options protections ban 0"']))
hexchat.command("".join(['menu -t',
                       helper.conf_read("ignore_colors", "protections"),
                       ' ADD "GatoScript/Options/Protections/Ignore colors"',
                       ' "options protections colors 1"',
                       ' "options protections colors 0"']))
hexchat.command("".join(['menu -t',
                       helper.conf_read("ban_colors", "protections"),
                       ' ADD "GatoScript/Options/Protections/Ban colors"',
                       ' "options protections colors 1"',
                       ' "options protections colors 0"']))
hexchat.command("".join(['menu -t', helper.conf_read("ctcps", "protections"),
                       ' ADD "GatoScript/Options/Protections/CTCPs"',
                       ' "options protections ctcps 1"',
                       ' "options protections ctcps 0"']))
hexchat.command("".join(['menu -t', helper.conf_read("caps", "protections"),
                       ' ADD "GatoScript/Options/Protections/Caps"',
                       ' "options protections caps 1"',
                       ' "options protections caps 0"']))
hexchat.command("".join(['menu -t', helper.conf_read("hoygan", "protections"),
                       ' ADD "GatoScript/Options/Protections/HOYGAN"',
                       ' "options protections hoygan 1"',
                       ' "options protections hoygan 0"']))
hexchat.command("".join(['menu -t', helper.conf_read("spam", "protections"),
                       ' ADD "GatoScript/Options/Protections/Spam"',
                       ' "options protections spam 1"',
                       ' "options protections spam 0"']))
