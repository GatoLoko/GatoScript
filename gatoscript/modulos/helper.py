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
Modulo Auxiliar del GatoScript.

Este modulo contiene las funciones auxiliares para el GatoScript.
"""

__module_name__ = "GatoScript Helper"
__module_version__ = "2.0-alpha"
__module_description__ = "Helper module for GatoScript"
__module_autor__ = "GatoLoko"

# Cargamos las librerias y funciones que necesitamos
import xchat
from os import path
from ConfigParser import SafeConfigParser
import sqlite3

#############################################################################
# Definimos algunas variables que describen el entorno de trabajo y librerias
# opcionales.
#############################################################################

_SCRIPTDIR = xchat.get_info("xchatdir")
_GATODIR = "".join([_SCRIPTDIR, "/gatoscript/"])
_CONFIGFILE = "".join([_GATODIR, "gatoscript.conf"])
_GATODB_PATH = "".join([_GATODIR, "gatoscript.db"])
#_HOME = path.expanduser("~")
_CP = SafeConfigParser()

#############################################################################
# Inicializamos el modulo
#############################################################################
if path.exists(_GATODB_PATH):
    _CONEXIONDB = sqlite3.connect(_GATODB_PATH)
    _CURSOR = _CONEXIONDB.cursor()
    CONECTADO = 1
else:
    CONECTADO = 0


#############################################################################
# Definimos las funciones de uso interno en el GatoScript
#############################################################################
# Informacion
def scriptdirs():
    """Get the base path for HexChat/X-Chat and GatoScript."""
    modules = path.join(_SCRIPTDIR, "modules")
    media = path.join(modules, "players")
    return _SCRIPTDIR, _GATODIR, modules, media


# Configuracion
def lee_conf(seccion, opcion):
    """Lee una opcion del archivo de configuracion.
    Argumentos:
    seccion -- cadena con el nombre de la seccion del archivo de
    configuracion, en caso de no suministrarte se usara "comun"
    opcion  -- cadena con el nombre de la opcion que queremos leer
    """
    if (seccion == ""):
        seccion = "comun"
    _CP.read(_CONFIGFILE)
    return _CP.get(seccion, opcion)


def escribe_conf(seccion, opcion, valor):
    """Guarda una opcion en el archivo de configuracion.
    Argumentos:
    seccion -- cadena con el nombre de la seccion del archivo de
    configuracion, en caso de no suministrarse se utilizara "comun"
    opcion  -- cadena con el nombre de la opcion que queremos guardar
    valor   -- cadena con el valor que queremos asignar a esa opcion
    """
    if (seccion == ""):
        seccion = "comun"
    _CP.read(_CONFIGFILE)
    _CP.set(seccion, opcion, valor)
    _CP.write(file(_CONFIGFILE, "w"))


def gatodb_cursor_execute(sql):
    """Executes an sql statement over the database.
    Arguments:
    sql -- sql statement to be executed
    """
    try:
        resultado = _CURSOR.execute(sql)
        return resultado
    except sqlite3.Error, err:
        mensaje = "Se ha producido un error SQL: {0}".format(err.args[0])
        gprint(mensaje)
        return None


def gatodb_commit():
    """ Commits any pending changes to the database."""
    _CONEXIONDB.commit()


# Mostrar mensajes
def gprint(mensaje):
    """Escribe "Gatoscript >> " seguido de la cadena que recibe como
    parametro. Util para mostrar mensajes del script al usuario.
    Argumentos:
    mensaje -- cadena con el mensaje a mostrar
    """
    g_mensaje = "".join(["GatoScript >> ", mensaje])
    print(g_mensaje)
    return ""


def priv_imprime(mensajes):
    """Escribe una o mas lineas en la pestaña "GatoScript". Util para mostrar
    mensajes largos sin que se pierdan entre los recibidos en los canales,
    asi como menus de opciones.
    Argumentos:
    mensajes -- array de cadenas
    """
    contexto = xchat.find_context(channel="GatoScript")
    if contexto is None:
        xchat.command("query -nofocus GatoScript")
        contexto = xchat.find_context(channel="GatoScript")
    for mensaje in mensajes:
        contexto.emit_print("Private Message", "GatoScript", mensaje)
    return ""


def priv_linea(mensaje):
    """Escribe una linea en la pestaña "GatoScript". Util para mostrar mensajes
    cortos sin que se pierdan entre los recibidos en los canales.
    Argumentos:
    mensaje -- cadena con el mensaje
    """
    contexto = xchat.find_context(channel="GatoScript")
    if contexto is None:
        xchat.command("query -nofocus GatoScript")
        contexto = xchat.find_context(channel="GatoScript")
    contexto.emit_print("Private Message", "GatoScript", mensaje)
    return ""


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


#Conversion de unidades
def unidades(valor, base):
    """Convierte cantidades de bytes a alguno de sus multiplos
    Argumentos:
    valor    -- entero con la cantidad en bytes que queremos convertir
    """
    sufijos = {1024: ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB'],
        1000: ['KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']}
    if valor < 0:
        raise ValueError('los valores negativos no son validos')
    for sufijo in sufijos[base]:
        # Agregamos ".0" a la base para forzar el uso de decimales
        valor /= base / 1.0
        if valor < 1024:
            # ".2f" limita los decimales mostrados a 2
            return '{0:.2f}{1}'.format(valor, sufijo)
    raise ValueError('numero demasiado grande')


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


def gato_info_cb(word, word_eol, userdata):
    """Muestra la publicidad del GatoScript
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook
    word_eol -- array de cadenas que envia xchat a cada hook
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    if "hexchat" in xchat.get_info("xchatdir"):
        cliente = "HexChat"
    else:
        cliente = "X-Chat"
    version = xchat.get_info("version")
    comando = ''.join(["say ( {0} ) {1}".format(cliente, version),
        " ( Script ) GatoScript {0},".format(__module_version__),
        " script en python para X-Chat/HexChat",
        " (http://gatoloko.homelinux.org)"])
    xchat.command(comando)
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
# Definimos las funciones de informacion y ayuda sobre el manejo del modulo
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
# Definimos la funcion para la descarga del programa
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
# Conectamos los "lanzadores" de xchat con las funciones que hemos definido
# para ellos
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
