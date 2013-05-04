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
        urls = ["(ftp://.*|http://.*|https://.*)", "(www|ftp)\..*\..*"]
        new_msg = ""
        action = False
        # Action messages change from one network to the next, so we need to be
        # carefull and take it into account.
        # IRC-Hispano:
        #   >> :nick!ident@host PRIVMSG #canal :ACTION hola
        # Freenode:
        #   >> :nickt!~ident@host PRIVMSG #canal :-ACTION hola
        #   >> :nickt!~ident@host PRIVMSG #canal :+ACTION hola
        if word[3] in [":ACTION", ":-ACTION", ":+ACTION"]:
            palabras = word_eol[4][:-1].split(" ")
            action = True
        elif "freenode" in xchat.get_info("server").lower():
            palabras = word_eol[3][2:].split(" ")
        else:
            palabras = word_eol[3][1:].split(" ")
        direccion = []
        for i in urls:
            expresion = re.compile(i, re.IGNORECASE)
            for j in palabras:
                if expresion.match(j):
                    direccion.append(j)
        for palabra in palabras:
            if palabra in direccion:
                if new_msg == "":
                    new_msg = "".join(["\003", color, palabra, "\003"])
                else:
                    new_msg = "".join([new_msg, " \003", color, palabra,
                        "\003"])
            else:
                if new_msg == "":
                    new_msg = palabra
                else:
                    new_msg = "".join([new_msg, " ", palabra])
        # Find the context:
        if word[2][0] == "#":
            contexto = xchat.find_context(channel=word[2])
        else:
            xchat.command("".join(["query -nofocus ",
                word[0].split("!")[0][1:]]))
            contexto = xchat.find_context(channel=word[0].split("!")[0][1:])
        # Emit the apropiate message
        if action is False:
            contexto.emit_print("Channel Message", word[0].split("!")[0][1:],
                 new_msg)
        else:
            if word[2][0] == "#":
                contexto.emit_print("Channel Action",
                    word[0].split("!")[0][1:], new_msg)
            else:
                contexto.emit_print("Private Action",
                    word[0].split("!")[0][1:], new_msg)
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


#############################################################################
# Conectamos los "lanzadores" de xchat con las funciones que hemos definido
# para ellos
#############################################################################
# Resaltados
HOOKRESALTADOS = xchat.hook_server('PRIVMSG', resaltados_cb, userdata=None)
HOOKREALZAURL = xchat.hook_server('PRIVMSG', realza_url_cb, userdata=None,
                                  priority=-10)
