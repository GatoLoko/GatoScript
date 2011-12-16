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
_GATODIR = "{0}/gatoscript/".format(_SCRIPTDIR)
_GATODB_PATH = "{0}gatoscript.db".format(_GATODIR)

#############################################################################
# Inicializamos el modulo
#############################################################################
if auxiliar.lee_conf("autosend", "activo") == "1":
    ACTIVO = True
    ALMACEN = "{0}{1}".format(_GATODIR,
                              auxiliar.lee_conf("autosend", "directorio"))

# Conectamos a la base de datos
if path.exists(_GATODB_PATH):
    CONEXIONDB = sqlite3.connect(_GATODB_PATH)
    CURSOR = CONEXIONDB.cursor()
    _CONECTADO = 1
else:
    _CONECTADO = 0


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
def torrent_cb(word, word_eol, userdata):
#    """Docstring incompleta
#    Argumentos:
#    Recibimos los 3 argumentos que utiliza xchat, aunque no los queramos
#    word     -- array de palabras que envia xchat a cada hook
#    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
#    userdata -- variable opcional que se puede enviar a un hook (ignorado)
#    """
#>> :Anti_Bots!GatoBot@CUhvdB.DnL1wf.virtual PRIVMSG #gatoscript :!torrent
    protegidos = []
    for i in CURSOR.execute("SELECT canales FROM canales"):
        protegidos.append(i[0])
    if ACTIVO == True:
        #Definimos la expresion regular que actuara como disparador
        texto = auxiliar.lee_conf("autosend", "disparador")
        disparador = re.compile("^{0}".format(texto), re.IGNORECASE)
        if word[2] in protegidos:
            if disparador.search(word[3][1:]):
                partes = word_eol[3].split()
                if len(partes) == 1:
                    lista = listdir(ALMACEN)
                    if len(lista) == 0:
                        xchat.command("say No hay archivos disponibles")
                    elif len(lista) > 0:
                        archivos = ""
                        for archivo in lista:
                            archivos += "{0} ".format(archivo)
                        parte1 = "say Tengo los siguietnes "
                        parte2 = "archivos: {0}".format(archivos)
                        mensaje = "{0}{1}".format(parte1, parte2)
                        xchat.command(mensaje)
                        parte1 = "say Para pedir uno "
                        parte2 = "pon: {0} archivo".format(texto)
                elif len(partes) == 2:
                    lista = listdir(ALMACEN)
                    if partes[1] in lista:
                        parte1 = "dcc send "
                        parte2 = "{0} {1}/{2}".format(word[0][1:].split("!")[0],
                                                      ALMACEN, partes[1])
                        envio = "{0}{1}".format(parte1, parte2)
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
    xchat.unhook(HOOKTORRENT)
    # Descargamos el 
    xchat.unhook(HOOKAUTOSEND)


#############################################################################
# Conectamos los "lanzadores" de xchat con las funciones que hemos definido
# para ellos
#############################################################################
HOOKTORRENT = xchat.hook_server('PRIVMSG', torrent_cb, userdata=None)
# Descarga del modulo
HOOKAUTOSEND = xchat.hook_unload(unload_cb)
