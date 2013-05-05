# -*- coding: UTF8 -*-

# CopyRight (C) 2006-2009 GatoLoko
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
Highlight module for GatoScript.

This module contains functions to highlight texts and URLs
"""

__module_name__ = "GatoScript Highlight"
__module_description__ = "Highlight module for GatoScript"
__module_autor__ = "GatoLoko"

# Load all needed libraries
import xchat
import re
import helper

action_txt = [":ACTION", ":-ACTION", ":+ACTION"]
ctcp_txt = [":VERSION", ":TIME", ":FINGER", ":PING"]


##############################################################################
# Define internal use functions
##############################################################################
def color():
    if helper.conf_read("highlightoverride", "common") == "1":
        color = helper.conf_read("highlightcolor", "common")
    else:
        event = xchat.get_info('event_text Channel Msg Hilight')
        color = re.findall(r'%C[0-9]{1,2}', event)[-1][2:]
    return color


#############################################################################
# Define highlight functions
#############################################################################
def highlight_collect_cb(word, word_eol, userdata):
    """Looks for highlighted words (set on HexChat/X-Chat settings) and copy
    the entire line who contains it to the "GatoScript" tab.
    Arguments:
    word     -- array of strings sent by HexChat/X-Chat to every hook
    word_eol -- array of strings sent by HexChat/X-Chat to every hook
    userdata -- optional variable that can be sent to a hook (ignored)
    """
    if xchat.get_prefs("irc_extra_hilight") != '':
        highlight = xchat.get_prefs("irc_extra_hilight").split(",")
        # Extract some text to compose the output string
        channel = word[2]
        nick = word[0].split("!")[0][1:]
        text = word_eol[3][1:]
        # If there is any highlighted word, compose the string and write it to
        # the script query
        for highlighted in highlight:
            exp = re.compile(highlighted, re.IGNORECASE)
            if exp.search(text):
                if word[3] in action_txt:
                    helper.query_line("".join([
                        nick, "has mentioned \003", color(),
                        highlighted, "\003 in a query: <", nick, "> ",
                        word_eol[4][:-1]]))
                else:
                    helper.query_line("".join([
                        nick, " has mentioned \003", color(), highlighted,
                        "\003 in ", channel, ": <", nick, "> ", text]))
    return xchat.EAT_NONE


def url_highlight_cb(word, word_eol, userdata):
    """Looks for URLs and highlight them with the chosen color.
    Arguments:
    word     -- array of strings sent by HexChat/X-Chat to every hook
    word_eol -- array of strings sent by HexChat/X-Chat to every hook
    userdata -- optional variable that can be sent to a hook (ignored)
    """
    # If we are dealing with a CTCP, don't bother trying'
    if len(word[3]) > 1 and word[3][1] in ctcp_txt:
        return xchat.EAT_NONE
    if helper.conf_read("highlight", "common") == "1":
        urls = re.compile("".join([
            "((ftp|https?)://.*)|((www|ftp)\..*\..*)",
            "|([a-z0-9_\.-\\\+]+)\@([a-z0-9_\.-]+)\.([a-z\.]{2,6})"]),
            re.IGNORECASE)
        # Set the apropriate start depending on whether it's an action message
        # or the network it's received from
        action = False
        if word[3] in action_txt:
            words = word_eol[4][:-1].split(" ")
            action = True
        elif "freenode" in xchat.get_info("server").lower():
            words = word_eol[3][2:].split(" ")
        else:
            words = word_eol[3][1:].split(" ")
        address = []
        # Find if there is any URL
        for i in words:
            if urls.match(i):
                address.append(i)
        # If there is any URL, colorize all of them
        new_msg_tmp = []
        if address != []:
            for entry in words:
                if entry in address:
                    new_msg_tmp.append("".join(["\003", color(), entry,
                                                "\003"]))
                else:
                    new_msg_tmp.append(entry)
            new_msg = " ".join(new_msg_tmp)
            # Find the context:
            context = xchat.get_context()
            # Find what's the appropiate event and emit the corresponding text
            if action is False:
                context.emit_print("Channel Message",
                                   word[0].split("!")[0][1:], new_msg)
            else:
                if word[2][0] == "#":
                    context.emit_print("Channel Action",
                                       word[0].split("!")[0][1:], new_msg)
                else:
                    context.emit_print("Private Action",
                                       word[0].split("!")[0][1:], new_msg)
            return xchat.EAT_ALL
    else:
        return xchat.EAT_NONE


#############################################################################
# Define the help function
#############################################################################
def ghelp():
    """Returns the help information."""
    return []


#############################################################################
# Define the function to to unload this module. This should be called from the
# main module unload function
#############################################################################
def unload():
    """This function disconects all module functions"""
    xchat.unhook(HOOKHIGHLIGHT)
    xchat.unhook(HOOKURLHIGHLIGHT)


#############################################################################
# Hooks for all functions provided by this module
#############################################################################
# Highlight
HOOKHIGHLIGHT = xchat.hook_server('PRIVMSG', highlight_collect_cb,
                                  userdata=None)
HOOKURLHIGHLIGHT = xchat.hook_server('PRIVMSG', url_highlight_cb, userdata=None)
