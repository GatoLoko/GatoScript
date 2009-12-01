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
Modulo principal del GatoScript.

Este modulo se encarga de cargar e interconectar otras partes del GatoScript.
"""

__module_name__ = "GatoScript WhoIs"
__module_description__ = "Modulo WhoIs para GatoScript"
__module_autor__ = "GatoLoko"

# Cargamos la libreria de funciones de X-Chat
import xchat
# Importamos el modulo de funciones auxiliares
import auxiliar

# Definimos algunas variables de entorno para poder trabajar comodamente


##############################################################################
# Definimos las funciones de uso interno del modulo
##############################################################################
def espacios(palabra):
    """Devuelve una cadena de espacios de tamaño variable para facilitar el
    alineamiento de textos.
    Argumentos:
    palabra   -- palabra a la que se añadiran los espacios
    """
    cantidad = 15 - len(palabra)
    cadena = " "
    for i in range(cantidad):
        cadena = cadena + " "
    return cadena


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
        #if word[1] == "-g":
            #mensajes = [
            #"",
            #"Informacion:",
            #"    /gato:   Muestra esta informacion",
            #"    /ginfo:  Muestra en el canal activo la publicidad sobre el script",
            #""]
        #else:
            #mensajes = [
            #"",
            #"Parametro no soportado",
            #""]
    #return mensajes


#############################################################################
# Definimos la funcion para redireccion y formateo de respuestas al whois
#############################################################################
# Respuesta al whois: Informacion de usuario
def whois_cb(word, word_eol, userdata):
    """Redirecciona las respuestas al "whois" hacia la ventana activa, al
    tiempo que modifica el formato de salida.
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook
    word_eol -- array de cadenas que envia xchat a cada hook
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    whois_activo = auxiliar.lee_conf("comun", "whois")
    if (whois_activo == "1"):
        if (word[1] == "301"):
            # Respuesta al whois: AwayMessage
            print('\0033[No disponible   ]\003 ' + word_eol[4][1:])
        elif (word[1] == "310"):
            # Respuesta al whois: Operador de servicios
            cadena = espacios(word[3])
            print('\0033[' + word[3] + cadena + ']\003 ' + word_eol[4][1:])
        elif (word[1] == "311"):
            # Respuesta al whois: Usuario
            nick = word[3]
            host = word[4] + "@" + word[5]
            nombre = word_eol[7][1:]
            print('\0033[Nick            ]\003 ' + nick)
            print('\0033[Direccion       ]\003 ' + host)
            print('\0033[Nombre real     ]\003 ' + nombre)
        elif (word[1] == "312"):
            # Respuesta al whois: Servidor
            print('\0033[Servidor        ]\003 ' + word_eol[4])
        elif (word[1] == "313"):
            # Respuesta al whois: IrcOp
            cadena = espacios(word[3])
            print('\0033[' + word[3] + cadena + ']\003 ' + word_eol[4])
        elif (word[1] == "316"):
            # Respuesta al whois: Bot de la red
            cadena = espacios(word[3])
            print('\0033[' + word[3] + cadena + ']\003 ' + word_eol[4])
        elif (word[1] == "317"):
            # Respuesta al whois: IDLE
            horas = int(word[4])/3600
            minutos = (int(word[4])-horas*3600)/60
            segundos = int(word[4])-((horas*3600)+(minutos*60))
            tiempo = "%s horas, %s minutos y %s segundos" % (str(horas), \
                                                            str(minutos), \
                                                            str(segundos))
            print('\0033[IDLE            ]\003 %s' % tiempo)
        elif (word[1] == "318"):
            # Respuesta al whois: Fin del whois
            print('\0033Fin del WHOIS\003')
        elif (word[1] == "319"):
            # Respuesta al whois: Canales
            print('\0033[Canales         ]\003 ' + word_eol[4][1:])
        elif (word[1] == "320"):
            # Respuesta al whois: Especial
            cadena = espacios(word[3])
            print('\0033[' + word[3] + cadena + ']\003 ' + word_eol[4][1:])
        elif (word[1] == "335"):
            # Respuesta al whois: Bot
            print('\0033' + word_eol[0] + '\003')
        elif (word[1] == "307"):
            # Respuesta al whois: RegNick
            cadena = espacios(word[3])
            print('\0033[' + word[3] + cadena + '] \003' + word_eol[4][1:])
        elif (word[1] == "342"):
            # Respuesta al whois: Solo admite privados de usuarios registrados
            cadena = espacios(word[3])
            print('\0033[' + word[3] + cadena + '] \003' + word_eol[4][1:])
        elif (word[1] == "378"):
            # Respuesta al whois: VHOST
            print('\0033[VHost           ]\003 ' + word_eol[6])
        elif (word[1] == "379"):
            # Respuesta al whois: whoismodes
            print('\0033[Modos           ]\003 ' + word_eol[4][1:])
        elif (word[1] == "401"):
            # Respuesta al whois: No such nick
            print('\0033El nick ' + word[3] + ' no existe o no esta conectado\003')
        else:
            # Raw no definido
            print('\0033El raw ' + word[1] + ' no esta definido')
        return xchat.EAT_ALL
    else:
        return xchat.EAT_NONE


