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
import xchat
from os import path
from ConfigParser import SafeConfigParser
import sqlite3

#############################################################################
# Define some environment variables
#############################################################################

_SCRIPTDIR = xchat.get_info("xchatdir")
_GATODIR = "".join([_SCRIPTDIR, "/gatoscript/"])
_CONFIGFILE = "".join([_GATODIR, "gatoscript.conf"])
_GATODB_PATH = "".join([_GATODIR, "gatoscript.db"])
#_HOME = path.expanduser("~")
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
    modules = path.join(_SCRIPTDIR, "modules")
    media = path.join(modules, "players")
    return _SCRIPTDIR, _GATODIR, modules, media


# Settings
def conf_read(option, section="common"):
    """Read ONE option from the config file.
    Arguments:
    option  -- string with the name of the option we want to read.
    section -- optional string with the section name. Default is "common".
    """
    if (section == ""):
        section = "common"
    _CP.read(_CONFIGFILE)
    return _CP.get(section, option)


def conf_write(option, value, section="common"):
    """Store ONE option in the config file.
    Arguments:
    option  -- string with the option's name.
    value   -- string with the value to store.
    section -- optional string with the config section. Default is "common".
    """
    _CP.read(_CONFIGFILE)
    _CP.set(section, option, value)
    _CP.write(file(_CONFIGFILE, "w"))


# Database management
def gatodb_cursor_execute(sql):
    """Executes an sql statement over the database.
    Arguments:
    sql -- sql statement to be executed
    """
    try:
        results = _CURSOR.execute(sql)
        return results
    except sqlite3.Error, err:
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
    mensaje -- cadena con el mensaje a mostrar
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
    orig_context = xchat.get_context()
    context = xchat.find_context(channel="GatoScript")
    if context is None:
        xchat.command("query -nofocus GatoScript")
        context = xchat.find_context(channel="GatoScript")
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
    orig_context = xchat.get_context()
    context = xchat.find_context(channel="GatoScript")
    if context is None:
        xchat.command("query -nofocus GatoScript")
        context = xchat.find_context(channel="GatoScript")
    context.emit_print("Private Message", "GatoScript", message)
    orig_context.set()


#Expulsion
def expulsa(mensaje, ban, word):
    """Expulsa un usuario del canal dependiendo de las opciones configuradas
    Argumentos:
    mensaje -- cadena con el mensaje de expulsion
    ban     -- booleano para añadir o no un veto
    word    -- cadena de la que extraemos el host a vetar/expulsar
    """
    if mensaje != "":
        if ban == "":
            ban = lee_conf("protecciones", "ban")
        if ban == "1":
            host = word[0][1:].split("@")[-1]
            comando = "".join(["ban *!*@", host])
            xchat.command(comando)
        partes = word[0][1:].split("!")
        comando = "".join(["kick ", partes[0], mensaje])
        xchat.command(comando)


#Unit conversion
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


# Comandos
def opciones_cb(word, word_eol, userdata):
    """Esta funcion se encarga de mostrar y modificar las configuraciones del
    script.
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook
    word_eol -- array de cadenas que envia xchat a cada hook
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    info_param = len(word_eol)
    if info_param == 1:
        _CP.read(_CONFIGFILE)
        priv_linea("")
        priv_linea("Lista de secciones y opciones de configuracion:")
        for seccion in _CP.sections():
            priv_linea(seccion)
            for opcion in _CP.options(seccion):
                mensaje = "".join([" ", opcion, "=", _CP.get(seccion, opcion)])
                priv_linea(mensaje)
        priv_linea("")
    elif info_param == 2:
        if word[1] == "prueba":
            print("Prueba con un solo parametro")
        else:
            print("Parametro erroneo")
    elif info_param == 4:
        escribe_conf(word[1], word[2], word[3])
    else:
        gprint("No mostramos nada")
    return xchat.EAT_ALL


# FIXME: This function interacts with the user and doesn't belong here
def gato_info_cb(word, word_eol, userdata):
    """Shows GatoScript publicity
    Arguments:
    word     -- array of strings sent by HexChat/X-Chat to every hook
    word_eol -- array of strings sent by HexChat/X-Chat to every hook
    userdata -- optional variable that can be sent to a hook (ignored)
    """
    if "hexchat" in _SCRIPTDIR:
        client = "HexChat"
    else:
        client = "X-Chat"
    version = xchat.get_info("version")
    xchat.command("".join(["say ( ", client, " ) ", version,
                           " ( Script ) GatoScript ", __module_version__,
                           " python script for HexChat/X-Chat ",
                           "(http://gatoloko.homelinux.org)"]))
    return xchat.EAT_ALL


# FIXME: This function interacts with the user and doesn't belong here
def kbtemp_cb(word, word_eol, userdata):
    """Temporarily expels an user on the active channel (must be OP).
    Arguments:
    word     -- array of strings sent by HexChat/X-Chat to every hook
    word_eol -- array of strings sent by HexChat/X-Chat to every hook
    userdata -- optional variable that can be sent to a hook (ignored)
    """
    if (len(word_eol) > 1):
        xchat.command("".join(["ban ", word[1], "!*@*"]))
        if (len(word_eol) > 2):
            xchat.command("".join(["kick ", word[1], " Banned for 5 minutes (",
                                   word_eol[2], ")"]))
        else:
            xchat.command("".join(["kick ", word[1], " Banned for 5 minutes"]))
        xchat.command("".join(["timer -repeat 1 300 unban ", word[1], "!*@*"]))
    else:
        gprint("You must specify a nick to kick/ban")
    return xchat.EAT_ALL


#############################################################################
# Define the help function
#############################################################################
def ayuda():
    """Muestra la ayuda de las funciones auxiliares para GatoScript."""
    mensajes = [
        "",
        "Auxiliar:",
        "Estas funciones son de uso interno y no deberian necesitar ayuda",
        "publica.",
        ""
        "Informacion:",
        "    /gato:               Muestra esta informacion",
        ""]
    return mensajes


#############################################################################
# Define the function to unload this module. This should be called from the
# main module unload function
#############################################################################
def unload_cb(userdata):
    """Esta funcion debe desconectar todas las funciones del modulo al
    descargarse el script.
    Argumentos:
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    # Opciones del script
    xchat.unhook(HOOKOPCIONES)
    # Informacion del script
    xchat.unhook(HOOKGINFO)
    # Temporary KickBan
    xchat.unhook(HOOKKBTEMP)


#############################################################################
# Connect all HexChat/X-Chat hooks with the functions defined for them
#############################################################################

# Opciones del script
HOOKOPCIONES = xchat.hook_command('opciones', opciones_cb)
# Informacion del script
HOOKGINFO = xchat.hook_command('ginfo', gato_info_cb)
# Temporary KickBan
kbtemp_usage = "".join([
    "Usage: KBTEMP <nick> <optional_message>, bans and kicks the selected",
    " nick from the actual channel, then activates a 5 minutes countdown,",
    " after wich the ban is removed. If a message is added, it's used as",
    " the kick reason. (You must be channel operator)"])
HOOKKBTEMP = xchat.hook_command('kbtemp', kbtemp_cb, help=kbtemp_usage)


#############################################################################
# Add Information and Options menus
#############################################################################
xchat.command('menu ADD "GatoScript/Information" "ginfo"')
xchat.command('menu ADD "GatoScript/-"')
xchat.command('menu ADD "GatoScript/Options"')
xchat.command('menu ADD "GatoScript/Options/Python" "py console"')
