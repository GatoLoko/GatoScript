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

__module_name__ = "GatoScript"
__module_version__ = "1.0"
__module_description__ = "GatoScript para XChat"
__module_autor__ = "GatoLoko"

# Cargamos la libreria de funciones de X-Chat
import xchat
# Importamos la funcion para unir directorios de forma portable
from os.path import join
# Importamos la funcion que nos permite definir nuestro directorio de modulos
import sys

# Definimos algunas variables de entorno para poder trabajar comodamente
scriptdir = xchat.get_info("xchatdir")
moddir = join(scriptdir, "gatoscript", "modulos")

# Incluimos el directorio de modulos en el path
sys.path.append(moddir)

xchat.command('menu -p4 ADD "GatoScript"')

# Importamos el modulo de funciones auxiliares
import auxiliar
# Importamos el modulo antispam
import antispam
# Importamos el modulo de protecciones
import protecciones
# Importamos el modulo gestor de whois
import whois
# Importamos el modulo de resaltes
import resaltados
# Importamos el modulo MultiMedia
import media
# Importamos el modulo gestor de rss
import rss
# Importamos el modulo sysinfo
import sysinfo
# Importamos el modulo autosend
import autosend
# Importamos el modulo p2p
import p2p
# Importamos el modolo remotos
import remotos
# Importamos el modulo consejos
# import consejos
# Importamos el modulo de notas
import notas
# Importamos el modulo ejemplo
# import ejemplo

#############################################################################
# Definimos la funcion para descargar el script
#############################################################################
def unload_cb(userdata):
    xchat.command('menu del GatoScript')
    print("Se ha descargado GatoScript %s" % __module_version__)

#############################################################################
# Conectamos la funcion de descarga del script
#############################################################################
HOOKUNLOAD = xchat.hook_unload(unload_cb)

# Si se ha llegado a este punto el script esta cargado completamente, asi que
# mostramos el mensaje de carga
mensaje = "Cargado GatoScript %s" % __module_version__
auxiliar.gprint(mensaje)

##############################################################################
##
## Codigos especiales en las cadenas:
##
##   X-Chat      Python      Resultado
##   "%C"    =   "\003"  =   Color
##   "%B"    =   "\002"  =   Negrilla
##   "%U"    =   "\037"  =   Subrallado
##   "%R"    =   "\026"  =   Color invertido
##   "%O"    =   "\017"  =   Desactiva los demas
##           =   "\007"  =   Pitido
##   "$t"    =   "\t"    =   $t
##
##############################################################################
