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
Modulo Resaltados del GatoScript.

Este modulo contiene las funciones resalte/"des-resalte" de textos para el
GatoScript.
"""

__module_name__ = "GatoScript Resaltados"
__module_description__ = "Modulo Resaltados para GatoScript"
__module_autor__ = "GatoLoko"

# Cargamos la libreria de funciones de X-Chat
import xchat
# import re
import re
# Importamos el modulo de funciones auxiliares
import auxiliar

color = auxiliar.lee_conf("comun", "colorrealze")
action_txt = [":ACTION", ":-ACTION", ":+ACTION"]


#############################################################################
# Redireccion de resaltados
#############################################################################
def resaltados_cb(word, word_eol, userdata):
    """Detecta palabras resaltadas (en la configuracion del xchat) y copia la
    linea que las contiene a la pestaña "GatoScript"
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook
    word_eol -- array de cadenas que envia xchat a cada hook
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    resaltados = xchat.get_prefs("irc_extra_hilight")
    if resaltados != '':
        resaltados = xchat.get_prefs("irc_extra_hilight").split(",")
        canal = word[2]
        nick = word[0].split("!")[0][1:]
        for resaltado in resaltados:
            palabra = re.compile(resaltado, re.IGNORECASE)
            if palabra.search(word_eol[3][1:]):
                if word[3] in action_txt:
                    auxiliar.priv_linea("".join([nick, "ha mencionado",
                        " \003", color, resaltado, "\003 en un privado; ",
                        nick, " ", word_eol[4][:-1]]))
                else:
                    auxiliar.priv_linea("".join([nick,
                        " ha mencionado ", "\003", color, resaltado,
                        "\003 en ", canal, ": <", nick, "> ",
                         word_eol[3][1:]]))
    return xchat.EAT_NONE


def realza_url_cb(word, word_eol, userdata):
    """Detecta URLs y les aplica un color distinto al texto normal
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook
    word_eol -- array de cadenas que envia xchat a cada hook
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    if auxiliar.lee_conf("comun", "realze") == "1":
        urls = [ "(ftp://.*|http://.*|https://.*)", "(www|ftp)\..*\..*" ]
        nuevo_mensaje = ""
        color = auxiliar.lee_conf("comun", "colorrealze")
        # Algunas redes agregan un caracter extra a los mensajes
        if "freenode" in xchat.get_info("server"):
            palabras = word_eol[3][2:].split(" ")
        else:
            palabras = word_eol[3][1:].split(" ")
        direccion = []
        for i in urls:
            #print i
            expresion = re.compile(i, re.IGNORECASE)
            for j in palabras:
                if expresion.match(j):
                    direccion.append(j)
        for palabra in palabras:
            if palabra in direccion:
                if nuevo_mensaje == "":
                    nuevo_mensaje = " \003{0}{1}\003".format(color, palabra)
                else:
                    nuevo_mensaje = "{0} \003{1}{2}\003".format(nuevo_mensaje,
                                                                color, palabra)
            else:
                if nuevo_mensaje == "":
                    nuevo_mensaje = palabra
                else:
                    nuevo_mensaje = "{0} {1}".format(nuevo_mensaje, palabra)
        if word[2][0] == "#":
            contexto = xchat.find_context(channel=word[2])
        else:
            comando = "query -nofocus {0}".format(word[0].split("!")[0][1:])
            xchat.command(comando)
            contexto = xchat.find_context(channel=word[0].split("!")[0][1:])
        # Action messages change from one network to the next.
        # IRC-Hispano:
        #   >> :nick!ident@host PRIVMSG #canal :ACTION hola
        # Freenode:
        #   >> :nickt!~ident@host PRIVMSG #canal :-ACTION hola
        #   >> :nickt!~ident@host PRIVMSG #canal :+ACTION hola
        if word[3] in [":ACTION", ":-ACTION", ":+ACTION"]:
            #print "action"
            #contexto.emit_print("Action", word[0].split("!")[0][1:],
            #                    nuevo_mensaje)
            #action_mensaje = nuevo_mensaje[8:-2]
            #contexto.prnt("\00313* {0}\003 {1}".format(
            #    word[0].split("!")[0][1:], nuevo_mensaje[8:-2]))
            return xchat.EAT_NONE
        else:
            contexto.emit_print("Channel Message", word[0].split("!")[0][1:],
                                nuevo_mensaje)
            return xchat.EAT_ALL


#############################################################################
# Definimos las funciones de informacion y ayuda sobre el manejo del script
#############################################################################
def ayuda_cb(word, word_eol, userdata):
    """Muestra la ayuda del GatoScript
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook
    word_eol -- array de cadenas que envia xchat a cada hook
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    info_param = len(word_eol)
    if info_param > 2:
        mensajes = [
        "",
        "Solo se puede usar un parametro cada vez",
        ""]
    else:
        if word[1] == "-g":
            mensajes = [
            "",
            "Informacion:",
            "    /gato:   Muestra esta informacion",
            "    /ginfo:  Muestra en el canal activo la publicidad sobre el script",
            ""]
        else:
            mensajes = [
            "",
            "Parametro no soportado",
            ""]
    auxiliar.priv_imprime(mensajes)
    return xchat.EAT_ALL


#############################################################################
# Definimos la funcion para la descarga del programa
#############################################################################
def unload_cb(userdata):
    """Esta funcion debe desenlazar todas las funciones del modulo al
    descargarse el script
    Argumentos:
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    # Desconectamos los comandos
    # Resaltados
    xchat.unhook(HOOKRESALTADOS)
    xchat.unhook(HOOKREALZAURL)
    # Descarga
    xchat.unhook(HOOKUNLOAD)


#############################################################################
# Conectamos los "lanzadores" de xchat con las funciones que hemos definido
# para ellos
#############################################################################
# Resaltados
HOOKRESALTADOS = xchat.hook_server('PRIVMSG', resaltados_cb, userdata=None)
HOOKREALZAURL = xchat.hook_server('PRIVMSG', realza_url_cb, userdata=None,
                                  priority=-10)
# Descarga del script
HOOKUNLOAD = xchat.hook_unload(unload_cb)
