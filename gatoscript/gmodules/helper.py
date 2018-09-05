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
Helper module for GatoScript.

This module contains auxiliary functions used all around the script.
"""

__module_name__ = "GatoScript Helper"
__module_version__ = "2.0-alpha"
__module_description__ = "Helper module for GatoScript"
__module_autor__ = "GatoLoko"

# Load all needed libraries
import hexchat
from os import path
from configparser import SafeConfigParser
import sqlite3

#############################################################################
# Define some environment variables
#############################################################################

_SCRIPTDIR = hexchat.get_info("xchatdir")
_GATODIR = "".join([_SCRIPTDIR, "/gatoscript/"])
_CONFIGFILE = "".join([_GATODIR, "gatoscript.conf"])
_GATODB_PATH = "".join([_GATODIR, "gatoscript.db"])
# _HOME = path.expanduser("~")
_CP = SafeConfigParser()

#############################################################################
# Initialize the module
#############################################################################
if path.exists(_GATODB_PATH):
    _DBCONECTION = sqlite3.connect(_GATODB_PATH)
    _CURSOR = _DBCONECTION.cursor()
    CONNECTED = 1
else:
    CONNECTED = 0


#############################################################################
# Define functions for GatoScript
#############################################################################
# Information
def scriptdirs():
    """Get the base path for HexChat/X-Chat and GatoScript."""
    modules = path.join(_GATODIR, "gmodules")
    media = path.join(modules, "players")
    return _SCRIPTDIR, _GATODIR, modules, media


# Settings
def conf_read(option, section="common"):
    """Read ONE option from the config file.
    Arguments:
    option  -- string with the name of the option we want to read.
    section -- optional string with the section name. Default is "common".
    """
    if section == "":
        section = "common"
    _CP.read(_CONFIGFILE)
    return _CP.get(section, option)


def conf_show():
    """Reads the entire config file and shows it in the script query channel"""
    _CP.read(_CONFIGFILE)
    query_line("")
    query_line("List of configuration sections and options:")
    for section in _CP.sections():
        query_line(section)
        for option in _CP.options(section):
            message = "".join([" ", option, "=", _CP.get(section, option)])
            query_line(message)
    query_line("")


def conf_write(option, value, section="common"):
    """Store ONE option in the config file.
    Arguments:
    option  -- string with the option's name.
    value   -- string with the value to store.
    section -- optional string with the config section. Default is "common".
    """
    _CP.read(_CONFIGFILE)
    _CP.set(section, option, value)
    _CP.write(open(_CONFIGFILE, "w"))


# Database management
def gatodb_cursor_execute(sql):
    """Executes an sql statement over the database.
    Arguments:
    sql -- sql statement to be executed
    """
    try:
        results = _CURSOR.execute(sql)
        return results
    except sqlite3.Error as err:
        message = "SQL error: {0}".format(err.args[0])
        gprint(message)
        return None


def gatodb_commit():
    """ Commits any pending changes to the database."""
    _DBCONECTION.commit()


# Show script messages
def gprint(message):
    """Writes a line with format "Gatoscript >> blah", where blah is the string
    received as an argument. Usefull to send the user messages from the script.
    Arguments:
    message -- string with the message to show
    """
    g_message = "".join(["GatoScript >> ", message])
    print(g_message)


def query_print(messages):
    """Writes multiple lines to the private script channel tagged as
    "GatoScript". Usefull to send long messages without mixing/lossing them
    in the conversation.
    Arguments:
    messages -- list of string
    """
    orig_context = hexchat.get_context()
    context = hexchat.find_context(channel="GatoScript")
    if context is None:
        hexchat.command("query -nofocus GatoScript")
        context = hexchat.find_context(channel="GatoScript")
    for message in messages:
        context.emit_print("Private Message", "GatoScript", message)
    orig_context.set()


def query_line(message):
    """Writes a single line to the private script channel tagged as
    "GatoScript". Usefull to send short messages without mixing/lossing them
    in the conversation.
    Arguments:
    message -- message string
    """
    orig_context = hexchat.get_context()
    context = hexchat.find_context(channel="GatoScript")
    if context is None:
        hexchat.command("query -nofocus GatoScript")
        context = hexchat.find_context(channel="GatoScript")
    context.emit_print("Private Message", "GatoScript", message)
    orig_context.set()


# Expulsion
def expel(message, ban, word):
    """Expels an user from the channel according to the configured options.
    Arguments:
    message -- string with the kick message
    ban     -- boolean to add a ban or not
    word    -- string from where to extract the host to ban/kick
    """
    if message != "":
        if ban == "":
            ban = int(conf_read("protections", "ban"))
        if ban:
            host = word[0][1:].split("@")[-1]
            hexchat.command("".join(["ban *!*@", host]))
        hexchat.command("".join(["kick ", word[0][1:].split("!")[0], message]))


# Unit conversion
def units(value, base):
    """Converts amounts of bytes to one of its multiples
    Arguments:
    value    -- integer with the amount of bytes to convert
    """
    sufixes = {
        1024: ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB'],
        1000: ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']}
    if value < 0:
        raise ValueError('negative values are invalid')
    for sufix in sufixes[base]:
        # Add ".0" to the base to force the use of decimals
        value /= base / 1.0
        if value < base:
            # ".2f" only show 2 decimals
            return '{0:.2f}{1}'.format(value, sufix)
    raise ValueError('value too big')


#############################################################################
# Define the help function
#############################################################################
def ghelp():
    """This module doesn't contain any interactive functions"""
    return []


#############################################################################
# Define the function to unload this module. This should be called from the
# main module unload function
#############################################################################


#############################################################################
# Connect all HexChat/X-Chat hooks with the functions defined for them
#############################################################################
