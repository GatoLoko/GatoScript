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
Modulo AntiSpam del GatoScript.

Este modulo contiene las funciones auxiliares para el GatoScript.
"""

__module_name__ = "GatoScript Auxiliar"
__module_version__ = "1.0alpha"
__module_description__ = "Modulo Auxiliar para el GatoScript"
__module_autor__ = "GatoLoko"

# Cargamos las librerias y funciones que necesitamos
import xchat
from os import path
from ConfigParser import ConfigParser

#############################################################################
# Definimos algunas variables que describen el entorno de trabajo y librerias
# opcionales.
#############################################################################

_SCRIPTDIR = xchat.get_info("xchatdir")
_GATODIR = _SCRIPTDIR + "/gatoscript/"
_CONFIGFILE = _GATODIR + "gatoscript.conf"
#home = xchat.get_info("xchatdir")[:-7]
HOME = path.expanduser("~")
CP = ConfigParser()

#############################################################################
# Inicializamos el modulo
#############################################################################

#############################################################################
# Definimos las funciones de uso interno en el GatoScript
#############################################################################
def lee_conf(seccion, opcion):
    """Lee una opcion del archivo de configuracion.
    Argumentos:
    seccion -- cadena con el nombre de la seccion del archivo de
    configuracion, en caso de no suministrarte se usara "comun"
    opcion  -- cadena con el nombre de la opcion que queremos leer
    """
    if (seccion == ""):
        seccion = "comun"
    CP.read(_CONFIGFILE)
    return CP.get(seccion, opcion)

def gprint(mensaje):
    """Escribe "Gatoscript >> " seguido de la cadena que recibe como
    parametro. Util para mostrar mensajes del script al usuario.
    Argumentos:
    mensaje -- cadena con el mensaje a mostrar
    """
    g_mensaje = "GatoScript >> " + mensaje
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
    CP.read(_CONFIGFILE)
    CP.set(seccion, opcion, valor)
    CP.write(file(_CONFIGFILE, "w"))

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
            comando = "ban *!*@" + partes[len(partes)-1]
            xchat.command(comando)
        partes = word[0][1:].split("!")
        comando = "kick " + partes[0] + mensaje
        xchat.command(comando)

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
        CP.read(_CONFIGFILE)
        priv_linea("")
        priv_linea("Lista de secciones y opciones de configuracion:")
        for seccion in CP.sections():
            priv_linea(seccion)
            for opcion in CP.options(seccion):
                mensaje =  " " + opcion + "=" + CP.get(seccion, opcion)
                priv_linea(mensaje)
        priv_linea("")
    elif info_param == 2:
        if word[1] == "prueba":
            print "Prueba con un solo parametro"
        else:
            print "Parametro erroneo"
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
    xchat.command("say (X-Chat) %s - ( Script ) GatoScript %s, script en python para X-Chat (http://gatoloko.homelinux.org)" %(version, __module_version__))
    return xchat.EAT_ALL


#############################################################################
# Definimos las funciones de informacion y ayuda sobre el manejo del modulo
#############################################################################
def ayuda():
    """Muestra la ayuda de las funciones auxiliares para GatoScript."""
    mensajes = [
        "",
        "Auxiliar:",
        "Estas funciones son de uso interno y no deberian necesitar ayuda publica.",
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
# Descarga del script
HOOKAUXILIAR = xchat.hook_unload(unload_cb)
