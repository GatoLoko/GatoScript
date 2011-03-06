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
Modulo AntiSpam del GatoScript.

Este modulo contiene las funciones AntiSpam para el GatoScript.
"""

__module_name__ = "GatoScript AntiSpam"
__module_description__ = "Modulo AntiSpam para el GatoScript"
__module_autor__ = "GatoLoko"

# Cargamos las librerias y funciones que necesitamos
import xchat
import re
import auxiliar

#############################################################################
# Definimos algunas variables que describen el entorno de trabajo y librerias
# opcionales.
#############################################################################


#############################################################################
# Inicializamos el modulo
#############################################################################
# Cargamos la lista de filtros para el antispam y compilamos las regexps
if auxiliar.CONECTADO == 1:
    ANTISPAM = int(auxiliar.lee_conf("protecciones", "spam"))
    SPAMBOTS = int(auxiliar.lee_conf("protecciones", "spambots"))
    CANALES = []
    for canal in auxiliar.gatodb_cursor_execute("SELECT canales FROM canales"):
        CANALES.append(canal[0])
    filtros = auxiliar.gatodb_cursor_execute("SELECT filtro FROM filtros")
    compilados = []
    for filtro in filtros:
        compilados.append(re.compile(".*" + filtro[0] + ".*", re.IGNORECASE))
else:
    mensaje = "AntiSpam esta desactivado o no se puede cargar la lista de " + \
              "filtros"
    auxiliar.gprint(mensaje)
    ANTISPAM = 0
    SPAMBOTS = 0
    CANALES = ""


#############################################################################
# Definimos las funciones de uso interno en el modulo
#############################################################################
def antispam_reload():
    """Recarga la lista de filtros antispam para aplicar los cambios o
    retomar una lista anterior
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook (ignorado)
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    # Utilizamos las variables globales porque esto modifica el
    # funcionamiento del modulo completo
    global ANTISPAM
    global SPAMBOTS
    global CANALES
    if auxiliar.CONECTADO == 1:
        ANTISPAM = int(auxiliar.lee_conf("protecciones", "spam"))
        SPAMBOTS = int(auxiliar.lee_conf("protecciones", "spambots"))
        CANALES = []
        for canal in auxiliar.gatodb_cursor_execute("SELECT canales FROM canales"):
            CANALES.append(canal[0])
        # Cargamos la nueva lista de filtros y compilamos las regexps
        filtros = auxiliar.gatodb_cursor_execute("SELECT filtro FROM filtros")
        compilados = []
        for filtro in filtros:
            compilados.append(re.compile(".*" + filtro[0] + ".*", \
                                         re.IGNORECASE))
    else:
        auxiliar.gprint("No se pueden recargar los filtros, AntiSpam desactivado")
        ANTISPAM = 0
        SPAMBOTS = 0
        CANALES = ""


#############################################################################
# Definimos la funcion antispam para filtrado de mensajes privados.
# El sistema antispam eliminara todas las lineas que contengan alguna de las
# cadenas definidas en el archivo antispam.conf
#############################################################################
def antispam_cb(word, word_eol, userdata):
    """Compara las lineas que se reciben con una lista de filtros y elimina
    aquellas que coincidan. Ademas, de forma opcional, expulsa a los spambots.
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook (ignorado)
    word_eol -- array de cadenas que envia xchat a cada hook
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    global SPAMBOTS
    global ANTISPAM
    global CANALES
    # Comprobamos si el antispam esta activado.
    if ANTISPAM == 1:
        #canales = auxiliar.gatodb_cursor_execute("SELECT canales FROM canales")
        # Comprobamos si el mensaje se ha recibido en un canal protegido
        if word[2] in CANALES:
            for spam_exp in compilados:
                if spam_exp.search(word_eol[3][1:]):
                    ban = "1"
                    mensaje = " Spam/Troll"
                    auxiliar.expulsa(mensaje, ban, word)
                    # Una vez expulsado el spammer, devolvemos el control a
                    # X-Chat para que no se ejecute la comprobacion de privados
                    # cuando el mensaje se ha recibido en un canal publico.
                    return xchat.EAT_NONE
    # Comprobamos si el antibots esta activado.
    if SPAMBOTS == 1:
        # Comprobamos si el mensaje se ha recibido en un privado
        if word[2] == xchat.get_info("nick"):
            # Si es asi, comprobamos si el mensaje contiene spam
            for spam_exp in compilados:
                if spam_exp.search(word_eol[3][1:]):
                    # Si contiene spam, expulsamos al bot responsable
                    ban = "1"
                    mensaje = " Bot spammer"
                    auxiliar.expulsa(mensaje, ban, word)
                    # Quitamos el nick del spammer de la lista de niños buenos
                    nick = word[0].split("!")[0].split(":")[1]
                    sql = "SELECT goodboy FROM goodboys"
                    if nick in auxiliar.gatodb_cursor_execute(sql):
                        sql = "DELETE FROM goodboys WHERE goodboy IN (?)"
                        auxiliar.gatodb_cursor_execute(sql, (nick,))
                        auxiliar.gatodb_commit()
                    # Y devolvemos el control a X-Chat tragandonos el mensaje
                    return xchat.EAT_ALL
    # Si se ha llegado hasta aqui, es que estan desactivadas estas protecciones
    # o no hay spam o no esta en un canal protegido asi que volvemos a X-Chat
    # sin hacer nada.
    return xchat.EAT_NONE


def antispam_add_cb(word, word_eol, userdata):
    """Añade un nuevo filtro al final de la lista para usarse con el sistema
    antispam. Esta funcion no comprueba si el nuevo filtro ya existe,
    simplemente lo añade al final.
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    if auxiliar.CONECTADO == 1:
        sql = 'INSERT INTO filtros ("id", "filtro", "creado", "usado", "veces") \
              VALUES (null, "%s", date("now"), date("now"), "1")' % word[1]
        auxiliar.gatodb_cursor_execute(sql)
        auxiliar.gatodb_commit()
        mensaje = "Se ha añadido '" + word[1] + "' a la lista de filtros"
        auxiliar.priv_linea(mensaje)
        del mensaje
        antispam_reload()
    else:
        auxiliar.gprint("Active el sistema AntiSpam antes de quitar filtros")
    return xchat.EAT_ALL


