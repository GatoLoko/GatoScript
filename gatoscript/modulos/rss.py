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
Modulo RSS del GatoScript.

Este modulo contiene las funciones RSS para el GatoScript.
"""

__module_name__ = "GatoScript RSS"
__module_description__ = "Modulo RSS para el GatoScript"
__module_autor__ = "GatoLoko"

# Cargamos la libreria de funciones de X-Chat
import xchat
# Importamos las librerias externas
from os import path
import sqlite3
import xml.dom.minidom
import datetime
from urllib import urlopen
import auxiliar

##############################################################################
# Definimos algunas variables que describen el entorno de trabajo y librerias
# opcionales.
##############################################################################
_SCRIPTDIR = xchat.get_info("xchatdir")
_GATODIR = path.join(_SCRIPTDIR, "gatoscript")
_GATODB_PATH = path.join(_GATODIR, "gatoscript.db")
_GATOCONF = path.join(_SCRIPTDIR, "gatoscript.conf")

##############################################################################
# Inicializamos el modulo
##############################################################################
# Conectamos a la base de datos
if path.exists(_GATODB_PATH):
    CONEXIONDB = sqlite3.connect(_GATODB_PATH)
    CURSOR = CONEXIONDB.cursor()
    _CONECTADO = 1
else:
    _CONECTADO = 0

##############################################################################
## Definimos las funciones del lector rss
##############################################################################
def rss_cb(word, word_eol, userdata):
    """ Muestra las noticias actuales contenidas en los feeds que hemos
    configurado en la pestaña/ventana GatoScript.
    aleatoriamente.
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    feeds = CURSOR.execute("SELECT feeds limite FROM feeds")
    servidores = auxiliar.lee_conf("rss", "feeds").split(',')
    fecha = str(datetime.datetime.now())[:19]
    limitador = int(auxiliar.lee_conf("rss", "limitador"))
    for servidor in servidores:
        auxiliar.priv_linea(servidor + " - " + fecha)
        auxiliar.priv_linea("")
        archivo = xml.dom.minidom.parse(urlopen(servidor))
        if len(archivo.getElementsByTagName('item')) < limitador:
            limite = len(archivo.getElementsByTagName('item'))
        else:
            limite = limitador
        for i in range(limite):
            objeto = archivo.getElementsByTagName('item')[i]
            titulo = objeto.getElementsByTagName('title')[0].firstChild.data
            enlace = objeto.getElementsByTagName('link')[0].firstChild.data
            auxiliar.priv_linea("Enlace: " + enlace.encode('latin-1', 'replace') + " <--> Titulo: " + titulo.encode('latin-1', 'replace'))
            #i = i + 1
        auxiliar.priv_linea("")
    del servidores, fecha, servidor
    return xchat.EAT_ALL

def rsslista_cb(word, word_eol, userdata):
    """ Muestra la lista de feeds RSS/RDF que tenemos configurados.
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    servidores = auxiliar.lee_conf("rss", "feeds").split(',')
    auxiliar.priv_linea("")
    auxiliar.priv_linea("Lista de feeds RSS:")
    for servidor in servidores:
        auxiliar.priv_linea(servidor)
    auxiliar.priv_linea("")
    del servidores
    return xchat.EAT_ALL

def rssadd_cb(word, word_eol, userdata):
    """ Agrega un nuevo feed RSS/RDF a la configuracion.
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook
    word_eol -- array de cadenas que envia xchat a cada hook
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    info_param = len(word_eol)
    if info_param == 1:
        auxiliar.gprint("Debes añadir la direccion de un feed RSS")
    elif info_param > 2:
        auxiliar.gprint("De momento solo se admite un rss cada vez")
    else:
        actuales = auxiliar.lee_conf("rss", "feeds")
        nuevos = actuales + "," + word[1]
        auxiliar.escribe_conf("rss", "feeds", nuevos)
        auxiliar.gprint("Se ha agregado '" + word[1] + "' a la lista de feeds")
    del actuales, nuevos
    return xchat.EAT_ALL

def rssdel_cb(word, word_eol, userdata):
    """ Elimina un feed RSS/RDF de la lista.
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook
    word_eol -- array de cadenas que envia xchat a cada hook
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    info_param = len(word_eol)
    if info_param == 1:
        auxiliar.gprint("Debes añadir la direccion de un feed RSS")
    elif info_param > 2:
        auxiliar.gprint("De momento solo se admite un feed cada vez")
    else:
        actuales = auxiliar.lee_conf("rss", "feeds").split(',')
        try:
            actuales.remove(word_eol[1])
            temporal = ""
            for feed in range(len(actuales)):
                if (actuales[feed] != word_eol[1]) and (actuales[feed] != ""):
                    temporal = temporal + actuales[feed]
                    if feed < len(actuales)-1:
                        temporal = temporal + ','
            auxiliar.escribe_conf("rss", "feeds", temporal)
            auxiliar.gprint("Se ha eliminado '" + word_eol[1] + "'")
            del actuales, temporal, feed
        except ValueError:
            auxiliar.gprint("No existe ningun feed que coincida con el indicado")
    return xchat.EAT_ALL


#############################################################################
# Definimos las funciones de informacion y ayuda sobre el manejo del modulo
#############################################################################
def ayuda():
    """Muestra la ayuda de las funciones RSS para GatoScript."""
    mensajes = [
        "",
        "Gestion RSS",
        "    /rss:             Muestra las noticias actuales en los feeds actuales",
        "    /rsslista:        Muestra la lista de feeds actuales",
        "    /rssadd:          Añade un nuevo feed a la lista (No disponible aun)",
        "    /rssdel:          Elimina un feed de la lista actual (No disponible aun)",
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
    ## Desconectamos los comandos
    # Lector de feeds RSS
    xchat.unhook(hookrss)
    xchat.unhook(hooklistarss)
    xchat.unhook(hookrssadd)
    xchat.unhook(hookrssdel)
    # Descarga
    xchat.unhook(hookunload)


#############################################################################
# Conectamos los "lanzadores" de xchat con las funciones que hemos definido
# para ellos
#############################################################################
hookrss = xchat.hook_command('rss', rss_cb)
hooklistarss = xchat.hook_command('listarss', rsslista_cb)
hookrssadd = xchat.hook_command('rssadd', rssadd_cb)
hookrssdel = xchat.hook_command('rssdel', rssdel_cb)
# Descarga del script
hookunload = xchat.hook_unload(unload_cb)


#############################################################################
# Añadimos las opciones del menu
#############################################################################
xchat.command('menu ADD "GatoScript/RSS"')
xchat.command('menu ADD "GatoScript/RSS/Mostrar resultados" "rss"')
xchat.command('menu ADD "GatoScript/RSS/-"')
xchat.command('menu ADD "GatoScript/RSS/Lista de feeds" "listarss"')
xchat.command('menu ADD "GatoScript/RSS/Añadir feed" "getstr # "rssadd" "Feed:""')
xchat.command('menu ADD "GatoScript/RSS/Eliminar feed" "getstr # "rssdel" "Feed:""')