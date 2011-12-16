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
import xml.dom.minidom
from urllib import urlopen
import auxiliar

##############################################################################
# Definimos algunas variables que describen el entorno de trabajo
##############################################################################


##############################################################################
# Inicializamos el modulo
##############################################################################


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
    feeds = auxiliar.gatodb_cursor_execute("SELECT feeds,limite FROM feeds")
    if feeds != None:
        for entrada in feeds:
            servidor = entrada[0]
            limitador = entrada[1]
            auxiliar.priv_linea(entrada[0])
            auxiliar.priv_linea("")
            archivo = xml.dom.minidom.parse(urlopen(servidor))
            if len(archivo.getElementsByTagName('item')) < limitador:
                limite = len(archivo.getElementsByTagName('item'))
            else:
                limite = limitador
            for i in range(limite):
                objeto = archivo.getElementsByTagName('item')[i]
                titulo = objeto.getElementsByTagName('title')[0].firstChild.data
                titulo = titulo.encode('latin-1', 'replace')
                enlace = objeto.getElementsByTagName('link')[0].firstChild.data
                enlace = enlace.encode('latin-1', 'replace')
                mensaje = "Enlace: {0} <--> Titulo: {1}".format(enlace, titulo)
                auxiliar.priv_linea(mensaje)
            auxiliar.priv_linea("")
        del feeds, servidor, limitador
    return xchat.EAT_ALL

def rsslista_cb(word, word_eol, userdata):
    """ Muestra la lista de feeds RSS/RDF que tenemos configurados.
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    servidores = auxiliar.gatodb_cursor_execute("SELECT feeds FROM feeds")
    auxiliar.priv_linea("")
    auxiliar.priv_linea("Lista de feeds RSS:")
    for servidor in servidores:
        auxiliar.priv_linea(servidor[0])
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
        sql = 'INSERT INTO feeds ("id", "feeds", "limite") \
              VALUES (null, "{0}", "10")'.format(word[1])
        auxiliar.gatodb_cursor_execute(sql)
        auxiliar.gatodb_commit()
        mensaje = "Se ha agregado '{0}' a la lista de filtros".format(word[1])
        auxiliar.gprint(mensaje)
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
        try:
            sql = "DELETE FROM feeds WHERE feeds='{0}'".format(word_eol[1])
            auxiliar.gatodb_cursor_execute(sql)
            auxiliar.gatodb_commit()
            auxiliar.gprint("Se ha eliminado '{0}'".format(word_eol[1]))
        except ValueError:
            mensaje = "No existe ningun feed que coincida con el indicado"
            auxiliar.gprint(mensaje)
    return xchat.EAT_ALL


#############################################################################
# Definimos las funciones de informacion y ayuda sobre el manejo del modulo
#############################################################################
def ayuda():
    """Muestra la ayuda de las funciones RSS para GatoScript."""
    mensajes = [
        "",
        "Gestion RSS",
        "    /rss:      Muestra las noticias actuales en los feeds actuales",
        "    /rsslista: Muestra la lista de feeds actuales",
        "    /rssadd:   Añade un nuevo feed a la lista (No disponible aun)",
        "    /rssdel:   Elimina un feed de la lista actual (No disponible aun)",
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
    xchat.unhook(HOOKRSS)
    xchat.unhook(HOOKLISTARSS)
    xchat.unhook(HOOKRSSADD)
    xchat.unhook(HOOKRSSDEL)
    # Descarga
    xchat.unhook(HOOKUNLOAD)


#############################################################################
# Conectamos los "lanzadores" de xchat con las funciones que hemos definido
# para ellos
#############################################################################
HOOKRSS = xchat.hook_command('rss', rss_cb)
HOOKLISTARSS = xchat.hook_command('listarss', rsslista_cb)
HOOKRSSADD = xchat.hook_command('rssadd', rssadd_cb)
HOOKRSSDEL = xchat.hook_command('rssdel', rssdel_cb)
# Descarga del script
HOOKUNLOAD = xchat.hook_unload(unload_cb)


#############################################################################
# Añadimos las opciones del menu
#############################################################################
xchat.command('menu ADD "GatoScript/RSS"')
xchat.command('menu ADD "GatoScript/RSS/Mostrar resultados" "rss"')
xchat.command('menu ADD "GatoScript/RSS/-"')
xchat.command('menu ADD "GatoScript/RSS/Lista de feeds" "listarss"')
xchat.command('menu ADD "GatoScript/RSS/Añadir feed" "getstr \b "rssadd" "Feed:""')
xchat.command('menu ADD "GatoScript/RSS/Eliminar feed" "getstr \b "rssdel" "Feed:""')
