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
Modulo Ejemplo del GatoScript.

Este es un modulo de ejemplo del GatoScript.
"""

__module_name__ = "GatoScript Ejemplo"
__module_description__ = "Modulo Ejemplo para el GatoScript"
__module_autor__ = "GatoLoko"

# Cargamos las librerias y funciones que necesitamos
import xchat
import auxiliar

#############################################################################
# Definimos algunas variables que describen el entorno de trabajo
#############################################################################

_SCRIPTDIR = xchat.get_info("xchatdir")
_GATODIR = "{0}/gatoscript/".format(_SCRIPTDIR)

#############################################################################
# Inicializamos el modulo
#############################################################################


#############################################################################
# Definimos las funciones de uso interno en el modulo
#############################################################################
def ejemplo_interno():
    """Ejemplo de funcion"""
    # Comentario 
    auxiliar.gprint("Esta funcion solo se utiliza dentro de este modulo")


#############################################################################
# Definimos las funcion publicas del modulo
#############################################################################
def ejemplo_publico(word, word_eol, userdata):
    """Ejemplo de funcion publica
    Argumentos:
    Recibimos los 3 argumentos que utiliza xchat, aunque no los queramos
    word     -- array de palabras que envia xchat a cada hook (ignorado)
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    # Comentario
    auxiliar.gprint("Esta funcion se conecta a algun disparador de xchat")
    return xchat.EAT_ALL


#############################################################################
# Definimos la funcion de informacion y ayuda sobre el manejo del modulo 
#############################################################################
def ayuda():
    """Muestra la ayuda de las funciones de ejemplo para GatoScript"""
    mensajes = [
    "",
    "Ejemplo:",
    "    /ejemplo_publico: Muestra un mensaje de ejemplo",
    ""]
    return mensajes
    


#############################################################################
# Definimos la funcion para la descarga del programa
#############################################################################
def unload_cb(userdata):
    """Esta funcion debe desconectar todas las funciones del modulo al
    descargarse el script
    Argumentos:
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    # Desconectamos las funciones
    xchat.unhook(HOOKEJEMPLO1)
    # Descargamos el 
    xchat.unhook(HOOKEJEMPLO)


#############################################################################
# Conectamos los "lanzadores" de xchat con las funciones que hemos definido
# para ellos
#############################################################################
HOOKEJEMPLO1 = xchat.hook_command('ejemplo', ejemplo_publico, userdata=None)
# Descarga del modulo
HOOKEJEMPLO = xchat.hook_unload(unload_cb)