#############################################################################
# Definimos la funcion para la descarga del programa
#############################################################################
def unload_cb(userdata):
    """Esta funcion debe desenlazar todas las funciones del GatoScript al descargarse el script
    Argumentos:
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    # Desconectamos los comandos
    # Whois
    xchat.unhook(_RAW301)
    xchat.unhook(_RAW307)
    xchat.unhook(_RAW310)
    xchat.unhook(_RAW311)
    xchat.unhook(_RAW312)
    xchat.unhook(_RAW313)
    xchat.unhook(_RAW316)
    xchat.unhook(_RAW317)
    xchat.unhook(_RAW318)
    xchat.unhook(_RAW319)
    xchat.unhook(_RAW320)
    xchat.unhook(_RAW335)
    xchat.unhook(_RAW342)
    xchat.unhook(_RAW378)
    xchat.unhook(_RAW379)
    xchat.unhook(_RAW401)
    # Descarga
    xchat.unhook(_HOOKUNLOAD)


#############################################################################
# Conectamos los "lanzadores" de xchat con las funciones que hemos definido
# para ellos
#############################################################################
# Whois
# Mensaje de AWAY
_RAW301 = xchat.hook_server('301', whois_cb, userdata=None, priority=10)
# whoisregnick
_RAW307 = xchat.hook_server('307', whois_cb, userdata=None, priority=10)
# whoishelpop
_RAW310 = xchat.hook_server('310', whois_cb, userdata=None, priority=10)
# whoisuser
_RAW311 = xchat.hook_server('311', whois_cb, userdata=None, priority=10)
# whoisserver
_RAW312 = xchat.hook_server('312', whois_cb, userdata=None, priority=10)
# whoisoperator
_RAW313 = xchat.hook_server('313', whois_cb, userdata=None, priority=10)
# whoischanop
_RAW316 = xchat.hook_server('316', whois_cb, userdata=None, priority=10)
# whoisidle
_RAW317 = xchat.hook_server('317', whois_cb, userdata=None, priority=10)
# endofwhois
_RAW318 = xchat.hook_server('318', whois_cb, userdata=None, priority=10)
# whoischannels
_RAW319 = xchat.hook_server('319', whois_cb, userdata=None, priority=10)
# whoisspecial
_RAW320 = xchat.hook_server('320', whois_cb, userdata=None, priority=10)
# whoisbot
_RAW335 = xchat.hook_server('335', whois_cb, userdata=None, priority=10)
# Solo admite privados de usuarios registrados
_RAW342 = xchat.hook_server('342', whois_cb, userdata=None, priority=10)
# whoishost (ip virtual)
_RAW378 = xchat.hook_server('378', whois_cb, userdata=None, priority=10)
# whoismodes
_RAW379 = xchat.hook_server('379', whois_cb, userdata=None, priority=10)
# No such nick
_RAW401 = xchat.hook_server('401', whois_cb, userdata=None, priority=10)


# Descarga del script
_HOOKUNLOAD = xchat.hook_unload(unload_cb)
