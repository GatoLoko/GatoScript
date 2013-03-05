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
Modulo AutoSend del GatoScript.

Este modulo distribuye archivos de forma automatizada.
"""

__module_name__ = "GatoScript AutoSend"
__module_description__ = "Modulo AutoSend para el GatoScript"
__module_autor__ = "GatoLoko"

# Cargamos las librerias y funciones que necesitamos
import xchat
import auxiliar
import re
from os import listdir, path
import sqlite3

#############################################################################
# Definimos algunas variables que describen el entorno de trabajo y librerias
# opcionales.
#############################################################################

_SCRIPTDIR = xchat.get_info("xchatdir")
_GATODIR = "".join([_SCRIPTDIR, "/gatoscript/"])
_GATODB_PATH = "".join([_GATODIR, "gatoscript.db"])
_SQL = "SELECT canales FROM canales"

#############################################################################
# Inicializamos el modulo
#############################################################################
if auxiliar.lee_conf("autosend", "activo") == "1":
    ACTIVO = True
    ALMACEN = "".join([_GATODIR, auxiliar.lee_conf("autosend", "directorio")])
    TEXTO = auxiliar.lee_conf("autosend", "disparador")
    DISPARADOR = re.compile("".join(["^", TEXTO]), re.IGNORECASE)
    if auxiliar.CONECTADO == 1:
        CANALES = []
        for canal in auxiliar.gatodb_cursor_execute(_SQL):
            CANALES.append(canal[0].lower())
    else:
        ACTIVO = False


#############################################################################
# Definimos las funciones de uso interno en el modulo
#############################################################################
#def ejemplo_interno():
#    """Ejemplo de funcion"""
#    # Comentario
#    auxiliar.gprint("Esta funcion solo se utiliza dentro de este modulo")


#############################################################################
# Definimos las funciones de uso publico en el modulo
#############################################################################
def autosend_cb(word, word_eol, userdata):
    """This function manages the automatic response to users asking for files
    Arguments:
    We get the 3 arguments the client feeds us, but ignore the third one
    word     -- array of words
    word_eol -- array of strings
    userdata -- optional variable that we don't have an use for (ignorado)
    """
#>> :Anti_Bots!GatoBot@CUhvdB.DnL1wf.virtual PRIVMSG #gatoscript :!archivos
    if ACTIVO is True and word[2].lower() in CANALES and \
    DISPARADOR.search(word[3][1:]):
        partes = word_eol[3].split()
        if len(partes) == 1:
            lista = listdir(ALMACEN)
            if len(lista) == 0:
                xchat.command("say No hay archivos disponibles")
            elif len(lista) > 0:
                archivos = ""
                for archivo in lista:
                    archivos += "".join([archivo, " "])
                mensaje = ''.join(["say Tengo los siguientes archivos: ",
                                   archivos])
                xchat.command(mensaje)
                mensaje = ''.join(["say Para pedir uno pon: ", TEXTO,
                                   " archivo"])
                xchat.command(mensaje)
        elif len(partes) == 2:
            lista = listdir(ALMACEN)
            if partes[1] in lista:
                envio = "".join(["dcc send ", word[0][1:].split("!")[0],
                                 ALMACEN, "/", partes])
                xchat.command(envio)
            else:
                xchat.command("say No tengo archivos con ese nombre")
        elif len(partes) > 2:
            xchat.command("say ¡No seas abuson!¡Un archivo cada vez!")
    return xchat.EAT_NONE


#############################################################################
# Definimos la funcion de informacion y ayuda sobre el manejo del modulo
#############################################################################
#def ayuda():
#    """Muestra la ayuda de las funciones de AutoSend para GatoScript"""
#    mensajes = [
#    "",
#    "Ejemplo:",
#    "    /ejemplo_publico: Muestra un mensaje de ejemplo",
#    ""]
#    return mensajes
    


#############################################################################
# Definimos la funcion para la descarga del programa
#############################################################################
def unload_cb(userdata):
    """Esta funcion debe desconectar todas las funciones del modulo al
    descargarse el script
    Argumentos:
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    # Desconectamos las funciones del modulo
    xchat.unhook(HOOKAUTOSEND)


#############################################################################
# Conectamos los "lanzadores" de xchat con las funciones que hemos definido
# para ellos
#############################################################################
HOOKAUTOSEND = xchat.hook_server('PRIVMSG', autosend_cb, userdata=None)
