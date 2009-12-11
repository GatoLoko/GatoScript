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
Modulo Remotos del GatoScript.

Este modulo contiene las funciones para comandos remotos del GatoScript.
"""

__module_name__ = "GatoScript Remotos"
__module_description__ = "Modulo Remotos para el GatoScript"
__module_autor__ = "GatoLoko"

# Cargamos la libreria de funciones de X-Chat
import xchat
import re
import auxiliar

#############################################################################
# Definimos algunas variables que describen el entorno de trabajo
#############################################################################

#############################################################################
# Inicializamos el modulo
#############################################################################
if auxiliar.CONECTADO:
    remotos_db = auxiliar.gatodb_cursor_execute("SELECT disparador,respuesta,es_comando FROM remotos")
    remotos = []
    for elemento in remotos_db:
        expresion = elemento[0]
        remoto = elemento[0], elemento[1], elemento[2], re.compile(expresion, re.IGNORECASE)
        remotos.append(remoto)

##############################################################################
## Definimos las funciones de informacion y ayuda sobre el manejo del script
##############################################################################
#def gato_cb(word, word_eol, userdata):
    #"""Muestra la ayuda del GatoScript
    #Argumentos:
    #word     -- array de palabras que envia xchat a cada hook
    #word_eol -- array de cadenas que envia xchat a cada hook
    #userdata -- variable opcional que se puede enviar a un hook (ignorado)
    #"""
    #info_param = len(word_eol)
    #if info_param > 2:
        #mensajes = [
        #"",
        #"Solo se puede usar un parametro cada vez",
        #""]
    #else:
        #else:
            #mensajes = [
            #"",
            #"Parametro no soportado",
            #""]
    #priv_imprime(mensajes)
    #return xchat.EAT_ALL


##############################################################################
## Definimos las funcion de controles remotos
##############################################################################
def remoto_cb(word, word_eol, userdata):
    """Esta funcion revisa los mensajes recibidos en busca de comandos remotos
    y cuando los encuentra, actua en consecuencia.
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook
    word_eol -- array de cadenas que envia xchat a cada hook
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    remotos_activo = auxiliar.lee_conf("comun", "remotos")
    if (remotos_activo == "1"):
        #Definimos la expresion regular que actuara como activador
        consejo_rem = re.compile("!consejo", re.IGNORECASE)
        hola_rem = re.compile("!hola", re.IGNORECASE)
        version_rem = re.compile("!version", re.IGNORECASE)
        #Si se ha encontrado actuamos
        if consejo_rem.search(word[1]):
            #consejo_aleatorio_cb("0", "0", "0")
            xchat.command("say No hay consejos disponibles en este momento")
        elif hola_rem.search(word[1]):
            xchat.command("say Hola %s!!" %word[0])
        elif version_rem.search(word[1]):
            xchat.command("gsoft")
            xchat.command("ginfo")
        for remoto in remotos:
            if remoto[3].search(word[1]):
                if remoto[3] == 1:
                    #respuestas = remoto[1].split(",")
                    xchat.command("say Esto no esta implementado aun")
                else:
                    xchat.command("say %s" % remoto[1])


##############################################################################
## Definimos la funcion para la descarga del programa
##############################################################################
def unload_cb(userdata):
    """Esta funcion debe desenlazar todas las funciones del modulo al
    descargarse el script.
    Argumentos:
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    # Desconectamos los comandos
    # Controles remotos
    xchat.unhook(HOOKREMOTO)
    # Descarga
    xchat.unhook(HOOKREMOTOS)


##############################################################################
## Conectamos los "lanzadores" de xchat con las funciones que hemos definido
## para ellos
##############################################################################
# Controles remotos
HOOKREMOTO = xchat.hook_print('Channel Message', remoto_cb)
# Descarga del script
HOOKREMOTOS = xchat.hook_unload(unload_cb)
