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
Protections module for GatoScript.

This module contains protections functions for GatoScript
"""

__module_name__ = "GatoScript Protections"
__module_description__ = "Protections module for GatoScript"
__module_autor__ = "GatoLoko"

# Cargamos la libreria de funciones de X-Chat
import xchat
# Importamos las librerias externas
import re
# Importamos la libreria de funciones auxiliares
import auxiliar

##############################################################################
# Definimos algunas variables que describen el entorno de trabajo y librerias
# opcionales
##############################################################################
_NUM_ABUSOS_MAYUS = []
_NUM_ABUSOS_COLORES = []

##############################################################################
# Definimos las funciones de uso interno del modulo
##############################################################################


##############################################################################
# Definimos las funciones de proteccion
##############################################################################
def anti_ctcp_cb(word, word_eol, userdata):
    """Detecta el envio de CTCPs a canales protegidos y expulsa al autor.
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    if auxiliar.lee_conf("protecciones", "ctcps") == "1":
        for canal in auxiliar.lee_conf("protecciones", "canales").split(','):
            if canal.lower() == word[2].lower():
                ctcp = re.compile("\.*\", re.IGNORECASE)
                canales = auxiliar.lee_conf("protecciones",
                                            "canales").split(',')
                if ctcp.search(word[3]):
                    for canal in canales:
                        canal_re = re.compile(canal[1:], re.IGNORECASE)
                        if canal_re.search(word[2]):
                            mensaje = "".join(["Se ha recibido un CTCP al ",
                                               "canal ", word[2]])
                            auxiliar.gprint(mensaje)
                            host = word[0][1:].split("@")[-1]
                            xchat.command("".join(["ban *!*@", host]))
                            nick = word[0][1:].split("!")[0]
                            xchat.command("".join(["kick ", nick, "CTCPs al ",
                                                   "canal..."]))
    return xchat.EAT_NONE


def anti_notice_cb(word, word_eol, userdata):
    """Detecta el envio de NOTICEs a canales protegidos y expulsa al autor.
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    """
    #>> :Anti_Bots!GatoBot@BvW8Qj.CtqRtH.virtual NOTICE #gatoscript :hola
    #>> :CHaN!-@- NOTICE #canal :nick añade en #canal a nick2 con nivel 499
    if auxiliar.lee_conf("protecciones", "notices") == "1":
        canales = auxiliar.lee_conf("protecciones", "canales").split(',')
        for canal in canales:
            if (word[2].lower() == canal.lower()) and \
            (word[0].lower() != ":chan!-@-"):  # Excepcion para IRC-Hispano
                print word[0]
                print "este ban lo pone por notice"
                xchat.command("".join(["kickban ", word[0][1:].split("!")[0],
                                       " Putos scriptkidies..."]))
    return xchat.EAT_NONE


def anti_hoygan_cb(word, word_eol, userdata):
    """Detecta la palabra "hoygan" en los canales y banea al autor
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    #>> :nick!ident@host PRIVMSG #channel :message
    if auxiliar.lee_conf("protecciones", "hoygan") == "1":
        for canal in auxiliar.lee_conf("protecciones", "canales").split(','):
            if canal.lower() == word[2].lower():
                hoyga = re.compile('hoyga|h 0 y g 4 n', re.IGNORECASE)
                if hoyga.search(word_eol[3]):
                    host = word[0][1:].split("@")[-1]
                    xchat.command("".join(["ban *!*@", host]))
                    nick = word[0][1:].split("!")[0]
                    xchat.command("".join(["kick ", nick, " Los hoygan son la",
                                           " versión electronica del payaso",
                                           " de la clase y no son",
                                           "graciosos."]))
                    del host, nick
    return xchat.EAT_NONE


def anti_mayusculas_cb(word, word_eol, userdata):
    """Detecta el abuso de mayusculas en los canales y banea al autor
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook
    word_eol -- array de cadenas que envia xchat a cada hook
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    if auxiliar.lee_conf("protecciones", "mayusculas") == "1":
        for canal in auxiliar.lee_conf("protecciones", "canales").split(','):
            if canal.lower() == word[2].lower():
                mensaje = ""
                cadena = word_eol[3][1:]
                accion = re.compile('^[\+,-]?\ACTION')
                if accion.match(cadena):
                    cadena = cadena[7:]
                letrasre = re.compile('[a-zA-Z]')
                letras = letrasre.findall(cadena)
                abuso = True
                for letra in letras:
                    if letra.islower() is True:
                        abuso = False
                if (len(letras)) > 10 and abuso is True:
                    host = word[0][1:].split("@")[1]
                    nick = word[0][1:].split("!")[0]
                    if host in _NUM_ABUSOS_MAYUS:
                        _NUM_ABUSOS_MAYUS.remove(host)
                        mensaje = "".join([" Escribir todo en mayusculas va",
                                           "contra las normas y estabas",
                                           " avisado"])
                        auxiliar.expulsa(mensaje, "1", word)
                    else:
                        _NUM_ABUSOS_MAYUS.append(host)
                        mensaje = "".join(["msg ", word[2], " ", nick, ": no",
                                           " escribas todo en mayusculas, va",
                                           " contra las normas. La próxima",
                                           " vez seras expulsado."])
                        xchat.command("")
                        xchat.command(mensaje)
    return xchat.EAT_NONE


def anti_colores_cb(word, word_eol, userdata):
    """Detecta el envio de mensajes con colores o realzados en los canales
    protegidos, avisa al autor en la primera ocasion y lo expulsa si reincide
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook
    word_eol -- array de cadenas que envia xchat a cada hook
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    accion = re.compile('^[\+,-]?\ACTION')
    colores = re.compile("".join(['\\x02|\\x16|\\x1f|\\x03(([0-9]{1,2})?',
                                  '(,[0-9]{1,2})?)?']))
    ignorar = False
    if auxiliar.lee_conf("protecciones", "banea_colores") == "1":
        for canal in auxiliar.lee_conf("protecciones", "canales").split(','):
            if canal.lower() == word[2].lower():
                mensaje = ""
                cadena = word_eol[3][1:]
                if accion.match(cadena):
                    cadena = cadena[7:]
                if colores.search(cadena):
                    host = word[0][1:].split("@")[1]
                    if host in _NUM_ABUSOS_COLORES:
                        _NUM_ABUSOS_COLORES.remove(host)
                        mensaje = "".join([" El uso de colores va contra las",
                                           "normas y estabas avisado."])
                        auxiliar.expulsa(mensaje, "1", word)
                    else:
                        _NUM_ABUSOS_COLORES.append(host)
                        mensaje = "".join(["msg ", word[2], " ",
                                           word[0][1:].split("!"), ": no uses",
                                           " colores/negrillas/subrayado en",
                                            " este canal, va contra las",
                                            " normas. La próxima vez serás",
                                            " expulsado. Para desactivarlos",
                                            " escribe:  /remote off"])
                        xchat.command(mensaje)
    if auxiliar.lee_conf("protecciones", "ignora_colores") == "1":
        for canal in auxiliar.lee_conf("protecciones", "canales").split(','):
            if canal.lower() == word[2].lower():
                cadena = word_eol[3][1:]
                if accion.match(cadena):
                    cadena = cadena[7:]
                if colores.search(cadena):
                    ignorar = True
    if ignorar is True:
        auxiliar.gprint("".join(["Mensaje de ", word[0][1:].split("!")[0],
                                 "ignorado por uso de colores."]))
        return xchat.EAT_ALL
    else:
        return xchat.EAT_NONE


def anti_drone_cb(word, word_eol, userdata):
    """Detecta nicks que entran al canal con nick/indent que concuerde con los
    de un Drone y los banea para evitar el expulsa para evitar el SPAM.
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    #print word_eol[0]
    if auxiliar.lee_conf("protecciones", "drones") == "1":
        nickre = re.compile("^[a-z]{4,}_[a-z]{2}$", re.IGNORECASE)
        identre = re.compile("^[a-z]{4,}_[a-z]{1,2}$", re.IGNORECASE)
        nick = word[0][1:].split("!")[0]
        ident = word[0][1:].split("!")[1].split("@")[0]
        if nickre.search(nick) and identre.search(ident):
            canal = word[2][1:]
            contexto = xchat.find_context(channel=canal)
            host = word[0].split("@")[1]
            contexto.command("".join(["ban *!*@", host]))
            contexto.command("".join(["kick ", nick, " Bot"]))
    return xchat.EAT_NONE


def anti_away_cb(word, word_eol, userdata):
    """Detecta mensajes de ausencia en el canal y expulsa al usuario
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se envia a un hook (ignorado)
    """
    if auxiliar.lee_conf("protecciones", "away") == "1":
        for canal in auxiliar.lee_conf("protecciones", "canales").split(','):
            if canal.lower() == word[2].lower():
                awaystr = auxiliar.lee_conf("protecciones",
                                            "awaystr").split(",")
                for i in range(len(awaystr)):
                    if word_eol[3].find(awaystr[i]) > 0:
                        ban = "1"
                        mensaje = "".join([" Quita los mensajes de away ",
                                           "automáticos, si no estás callate"])
                        auxiliar.expulsa(mensaje, ban, word)
    return xchat.EAT_NONE


##############################################################################
# Definimos la funcion de informacion y ayuda sobre el manejo del modulo
##############################################################################
def ayuda():
    """Muestra la ayuda de las funciones  de proteccion para GatoScript"""
    mensajes = [
    "",
    "Protecciones:",
    "    Este modulo no ofrece comandos interactivos",
    ""]
    auxiliar.priv_imprime(mensajes)
    return xchat.EAT_ALL


##############################################################################
## Definimos la funcion para la descarga del programa
##############################################################################
def unload_cb(userdata):
    """Esta funcion debe desconectar todas las funciones del modulo al
    descargarse el script
    Argumentos:
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    # Desconectamos las funciones de proteccion
    xchat.unhook(HOOKANTINOTICE)
    xchat.unhook(HOOKANTIDRONE)
    xchat.unhook(HOOKANTICTCP)
    xchat.unhook(HOOKANTIHOYGAN)
    xchat.unhook(HOOKANTIMAYUSCULAS)
    xchat.unhook(HOOKANTICOLORES)
    xchat.unhook(HOOKANTIAWAY)


##############################################################################
# Conectamos los "lanzadores" de xchat con las funciones que hemos definido
# para ellos
##############################################################################

# Protecciones
HOOKANTINOTICE = xchat.hook_server('NOTICE', anti_notice_cb, userdata=None)
HOOKANTIDRONE = xchat.hook_server('JOIN', anti_drone_cb, userdata=None)
HOOKANTICTCP = xchat.hook_server('PRIVMSG', anti_ctcp_cb, userdata=None)
HOOKANTIHOYGAN = xchat.hook_server('PRIVMSG', anti_hoygan_cb, userdata=None)
HOOKANTIMAYUSCULAS = xchat.hook_server('PRIVMSG', anti_mayusculas_cb,
                                       userdata=None)
HOOKANTICOLORES = xchat.hook_server('PRIVMSG', anti_colores_cb, userdata=None)
HOOKANTIAWAY = xchat.hook_server('PRIVMSG', anti_away_cb, userdata=None)


#############################################################################
# Add menu options
#############################################################################
xchat.command('menu ADD "GatoScript/Options/Protections"')
xchat.command("".join(['menu -t', helper.conf_read("away", "protections"),
                       ' ADD "GatoScript/Options/Protections/Away"',
                       ' "options protections away 1"',
                       ' "options protections away 0"']))
xchat.command("".join(['menu -t', helper.conf_read("ban", "protections"),
                       ' ADD "GatoScript/Options/Protections/Ban"',
                       ' "options protections ban 1"',
                       ' "options protections ban 0"']))
xchat.command("".join(['menu -t',
                       helper.conf_read("ignore_colors", "protections"),
                       ' ADD "GatoScript/Options/Protections/Ignore colors"',
                       ' "options protections colors 1"',
                       ' "options protections colors 0"']))
xchat.command("".join(['menu -t',
                       helper.conf_read("ban_colors", "protections"),
                       ' ADD "GatoScript/Options/Protections/Ban colors"',
                       ' "options protections colors 1"',
                       ' "options protections colors 0"']))
xchat.command("".join(['menu -t', helper.conf_read("ctcps", "protections"),
                       ' ADD "GatoScript/Options/Protections/CTCPs"',
                       ' "options protections ctcps 1"',
                       ' "options protections ctcps 0"']))
xchat.command("".join(['menu -t', helper.conf_read("caps", "protections"),
                       ' ADD "GatoScript/Options/Protections/Caps"',
                       ' "options protections caps 1"',
                       ' "options protections caps 0"']))
xchat.command("".join(['menu -t', helper.conf_read("hoygan", "protections"),
                       ' ADD "GatoScript/Options/Protections/HOYGAN"',
                       ' "options protections hoygan 1"',
                       ' "options protections hoygan 0"']))
xchat.command("".join(['menu -t', helper.conf_read("spam", "protections"),
                       ' ADD "GatoScript/Options/Protections/Spam"',
                       ' "options protections spam 1"',
                       ' "options protections spam 0"']))
