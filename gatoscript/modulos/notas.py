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

__module_name__ = "GatoScript Notas"
__module_description__ = "Modulo Notas para el GatoScript"
__module_autor__ = "GatoLoko"

# Cargamos las librerias y funciones que necesitamos
import xchat
import auxiliar

#############################################################################
# Definimos algunas variables que describen el entorno de trabajo
#############################################################################


#############################################################################
# Inicializamos el modulo
#############################################################################
if auxiliar.CONECTADO:
    activado = 1
else:
    activado = 0

#############################################################################
# Definimos las funciones de uso interno en el modulo
#############################################################################


#############################################################################
# Definimos la funcion antispam para filtrado de mensajes privados.
# El sistema antispam eliminara todas las lineas que contengan alguna de las
# cadenas definidas en el archivo antispam.conf
#############################################################################
def notas_cb(word, word_eol, userdata):
    """Almacena, elimina o muestra una nota"""
    parametros = len(word)
    if parametros == 1:
        # Muestra una nota existente
        notas = auxiliar.gatodb_cursor_execute("SELECT nota FROM notas")
        for nota in notas:
            if nota == None:
                print("No hay notas almacenadas")
            else:
                print("Nota: {0}".format(nota[0]))
    elif parametros > 1:
        if word[1] == "añade":
            # Agrega una nota
            sql = 'INSERT INTO notas ("id", "nota") \
                  VALUES (null, "{0}")'.format(word_eol[2])
            auxiliar.gatodb_cursor_execute(sql)
            mensaje = "Se ha agregado '{0}' a las notas".format(word_eol[2])
            auxiliar.gprint(mensaje)
        elif word[1] == "quita":
            # Quitar una nota
            sql = "DELETE FROM notas WHERE nota='{0}'".format(word_eol[2])
            auxiliar.gatodb_cursor_execute(sql)
            mensaje = "Se ha quitado '{0}' de las notas".format(word_eol[2])
            auxiliar.gprint(mensaje)
        # Aplicar los cambios a la base de datos
        auxiliar.gatodb_commit()
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
    xchat.unhook(HOOKNOTA)
    # Descargamos el 
    xchat.unhook(HOOKNOTAS)


#############################################################################
# Conectamos los "lanzadores" de xchat con las funciones que hemos definido
# para ellos
#############################################################################
HOOKNOTA = xchat.hook_command('notas', notas_cb, userdata=None)
# Descarga del modulo
HOOKNOTAS = xchat.hook_unload(unload_cb)
