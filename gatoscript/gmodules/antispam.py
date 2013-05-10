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
AntiSpam module for GatoScript.

This module contains antispam functions for GatoScript.
"""

__module_name__ = "GatoScript AntiSpam"
__module_description__ = "AntiSpam module for GatoScript"
__module_autor__ = "GatoLoko"

# Load all needed libraries
import xchat
import re
import helper

#############################################################################
# Define some environment variables
#############################################################################


#############################################################################
# Initialize the module
#############################################################################
# Load the filter list and compile the regular expressions
if helper.CONNECTED == 1:
    ANTISPAM = int(helper.conf_read("spam", "protections"))
    SPAMBOTS = int(helper.conf_read("spambots", "protections"))
    CHANNELS = helper.conf_read("channels", "protections").split(",")
    filters = helper.gatodb_cursor_execute("SELECT filter FROM filters")
    COMP_FILTERS = []
    for item in filters:
        COMP_FILTERS.append(re.compile("".join([".*", item[0], ".*"]),
                                       re.IGNORECASE))
else:
    helper.gprint("AntiSpam is disabled or couldn't read the filters list")
    ANTISPAM = 0
    SPAMBOTS = 0
    CHANNELS = []


#############################################################################
# Define internal use functions
#############################################################################
def antispam_reload():
    """Reload the antispam filters list to apply changes"""
    # Use the global variables so this change applies to the wole module
    global ANTISPAM
    global SPAMBOTS
    global CHANNELS
    if helper.CONNECTED == 1:
        ANTISPAM = int(helper.conf_read("spam", "protections"))
        SPAMBOTS = int(helper.conf_read("spambots", "protections"))
        CHANNELS = helper.conf_read("channels", "protections")
        # Load the new filter list and compile the regexps
        filters = helper.gatodb_cursor_execute("SELECT filter FROM filters")
        COMP_FILTERS = []
        for item in filters:
            COMP_FILTERS.append(re.compile("".join([".*", item[0], ".*"]),
                                               re.IGNORECASE))
    else:
        helper.gprint("Failed to reload filters, AntiSpam disabled")
        ANTISPAM = 0
        SPAMBOTS = 0
        CHANNELS = []


#############################################################################
# Define AntiSpam functions to filter messages.
# The AntiSpam system removes every line matching with one or more filters.
#############################################################################
def antispam_cb(word, word_eol, userdata):
    """Compare received messages with a list of filters and remove those who
    match. Also, optionally, expel the spamer.
    Arguments:
    word     -- array of strings sent by HexChat/X-Chat to every hook
    word_eol -- array of strings sent by HexChat/X-Chat to every hook (ignored)
    userdata -- optional variable that can be sent to a hook (ignored)
    """
    global SPAMBOTS
    global ANTISPAM
    global CHANNELS
    # Check whether the message was receiven on a protected channel and the
    # antispam is enabled. If so, expel the spammer
    if word[2] in CHANNELS and ANTISPAM == 1:
        for spam_exp in COMP_FILTERS:
            if spam_exp.search(word_eol[3][1:]):
                ban = "1"
                message = " Spam/Troll"
                helper.expel(message, ban, word)
                # Once the spammer is expelled, return to X-Chat/Hexchat so
                # the check for private messages isn't executed when it's a
                # public channel message.
                return xchat.EAT_NONE
    # Check wheter the message was received in a private conversation and
    # spambots protection is enabled.
    elif word[2] == xchat.get_info("nick") and SPAMBOTS == 1:
        # If so, check wheter there it contains spam
        for spam_exp in COMPILED_FILTERS:
            if spam_exp.search(word_eol[3][1:]):
                # If there is spam, expel the author
                ban = "1"
                message = " Spambot"
                helper.expel(message, ban, word)
                # And return to X-Chat/Hexchat eating the entire message
                return xchat.EAT_ALL
    # If this point is reached, this protections are disabled OR there is no
    # spam OR the message is from an unprotected channel, so return to
    # X-chat/Hexchat without doing anything
    else:
        return xchat.EAT_NONE


def antispam_add_cb(word, word_eol, userdata):
    """Adds a new filter to the end of the current antispam filters list.
    This function doesn't check for duplicates, just adds at the end.
    Arguments:
    word     -- array of strings sent by HexChat/X-Chat to every hook
    word_eol -- array of strings sent by HexChat/X-Chat to every hook (ignored)
    userdata -- optional variable that can be sent to a hook (ignored)
    """
    if helper.CONNECTED == 1:
        sql = "".join(['INSERT INTO filters ("id", "filter")',
                       ' VALUES (null, "', word[1], '")'])
        helper.gatodb_cursor_execute(sql)
        helper.gatodb_commit()
        message = "".join([word[1], " filter has been added to AntiSpam",
                           " filters"])
        helper.query_line(message)
        del message
        antispam_reload()
    else:
        helper.gprint("Enable the AntiSpam system before adding filters")
    return xchat.EAT_ALL


def antispam_del_cb(word, word_eol, userdata):
    """Removes one filter from the current antispam filters.
    This function doesnt check for duplicates, it removes every instance of the
    selected filter.
    Arguments:
    word     -- array of strings sent by HexChat/X-Chat to every hook (ignored)
    word_eol -- array of strings sent by HexChat/X-Chat to every hook
    userdata -- optional variable that can be sent to a hook (ignored)
    """
    if helper.CONNECTED == 1:
        sql = "".join(["DELETE FROM filters WHERE filter='", word_eol[1], "'"])
        helper.gatodb_cursor_execute(sql)
        helper.gatodb_commit()
        message = "".join([word_eol[1], " has been deleted from AntiSpam",
                           " filters"])
        helper.query_line(message)
        antispam_reload()
    else:
        helper.gprint("Enable the AntiSpam system before deleting filters")
    return xchat.EAT_ALL


def antispam_list_cb(word, word_eol, userdata):
    """Shows the list of currently active AntiSapm filters.
    Arguments:
    word     -- array of strings sent by HexChat/X-Chat to every hook (ignored)
    word_eol -- array of strings sent by HexChat/X-Chat to every hook (ignored)
    userdata -- optional variable that can be sent to a hook (ignored)
    """
    sql = "SELECT id, filter FROM filters"
    for item in helper.gatodb_cursor_execute(sql):
        message = u"".join([str(item[0]), ": ", item[1]])
        helper.query_line(message)
    del message
    return xchat.EAT_ALL


#############################################################################
# Define the help function
#############################################################################
def ghelp():
    """Returns the help information."""
    messages = [
    "",
    "Antispam:",
    "    /antiadd <string>:  Adds a new AntiSpam filter",
    "    /antidel <cadena>:  Removes an existing AntiSpam filter",
    "    /antilist:          Lists current AntiSpam filters",
    ""]
    return messages


#############################################################################
# Define the function to unload this module. This should be called from the
# main module unload function
#############################################################################
def unload():
    """This function disconects all module functions"""
    # Store all pending changes to the database
    helper.gatodb_commit()
    # Disconnect everything else
    xchat.unhook(HOOKANTISPAM)
    xchat.unhook(HOOKANTIADD)
    xchat.unhook(HOOKANTILIST)
    xchat.unhook(HOOKANTIDEL)
    xchat.unhook(HOOKTEST)


#############################################################################
# Hook all callbacks with their respective commands
#############################################################################

# Antispam
HOOKANTISPAM = xchat.hook_server('PRIVMSG', antispam_cb, userdata=None,
                                 priority=5)
HOOKANTIADD = xchat.hook_command('antiadd', antispam_add_cb)
HOOKANTILIST = xchat.hook_command('antilist', antispam_list_cb)
HOOKANTIDEL = xchat.hook_command('antidel', antispam_del_cb)


#############################################################################
# Add menu options
#############################################################################
xchat.command('menu ADD "GatoScript/-"')
xchat.command('menu ADD "GatoScript/AntiSpam"')
xchat.command('menu ADD "GatoScript/AntiSpam/Filters list" "antilist"')
xchat.command('menu ADD "GatoScript/AntiSpam/Add filter" "getstr \b \
              "antiadd" "Filter:""')
xchat.command('menu ADD "GatoScript/AntiSpam/Remove filter" "getstr \b \
              "antidel" "Filter:""')