def antispam_del_cb(word, word_eol, userdata):
    """Elimina un filtro de la lista que se usa con el sistema antispam.
    Esta funcion no verifica si hay duplicados, elimina todas las ocurrencias
    del filtro.
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook (ignorado)
    word_eol -- array de cadenas que envia xchat a cada hook
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    if auxiliar.CONECTADO == 1:
        sql = "DELETE FROM filtros WHERE filtro='%s'" % word_eol[1]
        auxiliar.gatodb_cursor_execute(sql)
        auxiliar.gatodb_commit()        
        mensaje = "Se ha eliminado '%s' de la lista de filtros" % word_eol[1]
        auxiliar.priv_linea(mensaje)
        del mensaje
        antispam_reload()
    else:
        auxiliar.gprint("Active el sistema AntiSpam antes de añadir filtros")
    return xchat.EAT_ALL


def antispam_list_cb(word, word_eol, userdata):
    """Muestra, en la pestaña "GatoScript", todas las lineas de la lista de
    filtros antispam.
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook (ignorado)
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    for filtro in auxiliar.gatodb_cursor_execute("SELECT id, filtro FROM filtros"):
        mensaje = u"Filtro %s: %s" % (filtro[0], filtro[1])
        auxiliar.priv_linea(mensaje)
    del mensaje
    return xchat.EAT_ALL


def testspam_cb(word, word_eol, userdata):
    """Envia un mensaje a todos los usuarios del canal que no esten en la
    lista de niños buenos para ver si responden con spam.
    """
    userlist = xchat.get_list("users")
    goodboys = []
    contexto_orig = xchat.find_context(server=None, channel=None)
    for row in auxiliar.gatodb_cursor_execute("SELECT goodboy FROM goodboys"):
        goodboys.append(row[0])
    for usuario in userlist:
        if usuario.nick not in goodboys:
            #print usuario.nick
            contexto = xchat.find_context(channel=usuario.nick)
            if contexto == None:
                xchat.command("query -nofocus %s" %usuario.nick)
                contexto = xchat.find_context(channel=usuario.nick)
            contexto.command("say %s" %auxiliar.lee_conf("protecciones", \
                    "botmensaje"))
            contexto.command("close")
            sql = "INSERT INTO goodboys VALUES (null, '%s')" % usuario.nick
            auxiliar.gatodb_cursor_execute(sql)
    auxiliar.gatodb_commit()
    contexto_orig.set()
    return xchat.EAT_NONE


#############################################################################
# Definimos la funcion de informacion y ayuda sobre el manejo del modulo 
#############################################################################
def ayuda():
    """Muestra la ayuda de las funciones antispam para GatoScript"""
    mensajes = [
    "",
    "Antispam:",
    "    /antiadd <cadena>: Añade una cadena al filtro AntiSpam",
    "    /antidel <cadena>: Elimina una cadena del filtro AntiSpam",
    "    /antilist:     Muestra la lista de filtros",
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
    # Guardamos los cambios en la base de datos
    auxiliar.gatodb_commit()
    # Desconectamos las funciones AntiSpam
    xchat.unhook(HOOKANTISPAM)
    xchat.unhook(HOOKANTIADD)
    xchat.unhook(HOOKANTILIST)
    xchat.unhook(HOOKANTIDEL)
    xchat.unhook(HOOKTEST)
    # Descargamos el 
    xchat.unhook(HOOKUNLOAD)


#############################################################################
# Conectamos los "lanzadores" de xchat con las funciones que hemos definido
# para ellos
#############################################################################

# Antispam
HOOKANTISPAM = xchat.hook_server('PRIVMSG', antispam_cb, userdata=None, priority=5)
HOOKANTIADD = xchat.hook_command('antiadd', antispam_add_cb)
HOOKANTILIST = xchat.hook_command('antilist', antispam_list_cb)
HOOKANTIDEL = xchat.hook_command('antidel', antispam_del_cb)
HOOKTEST = xchat.hook_command('test2', testspam_cb)
# Descarga del modulo
HOOKUNLOAD = xchat.hook_unload(unload_cb)


#############################################################################
# Añadimos las opciones del menu
#############################################################################
xchat.command('menu ADD "GatoScript/-"')
xchat.command('menu ADD "GatoScript/AntiSpam"')
xchat.command('menu ADD "GatoScript/AntiSpam/Lista de filtros" "antilist"')
xchat.command('menu ADD "GatoScript/AntiSpam/Añadir filtro" "getstr \b \
              "antiadd" "Filtro:""')
xchat.command('menu ADD "GatoScript/AntiSpam/Eliminar filtro" "getstr \b \
              "antidel" "Filtro:""')
