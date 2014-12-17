# -*- coding: UTF8 -*-

# CopyRight (C) 2006-2014 GatoLoko
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
WhoIs module for GatoScript.

This module contains functions to intercept and rewrite whois answers and
redirect them to the active channel, and is part of GatoScript.
"""

__module_name__ = "GatoScript WhoIs"
__module_description__ = "WhoIs module for GatoScript"
__module_autor__ = "GatoLoko"

# Load all needed libraries
import xchat
from . import helper

#############################################################################
# Define some environment variables
#############################################################################


#############################################################################
# Define internal use functions
#############################################################################


#############################################################################
# Define functions for whois formating and redirection
#############################################################################
def whois_cb(word, word_eol, userdata):
    """Redirects all whois responses to the active channel and reformats the
    output.
    Arguments:
    word     -- array of strings sent by HexChat/X-Chat to every hook
    word_eol -- array of strings sent by HexChat/X-Chat to every hook
    userdata -- optional variable that can be sent to a hook (ignored)
    """
    color = "3"
    start = "\003{0}[".format(color)
    end = "]\003 "
    min_width = 16
    if helper.conf_read("whois", "common") == "1":
        if (word[1] == "301"):
            # WhoIs reply: AwayMessage
            string = "Away message".ljust(min_width)
            print("{0}{1}{2}{3}".format(start, string, end, word_eol[4][1:]))
        elif (word[1] == "307"):
            # WhoIs reply: RegNick
            string = word[3].ljust(min_width)
            print("{0}{1}{2}{3}".format(start, string, end, word_eol[4][1:]))
        elif (word[1] == "310"):
            # WhoIs reply: Service Operator
            string = word[3].ljust(min_width)
            print("{0}{1}{2}{3}".format(start, string, end, word_eol[4][1:]))
        elif (word[1] == "311"):
            # WhoIs reply: User
            nick = word[3]
            host = "{0}@{1}".format(word[4], word[5])
            name = word_eol[7][1:]
            string = "Nick".ljust(min_width)
            print("{0}{1}{2}{3}".format(start, string, end, nick))
            string = "Address".ljust(min_width)
            print("{0}{1}{2}{3}".format(start, string, end, host))
            string = "Real name".ljust(min_width)
            print("{0}{1}{2}{3}".format(start, string, end, name))
        elif (word[1] == "312"):
            # WhoIs reply: Server
            string = "Server".ljust(min_width)
            print("{0}{1}{2}{3}".format(start, string, end, word_eol[4]))
        elif (word[1] == "313"):
            # WhoIs reply: IrcOp
            string = word[3].ljust(min_width)
            print("{0}{1}{2}{3}".format(start, string, end, word_eol[4]))
        elif (word[1] == "316"):
            # WhoIs reply: Network Bot
            string = word[3].ljust(min_width)
            print("{0}{1}{2}{3}".format(start, string, end, word_eol[4]))
        elif (word[1] == "317"):
            # WhoIs reply: IDLE
            hours = int(word[4]) / 3600
            minutes = (int(word[4]) - hours * 3600) / 60
            seconds = int(word[4]) - ((hours * 3600) + (minutes * 60))
            time = ''.join([str(hours), " hours, ", str(minutes), " minutes",
                           " and ", str(seconds), " seconds"])
            string = "IDLE".ljust(min_width)
            print("{0}{1}{2}{3}".format(start, string, end, time))
        elif (word[1] == "318"):
            # WhoIs reply: End of WhoIs
            string = "End of WHOIS".ljust(min_width)
            print("{0}{1}{2}".format(start, string, end))
        elif (word[1] == "319"):
            # WhoIs reply: Channels
            string = "Channels".ljust(min_width)
            print("{0}{1}{2}{3}".format(start, string, end, word_eol[4][1:]))
        elif (word[1] == "320"):
            # WhoIs reply: Special
            string = word[3].ljust(min_width)
            print("{0}{1}{2}{3}".format(start, string, end, word_eol[4][1:]))
        elif (word[1] == "330"):
            # WhoIs reply: Logged in as
            string = "Logged in as".ljust(min_width)
            print("{0}{1}{2}{3}".format(start, string, end, word[4]))
        elif (word[1] == "335"):
            # WhoIs reply: Bot
            print('\0033{0}\003'.format(word_eol[0]))
        elif (word[1] == "337"):
            string = word[3].ljust(min_width)
            print('{0}{1}{2}{3}'.format(start, string, end, word_eol[4][1:]))
        elif (word[1] == "338"):
            # WhoIs reply: user@host, ip
            string = "User@host".ljust(min_width)
            print("{0}{1}{2}{3}".format(start, string, end, word[4]))
            string = "IP".ljust(min_width)
            print("{0}{1}{2}{3}".format(start, string, end, word[5]))
        elif (word[1] == "342"):
            # WhoIs reply in ChatHispano:
            # Only accepts querys from registered users
            string = word[3].ljust(min_width)
            print("{0}{1}{2}{3}".format(start, string, end, word_eol[4][1:]))
        elif (word[1] == "378"):
            # WhoIs reply: VHOST
            string = "VHost".ljust(min_width)
            print("{0}{1}{2}{3}".format(start, string, end, word_eol[6]))
        elif (word[1] == "379"):
            # WhoIs reply: whoismodes
            string = "Modes".ljust(min_width)
            print("{0}{1}{2}{3}".format(start, string, end, word_eol[4][1:]))
        elif (word[1] == "401"):
            # WhoIs reply: No such nick
            part1 = '\0033Nick {0} doesn\'t exist'.format(word[3])
            part2 = 'or isn\'t connected.\003'
            print('{0}{1}'.format(part1, part2))
        elif (word[1] == "671"):
            string = word[3].ljust(min_width)
            print('{0}{1}{2}{3}'.format(start, string, end, word_eol[4][1:]))
        else:
            # Undefined Raw
            print(''.join(["\0033Unknown reply in whois: ", word_eol[1]]))
        return xchat.EAT_ALL
    else:
        return xchat.EAT_NONE


#############################################################################
# Define the function to unload this module. This should be called from the
# main module unload function
#############################################################################
def unload():
    """This function disconects all module functions"""
    xchat.unhook(_RAW301)
    xchat.unhook(_RAW307)
    xchat.unhook(_RAW310)
    xchat.unhook(_RAW311)
    xchat.unhook(_RAW312)
    xchat.unhook(_RAW313)
    xchat.unhook(_RAW316)
    xchat.unhook(_RAW317)
    xchat.unhook(_RAW318)
    xchat.unhook(_RAW319)
    xchat.unhook(_RAW320)
    xchat.unhook(_RAW330)
    xchat.unhook(_RAW335)
    xchat.unhook(_RAW337)
    xchat.unhook(_RAW338)
    xchat.unhook(_RAW342)
    xchat.unhook(_RAW378)
    xchat.unhook(_RAW379)
    xchat.unhook(_RAW401)
    xchat.unhook(_RAW671)


#############################################################################
# Hook all callbacks with their respective commands
#############################################################################
# AWAY message (RFC1459)
_RAW301 = xchat.hook_server('301', whois_cb, userdata=None, priority=10)
# whoisregnick (Unreal)
_RAW307 = xchat.hook_server('307', whois_cb, userdata=None, priority=10)
# whoishelpop (Unreal)
_RAW310 = xchat.hook_server('310', whois_cb, userdata=None, priority=10)
# whoisuser (RFC1459)
_RAW311 = xchat.hook_server('311', whois_cb, userdata=None, priority=10)
# whoisserver (RFC1459)
_RAW312 = xchat.hook_server('312', whois_cb, userdata=None, priority=10)
# whoisoperator (RFC1459)
_RAW313 = xchat.hook_server('313', whois_cb, userdata=None, priority=10)
# whoischanop (RFC1459)
_RAW316 = xchat.hook_server('316', whois_cb, userdata=None, priority=10)
# whoisidle (RFC1459)
_RAW317 = xchat.hook_server('317', whois_cb, userdata=None, priority=10)
# endofwhois (RFC1459)
_RAW318 = xchat.hook_server('318', whois_cb, userdata=None, priority=10)
# whoischannels (RFC1459)
_RAW319 = xchat.hook_server('319', whois_cb, userdata=None, priority=10)
# whoisspecial (Unreal)
_RAW320 = xchat.hook_server('320', whois_cb, userdata=None, priority=10)
# whoisaccount (logged in as) (IRCU)
_RAW330 = xchat.hook_server('330', whois_cb, userdata=None, priority=10)
# whoisbot (Unreal)
_RAW335 = xchat.hook_server('335', whois_cb, userdata=None, priority=10)
# SSL
_RAW337 = xchat.hook_server('337', whois_cb, userdata=None, priority=10)
# whoisactually (user@host, ip) (Unreal)
_RAW338 = xchat.hook_server('338', whois_cb, userdata=None, priority=10)
# Only accepts querys from registered users
_RAW342 = xchat.hook_server('342', whois_cb, userdata=None, priority=10)
# whoishost (virtual host) (Unreal)
_RAW378 = xchat.hook_server('378', whois_cb, userdata=None, priority=10)
# whoismodes (Unreal)
_RAW379 = xchat.hook_server('379', whois_cb, userdata=None, priority=10)
# No such nick (RFC1459)
_RAW401 = xchat.hook_server('401', whois_cb, userdata=None, priority=10)
# whoissecure (Using SSL) (KineIRCd, ircd-seven)
_RAW671 = xchat.hook_server('671', whois_cb, userdata=None, priority=10)
