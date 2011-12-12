#!/usr/bin/python
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
Modulo Auxiliar del GatoScript.

Este modulo contiene las funciones auxiliares para el GatoScript.
"""

__module_name__ = "GatoScript Auxiliar"
__module_version__ = "1.5-alpha"
__module_description__ = "Modulo Auxiliar para el GatoScript"
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
_GATODIR = "{0}/gatoscript/".format(_SCRIPTDIR)
_CONFIGFILE = "{0}gatoscript.conf".format(_GATODIR)
_GATODB_PATH = "{0}gatoscript.db".format(_GATODIR)
#home = xchat.get_info("xchatdir")[:-7]
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
    """Obtiene el directorio base de xchat."""
    base = xchat.get_info("xchatdir")
    script = path.join(base, "gatoscript")
    modules = path.join(script, "modulos")
    media = path.join(modules, "players")
    return base, script, modules, media

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
    try:
        resultado = _CURSOR.execute(sql)
        return resultado
    except sqlite3.Error, err:
        mensaje = "Se ha producido un error SQL: {0}".format(err.args[0])
        gprint(mensaje)
        return None

def gatodb_commit():
    _CONEXIONDB.commit()

# Mostrar mensajes
def gprint(mensaje):
    """Escribe "Gatoscript >> " seguido de la cadena que recibe como
    parametro. Util para mostrar mensajes del script al usuario.
    Argumentos:
    mensaje -- cadena con el mensaje a mostrar
    """
    g_mensaje = "GatoScript >> {0}".format(mensaje)
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
    if contexto == None:
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
    if contexto == None:
        xchat.command("query -nofocus GatoScript")
        contexto = xchat.find_context(channel="GatoScript")
    #contexto.prnt(mensaje)
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
            partes = word[0][1:].split("@")
            comando = "ban *!*@{0}".format(partes[len(partes)-1])
            xchat.command(comando)
        partes = word[0][1:].split("!")
        comando = "kick {0}{1}".format(partes[0], mensaje)
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
        valor /= base/1.0
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
                mensaje = " {0}={1}".format(opcion, _CP.get(seccion, opcion))
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
    version = xchat.get_info("version")
    parte1 = "say (X-Chat) {0} - ".format(version)
    parte2 = "( Script ) GatoScript {0}, ".format(__module_version__)
    parte3 = "script en python para X-Chat (http://gatoloko.homelinux.org"
    xchat.command("{0}{1}{2}".format(parte1, parte2, parte3))
    return xchat.EAT_ALL

def kbtemporal_cb(word, word_eol, userdata):
    """Expulsa de forma temporal a un usuario del canal activo (si somos OPs).
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook
    word_eol -- array de cadenas que envia xchat a cada hook
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    if (len(word_eol) > 2):
        xchat.command("ban {0}!*@*".format(word[1]))
        parte1 = "kick {0} ".format(word[1])
        parte2 = "Expulsado 5 minutos ({0})".format(word_eol[2])
        xchat.command("{0}{1}".format(parte1, parte2))
        xchat.command("timer -repeat 1 300 unban {0}!*@*".format(word[1]))
    elif (len(word_eol) > 1):
        xchat.command("ban {0}!*@*".format(word[1]))
        xchat.command("kick {0} Expulsado 5 minutos".format(word[1]))
        xchat.command("timer -repeat 1 300 unban {0}!*@*".format(word[1]))
    else:
        gprint("Hay que especificar un nick a patear")
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
    # KickBan Temporal
    xchat.unhook(HOOKKBTEMP)
    # Descarga
    xchat.unhook(HOOKAUXILIAR)


#############################################################################
# Conectamos los "lanzadores" de xchat con las funciones que hemos definido
# para ellos
#############################################################################

# Opciones del script
HOOKOPCIONES = xchat.hook_command('opciones', opciones_cb)
# Informacion del script
HOOKGINFO = xchat.hook_command('ginfo', gato_info_cb)
# KickBan Temporal
HOOKKBTEMP = xchat.hook_command('kbtemp', kbtemporal_cb, help="Uso: KB_TEMP <nick> <mensaje_opcional> Establece un baneo temporal de 5 minutos sobre el nick indicado y lo expulsa. Si se introduce un mensaje se usa como razon de la expulsion. (Necesita ser operador del canal)")
# Descarga del script
HOOKAUXILIAR = xchat.hook_unload(unload_cb)

#############################################################################
# Añadimos las opciones del menu
#############################################################################
xchat.command('menu ADD "GatoScript/Informacion" "ginfo"')
xchat.command('menu ADD "GatoScript/-"')
xchat.command('menu ADD "GatoScript/Opciones"')
xchat.command('menu ADD "GatoScript/Opciones/Python" "py console"')

