#!/usr/bin/python
# -*- coding: UTF8 -*-

# CopyRight (C) 2006-2007 GatoLoko
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

"""
Modulo principal del GatoScript.

Este modulo contiene las mayor parte de la logica del GatoScript.
"""

__module_name__ = "GatoScript"
__module_version__ = "0.16alpha"
__module_description__ = "GatoScript para XChat"
__module_autor__ = "GatoLoko"

# Cargamos las librerias y funciones que necesitamos
import xchat, re, datetime, xml.dom.minidom
from os import popen3, path
#from string import split, find
from random import randint
from ConfigParser import ConfigParser
from urllib import urlopen


#############################################################################
# Definimos algunas variables que describen el entorno de trabajo y librerias
# opcionales.
#############################################################################
home = xchat.get_info("xchatdir")[0:len(xchat.get_info("xchatdir"))-7]
scriptdir = xchat.get_info("xchatdir")
gatodir = scriptdir + "/gatoscript/"
filtros_path = gatodir + "antispam.conf"
consejos_path = gatodir + "consejos.txt"
configfile = gatodir + "gatoscript.conf"
rssfile = gatodir + "rss.conf"
amulesig = home + "/.aMule/amulesig.dat"
azureusstats = home + "/.azureus/Azureus_Stats.xml"
NoXmms = 0
NoDBus = 0
global DBusIniciado
DBusIniciado = 0
cp = ConfigParser()
global rbplayerobj
global rbplayer
global rbshellobj
global rbshell

#############################################################################
# Funcion para leer la configuracion del script
#############################################################################
def lee_conf(seccion, opcion):
    """Lee una opcion del archivo de configuracion.
    Argumentos:
    seccion -- cadena con el nombre de la seccion del archivo de configuracion (por defecto "comun")
    opcion  -- cadena con el nombre de la opcion que queremos leer
    """
    if (seccion == ""):
        seccion = "comun"
    cp.read(configfile)
    return cp.get(seccion, opcion)


#############################################################################
# Cargamos los modulos para la gestion multimedia
#############################################################################
repro_activo = lee_conf("media", "activo")
if (repro_activo == "1"):
    repro = lee_conf("media", "reproductor")
    if (repro == "xmms"):
        try:
            import xmms.control
        except ImportError:
            NoXmms = 1
            print "No se pudo cargar la libreria 'xmms', no funcionaran los controles de XMMS"
    elif (repro == "rhythmbox"):
        try:
            import dbus
            DBUS_START_REPLY_SUCCESS = 1
            DBUS_START_REPLY_ALREADY_RUNNING = 2
            bus = dbus.SessionBus()
        except ImportError:
            NoDBus = 1
            print "No se pudo cargar la libreria 'dbus', no funcionaran los controles de Rhythmbox"
    elif (repro == "banshee"):
        try:
            import dbus
        except ImportError:
            NoDBus = 1
            print "No se pudo cargar la libreria 'dbus', no funcionaran los controles de Banshee"


#############################################################################
# Definimos algunas funciones de uso interno en el GatoScript
#############################################################################
def gprint(mensaje):
    """Escribe "Gatoscript >> " seguido de la cadena que recibe como parametro.
    Util para mostrar mensajes del script al usuario.

    Argumentos:
    mensaje -- cadena con el mensaje a mostrar
    """
    g_mensaje = "GatoScript >> " + mensaje
    print(g_mensaje)
    return ""

def priv_imprime(mensajes):
    """Escribe una o mas lineas en la pestaña "GatoScript". Util para mostrar
    mensajes largos sin que se pierdan entre los recibidos en los canales, asi
    como menus de opciones.

    Argumentos:
    mensajes -- array de cadenas
    """
    contexto = xchat.find_context(channel="GatoScript")
    if contexto == None:
        xchat.command("query -nofocus GatoScript")
        contexto = xchat.find_context(channel="GatoScript")
    for mensaje in mensajes:
        contexto.prnt(mensaje)
    return ""

def priv_linea(mensaje):
    """Escribe una en la pestaña "GatoScript". Util para mostrar mensajes
    cortos sin que se pierdan entre los recibidos en los canales.

    Argumentos:
    mensaje -- cadena con el mensaje
    """
    contexto = xchat.find_context(channel="GatoScript")
    if contexto == None:
        xchat.command("query -nofocus GatoScript")
        contexto = xchat.find_context(channel="GatoScript")
    contexto.prnt(mensaje)
    return ""

def escribe_conf(seccion, opcion, valor):
    """Guarda una opcion en el archivo de configuracion.
    Argumentos:
    seccion -- cadena con el nombre de la seccion del archivo de configuracion (por defecto "comun")
    opcion  -- cadena con el nombre de la opcion que queremos guardar
    valor   -- cadena con el valor que queremos asignar a esa opcion
    """
    if (seccion == ""):
        seccion = "comun"
    cp.read(configfile)
    cp.set(seccion, opcion, valor)
    cp.write(file(configfile, "w"))

def expulsa(mensaje, ban, word):
    if mensaje != "":
        if ban == "":
            ban = lee_conf("protecciones", "ban")
        if ban == "1":
            partes = word[0][1:].split("@")
            comando = "ban *!*@" + partes[len(partes)-1]
            xchat.command(comando)
        partes = word[0][1:].split("!")
        comando = "kick " + partes[0] + mensaje
        xchat.command(comando)


#############################################################################
# Cargamos la lista de filtros para el antispam
#############################################################################
if path.exists(filtros_path):
    spam_gen = file(filtros_path, "r")
    filtros = spam_gen.read().split("\n")
    spam_gen.close()
    antispam = 1
else:
    print("No se puede cargar la lista de filtros, AntiSpam desactivado")
    antispam = 0
    

#############################################################################
# Definimos las funciones de informacion y ayuda sobre el manejo del script
#############################################################################
def gato_cb(word, word_eol, userdata):
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
    elif info_param < 2:
        mensajes = [
        "",
        "Añada uno de los siguientes parametros en funcion del tipo de ayuda que quiera",
        "    -g         Comandos para informacion del GatoScript",
        "    -a         Comandos para Antispam",
        "    -m         Comandos para informacion de reproductores Multimedia",
        "    -s         Comandos para informacion del Sistema",
        "    -c         Comandos para uso de los Consejos del Gato",
        "    -d         Comandos para informacion de Descargas",
        "    -u         Comandos para control de Usuarios",
        "    -o         Comandos para establecer las Opciones",
        "    -r         Comandos para gestion RSS",
        "",
        "Por ejemplo: /gato -s",
        ""]
    else:
        if word[1] == "-g":
            mensajes = [
            "",
            "Informacion:",
            "    /gato:               Muestra esta informacion",
            "    /ginfo:              Muestra en el canal activo la publicidad sobre el script",
            ""]
        elif word[1] == "-a":
            mensajes = [
            "",
            "    /antiadd <cadena>: Añade una cadena al filtro AntiSpam",
            "    /antidel <cadena>: Elimina una cadena del filtro AntiSpam",
            "    /antilist:     Muestra la lista de filtros",
            ""]
        elif word[1] == "-m":
            mensajes = [
            "",
            "Multimedia:",
            "    /escuchando:         Muestra en el canal activo la cancion que se esta reproduciendo",
            "    /reproductor:        Nos informa del reproductor seleccionado",
            "    /siguiente:          Cambia a la cancion siguiente",
            "    /anterior:           Cambia a la cancion anterior",
            "    /pausa:              Pausa la reproduccion",
            "    /play:               Reanuda la reproduccion",
            "    /stop:               Detiene la reproduccion",
            ""]
        elif word[1] == "-s":
            mensajes = [
            "",
            "Informacion del sistema:",
            "    /gup:                Muestra el uptime del sistema",
            "    /gos:                Muestra la distribucion y su version",
            "    /gsoft:              Muestra en el canal la version de los programas mas importantes",
            "    /gpc:                Muestra en el canal informacion sobre el hardware del pc",
            "    /hora:               Muestra en el canal la hora del sistema",
            ""]
        elif word[1] == "-c":
            mensajes = [
            "",
            "Consejos:",
            "    /consejos:           Muestra un consejo aleatorio",
            "    /consejo <opcion>:   Muestra el consejo que concuerde con la opcion especificada",
            "        Las opciones disponibles son: preguntar, ayudar, noayudar, planteamiento, manual, manual2, manual3, manual4 y buscador",
            ""]
        elif word[1] == "-d":
            mensajes = [
            "",
            "Descargas",
            "    /amule:             Muestra la informacion de aMule",
            "    /azureus:           Muestra la informacion de Azureus",
            ""]
        elif word[1] == "-u":
            mensajes = [
            "",
            "Control de usuarios",
            "    /kbtemp <nick>:              Baneo de 5 minutos y pateo",
            "    /kbtemp <nick> <mensaje>:    Baneo de 5 minutos y pateo con mensaje",
            ""]
        elif word[1] == "-o":
            mensajes = [
            "",
            "Opciones del script",
            "    /opciones:                   Muestra las opciones actuales",
            "    /opciones media on:          Se activan los controles multimedia",
            "    /opcion media off:           Se desactivan los controles multimedia",
            "    /opciones media xmms:        Selecciona XMMS como reproductor de sonido",
            "    /opciones media rhythmbox:   Selecciona Rhythmbox como reproductor de sonido",
            "    /opciones media banshee:     Selecciona Banshee como reproductor de sonido",
            ""]
        elif word[1] == "-r":
            mensajes = [
            "",
            "Gestion RSS",
            "    /rss:             Muestra las noticias actuales en los feeds actuales",
            "    /rsslista:        Muestra la lista de feeds actuales",
            "    /rssadd:          Añade un nuevo feed a la lista (No disponible aun)",
            "    /rssdel:          Elimina un feed de la lista actual (No disponible aun)",
            ""]
        else:
            mensajes = [
            "",
            "Parametro no soportado",
            ""]
    priv_imprime(mensajes)
    return xchat.EAT_ALL

def gato_info_cb(word, word_eol, userdata):
    """Muestra la publicidad del GatoScript
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook
    word_eol -- array de cadenas que envia xchat a cada hook
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    version = xchat.get_info("version")
    xchat.command("say (X-Chat) %s - ( Script ) GatoScript %s, script en python para X-Chat (http://www.gatoloko.org)" %(version, __module_version__))
    return xchat.EAT_ALL


#############################################################################
# Definimos las funciones de proteccion
#############################################################################
# Proteccion multiple en contra mensajes molestos (on PRIVMSG)
def anti_ctcp_cb(word, word_eol, userdata):
    """Detecta el envio de CTCPs a #ubuntu y #gatoscript y expulsa al autor
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    if lee_conf("protecciones", "ctcps") == "1":
        ctcp = re.compile("\.*\", re.IGNORECASE)
        canales = lee_conf("protecciones", "canales").split(',')
        if ctcp.search(word[3]):
            for canal in canales:
                canal_re = re.compile(canal[1:], re.IGNORECASE)
                if canal_re.search(word[2]):
                    gprint("Se ha recibido un CTCP al canal " + word[2])
                    partes = word[0][1:].split("@")
                    comando = "ban *!*@" + partes[len(partes)-1]
                    xchat.command(comando)
                    partes = word[0][1:].split("!")
                    comando = "kick " + partes[0] + " Putos scriptkidies...."
                    xchat.command(comando)
    return xchat.EAT_NONE

def anti_hoygan_cb(word, word_eol, userdata):
    """Detecta la palabra "hoygan" en los canales y banea al autor
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    if lee_conf("protecciones", "hoygan") == "1":
        hoyga = re.compile("hoyga", re.IGNORECASE)
        if hoyga.search(word_eol[3]):
            #noban = 0
            #mensaje = " Los 'HOYGAN' no son graciosos"
            partes = word[0][1:].split("@")
            xchat.command("ban *!*@" + partes[len(partes)-1])
            partes = word[0][1:].split("!")
            xchat.command("kick " + partes[0] + " Los hoygan no son graciosos")
    return xchat.EAT_NONE

def anti_mayusculas_cb(word, word_eol, userdata):
    """Detecta el abuso de mayusculas en los canales y banea al autor
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook (ignorado)
    word_eol -- array de cadenas que envia xchat a cada hook
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    if lee_conf("protecciones", "mayusculas") == "1":
        mensaje = ""
        cadena = word_eol[3][1:]
        accion = re.compile('^\ACTION')
        if accion.match(cadena):
            cadena = cadena[7:]
        if (len(cadena) > 10 and cadena.isupper() == True):
            mensaje = " Abuso de mayusculas"
        expulsa(mensaje, ban, word)
        #if mensaje != "":
            #if lee_conf("protecciones", "ban") == "1":
                #partes = word[0][1:].split("@")
                #comando = "ban *!*@" + partes[len(partes)-1]
                #xchat.command(comando)
            #partes = word[0][1:].split("!")
            #comando = "kick " + partes[0] + mensaje
            #xchat.command(comando)
    return xchat.EAT_NONE

def proteccion_cb(word, word_eol, userdata):
    """Detecta el envio de CTCPs a #ubuntu y #gatoscript y expulsa al autor
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    mensaje = ""
    noban = 0
    webs = [
    "http://www.geocities.com/octubre122005",
    "www.dominiosteca.biz",
    "es-facil.com/ganar",
    "WWW.ELECTRIKSOUND.COM",
    "http://www.fororelax.net"
    ]
    cantidad = len(webs)
    for i in range(cantidad):
        #if find(word_eol[3], webs[i]) > 0:
        if word_eol[3].find(webs[i]) > 0:
            ban = 0
            mensaje = " El spam es molesto, metetelo por el culo"
    away = [ "autoaway" ]
    cantidad = len(away)
    for i in range(cantidad):
        if word_eol[3].find(webs[i]) > 0:
            ban = 0
            mensaje = " Quita los mensajes de away automaticos, si no estas callate"
    expulsa(mensaje, ban, word)

    return xchat.EAT_NONE

# Anti ClonerX  (on JOIN)
def anti_clonerx_cb(word, word_eol, userdata):
    """Detecta nicks que entran al canal con un indent que concuerde con los de ClonerX y los banea para evitar el flood
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    canal = word[2][1:]
    contexto = xchat.find_context(channel=canal)
    bots = re.compile("^[a-z]{1}(\d){2,4}$")
    ident = word[0][1:].split("!")[1].split("@")[0]
    host = word[0].split("@")[1]
    if bots.search(ident):
        comando = "ban *!*@" + host
        contexto.command(comando)
        mensaje = "Ident de ClonerX en " + canal
        gprint(mensaje)
    return xchat.EAT_NONE
    
def anti_away_cb(word, word_eol, userdata):
    """Detecta mensajes de ausencia en el canal y expulsa al usuario
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se envia a un hook (ignorado)
    """
    away = [ "autoaway" ]
    cantidad = len(away)
    for i in range(cantidad):
        if word_eol[3].find(webs[i]) > 0:
            noban = 0
            mensaje = " Quita los mensajes de away automaticos, si no estas callate"
    


#############################################################################
# Redireccion de resaltados
#############################################################################
def resaltados_cb(word, word_eol, userdata):
    """Detecta palabras resaltadas (en la configuracion del xchat) y copia la linea que las contiene a la pestaña "GatoScript"
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook
    word_eol -- array de cadenas que envia xchat a cada hook
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    resaltados = xchat.get_prefs("irc_extra_hilight")
    if resaltados != '':
        resaltados = xchat.get_prefs("irc_extra_hilight").split(",")
        canal = word[2]
        if canal[0] == "#":
            for resaltado in resaltados:
                palabra = re.compile(resaltado, re.IGNORECASE)
                if palabra.search(word_eol[3][1:]):
                    nick = word[0].split("!")[0][1:]
                    mensaje = nick + " ha mencionado '" + resaltado + "' en " + canal + ": " + "<" + nick + "> " + word_eol[3][1:]
                    priv_linea(mensaje)
#    print resaltados
    return xchat.EAT_NONE


#############################################################################
# Definimos la funcion antispam para filtrado de mensajes privados.
# El sistema antispam eliminara todas las lineas que contengan alguna de las
# cadenas definidas en el archivo antispam.conf
#############################################################################
def antispam_reload():
    """Recarga la lista de filtros antispam para aplicar los cambios o retomar una lista anterior
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook (ignorado)
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    global filtros
    if path.exists(filtros_path):
        spam_gen = file(filtros_path, "r")
        filtros = spam_gen.read().split("\n")
        spam_gen.close()
        antispam = 1
        #print filtros
    else:
        gprint("No se puede cargar la lista de filtros, AntiSpam desactivado")
        antispam = 0

def antispam_cb(word, word_eol, userdata):
    """Compara las lineas que se reciben con una lista de filtros y elimina aquellas que coincidan
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook (ignorado)
    word_eol -- array de cadenas que envia xchat a cada hook
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    global filtros
    if (antispam == 1):
        texto = word_eol[3][1:]
        for linea in filtros[0:len(filtros)-1]:
            spam_exp = re.compile(".*"+linea[0:len(linea)-1]+".*", re.IGNORECASE)
            if (spam_exp.search(texto)):
                return xchat.EAT_ALL

def antispam_add_cb(word, word_eol, userdata):
    """Añade un nuevo filtro al final de la lista para usarse con el sistema antispam.
    Esta funcion no comprueba si el nuevo filtro ya existe, simplemente lo añade al final.

    Argumentos:
    word     -- array de palabras que envia xchat a cada hook
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    global filtros
    spam = open(filtros_path, "a")
    spam.write(word[1] + "\n")
    mensaje = "Se ha añadido '" + word[1] + "' a la lista de filtros"
    priv_linea(mensaje)
    spam.close
    del spam
    del mensaje
    antispam_reload()
    return xchat.EAT_ALL

def antispam_del_cb(word, word_eol, userdata):
    """Elimina un filtro de la lista que se usa con el sistema antispam.
    Esta funcion no verifica si hay duplicados, elimina todas las ocurrencias del filtro.

    Argumentos:
    word     -- array de palabras que envia xchat a cada hook (ignorado)
    word_eol -- array de cadenas que envia xchat a cada hook
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    global filtros
    if path.exists(filtros_path):
        spam = file(filtros_path, "r")
        memoria = spam.read().split("\n")
        spam.close()
        spam = file(filtros_path, "w")
        for linea in range(len(memoria)):
            if (memoria[linea] != word_eol[1]) and (memoria[linea] != ""):
                spam.write(memoria[linea] + "\n")
        spam.close()
        mensaje = "Se ha eliminado '" + word_eol[1] + "' de la lista de filtros"
        priv_linea(mensaje)
        del memoria
        del linea
        del spam
        del mensaje
        antispam_reload()
    else:
        gprint("Falta el archivo de filtros")
    return xchat.EAT_ALL

def antispam_list_cb(word, word_eol, userdata):
    """Muestra, en la pestaña "GatoScript", todas las lineas de la lista de filtros antispam.
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook (ignorado)
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    global filtros
    cuenta_lineas = 1
    priv_linea("\nLista de filtros:")
    for filtro in filtros[0:len(filtros)-1]:
        mensaje = "Filtro %s: %s" % (cuenta_lineas, filtro)
        priv_linea(mensaje)
        cuenta_lineas = cuenta_lineas + 1
    priv_linea("")
    del mensaje
    del cuenta_lineas
    return xchat.EAT_ALL


#############################################################################
# Definimos la funcion para redireccion y formateo de respuestas al whois
#############################################################################
# Respuesta al whois: Informacion de usuario
def whois_cb(word, word_eol, userdata):
    """Redirecciona las respuestas al "whois" hacia la ventana activa, al tiempo que modifica el formato de salida.
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook
    word_eol -- array de cadenas que envia xchat a cada hook
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    whois_activo = lee_conf("comun", "whois")
    if (whois_activo == "1"):
        if (word[1] == "301"):
            # Respuesta al whois: AwayMessage
            print '\0033[No disponible   ]\003 ' + word_eol[4][1:]
        elif (word[1] == "311"):
            # Respuesta al whois: Usuario
            nick = word[3]
            host = word[4] + "@" + word[5]
            nombre = word_eol[7][1:]
            print '\0033[Nick            ]\003 ' + nick
            print '\0033[Direccion       ]\003 ' + host
            print '\0033[Nombre real     ]\003 ' + nombre
        elif (word[1] == "312"):
            # Respuesta al whois: Servidor
            print '\0033[Servidor        ]\003 ' + word_eol[4]
        elif (word[1] == "317"):
            # Respuesta al whois: IDLE
            horas = int(word[4])/3600
            minutos = (int(word[4])-horas*3600)/60
            segundos = int(word[4])-((horas*3600)+(minutos*60))
            tiempo = str(horas) + ' horas, ' + str(minutos) + ' minutos y ' + str(segundos)
            print '\0033[IDLE            ]\003 ' + tiempo + ' segundos'
        elif (word[1] == "318"):
            # Respuesta al whois: Fin del whois
            print '\0033Fin del WHOIS\003'
        elif (word[1] == "319"):
            # Respuesta al whois: Canales
            print '\0033[Canales         ]\003 ' + word_eol[4][1:]
        elif (word[1] == "320"):
            # Respuesta al whois: Especial
            espacios = 15 - len(word[3])
            cadena = " "
            for i in range(espacios):
                cadena = cadena + " "
            print '\0033[' + word[3] + cadena + ']\003 ' + word_eol[4][1:]
        elif (word[1] == "335"):
            # Respuesta al whois: Bot
            print '\0033' + word_eol[0] + '\003'
        elif (word[1] == "307"):
            # Respuesta al whois: RegNick
            espacios = 15 - len(word[3])
            cadena = " "
            #if (espacios > 1):
            for i in range(espacios):
                cadena = cadena + " "
            print '\0033[' + word[3] + cadena + '] \003' + word_eol[4][1:]
        elif (word[1] == "342"):
            # Respuesta al whois: Solo admite privados de usuarios registrados
            espacios = 15 - len(word[3])
            cadena = " "
            #if (espacios > 1):
            for i in range(espacios):
                cadena = cadena + " "
            print '\0033[' + word[3] + cadena + '] \003' + word_eol[4][1:]
        elif (word[1] == "378"):
            # Respuesta al whois: VHOST
            print '\0033[VHost           ]\003 ' + word_eol[6]
        elif (word[1] == "379"):
            # Respuesta al whois: whoismodes
            print '\0033[Modos           ]\003 ' + word_eol[4][1:]
        elif (word[1] == "401"):
            # Respuesta al whois: No such nick
            print '\0033El nick ' + word[3] + ' no existe o no esta conectado\003'
        else:
            # Raw no definido
            print '\0033El raw ' + word[1] + ' no esta definido'
        return xchat.EAT_ALL
    else:
        return xchat.EAT_NONE


#############################################################################
# Definimos las funciones para el control de multimedia
#############################################################################
def media_cb(word, word_eol, userdata):
    """Muestra en el canal activo informacion sobre la cancion que estamos escuchando.
    Toma del archivo de configuracion el reproductor a usar.

    Argumentos:
    word     -- array de palabras que envia xchat a cada hook (ignorado)
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
#    print userdata
    media_activo = lee_conf("media", "activo")
    if (media_activo == "1"):
        reproductor = lee_conf("media", "reproductor")
#        print reproductor
        if (reproductor == "xmms"):
            if (NoXmms == 1):
                gprint("Esta funcion esta desactivada")
            else:
                if (userdata == "escuchando"):
                    entrada, salida, error = popen3("xmms --version", "r")
                    error2 = error.readlines()
                    if len(error2) > 0:
                        gprint(error2)
                    else:
                        version = (salida.readlines())[0]
                        posicion = xmms.control.get_playlist_pos()
                        titulo = xmms.control.get_playlist_title(posicion)
                        longitud = xmms.control.get_playlist_time(posicion)/1000
                        if longitud < 0:
                            tiempo = "Radio"
                        else:
                            minutos = int(longitud/60)
                            segundos = longitud-(minutos*60)
                            tiempo = str(minutos) + "m" + str(segundos) + "s"
                        rate, frec, canal = xmms.get_info()
                        bitrate = str(rate/1000) + "Kbps"
                        frecuencia = str(frec/1000) + "KHz"
                        if canal == 1:
                            canales = "mono"
                        else:
                            canales = "estereo"
                        #print str(bitrate) + " " + str(frecuencia) + " " + str(canales) + " " + str(longitud)
                        xchat.command("me esta escuchando: %s - %s (%s\%s\%s\%s) - %s" % (posicion+1, titulo, tiempo, bitrate, frecuencia, canales, version[0:len(version)-1]))
                    del entrada, salida, error, error2
                elif (userdata == "reproductor"):
                    entrada, salida, error = popen3("xmms --version", "r")
                    error2 = error.readlines()
                    if len(error2) > 0:
                        gprint(error2)
                    else:
                        version = salida.readlines()
                    gprint(version[0])
                elif (userdata == "siguiente"):
                    xmms.control.playlist_next()
                elif (userdata == "anterior"):
                    xmms.control.playlist_prev()
                elif (userdata == "pausa"):
                    xmms.control.pause()
                elif (userdata == "play"):
                    xmms.control.play()
                elif (userdata == "stop"):
                    xmms.control.stop()
                else:
                    mensaje = "La funcion " + userdata + " no esta implementada"
                    gprint(mensaje)
        elif (reproductor == "rhythmbox"):
            global DBusIniciado
            global rbplayerobj
            global rbplayer
            global rbshellobj
            global rbshell
            if (NoDBus == 1):
                gprint("No esta disponible la libreria de acceso a Rhythmbox")
            else:
                if DBusIniciado == 0:
                    bus = dbus.SessionBus()
                    rbplayerobj = bus.get_object('org.gnome.Rhythmbox', '/org/gnome/Rhythmbox/Player')
                    rbplayer = dbus.Interface(rbplayerobj, 'org.gnome.Rhythmbox.Player')
                    rbshellobj = bus.get_object('org.gnome.Rhythmbox', '/org/gnome/Rhythmbox/Shell')
                    rbshell = dbus.Interface(rbshellobj, 'org.gnome.Rhythmbox.Shell')
                    gprint("Conectando con Rhythmbox, por favor intentelo otra vez")
                    DBusIniciado = 1
                else:
                    try:
                        sonando = int(rbplayer.getPlaying())
                    except:
                        sonando = 0
                    if (userdata == "escuchando"):
                        if sonando == 0:
                            gprint("El reproductor esta parado")
                        else:
                            detalles = rbshell.getSongProperties(rbplayer.getPlayingUri())
                            titulo = detalles['title'].encode('utf-8')
                            artista = detalles['artist'].encode('utf-8')
                            #album = detalles['album'].encode('utf-8')
                            tiempo = detalles['duration']
                            if tiempo < 0:
                                longitud = "Radio"
                            else:
                                minutos = int(tiempo/60)
                                segundos = tiempo-(minutos*60)
                                longitud = str(minutos) + "m" + str(segundos) + "s"
                            xchat.command("me esta escuchando: %s - %s (%s) - %s" %(artista, titulo, longitud, "Rhythmbox"))
                    elif (userdata == "reproductor"):
                        gprint("Esta utilizando Rhythmbox")
                    elif (userdata == "siguiente"):
                        if sonando == 0:
                            gprint("El reproductor esta parado")
                        else:
                            rbplayer.next()
                    elif (userdata == "anterior"):
                        if sonando == 0:
                            gprint("El reproductor esta parado")
                        else:
                            rbplayer.previous()
                    #elif (userdata == "play" or userdata == "pausa"):
                        #rbplayer.playPause()
                    #elif (userdata == "stop"):
                        #gprint("Esta funcion no esta implementada")
                    else:
                        mensaje = "La funcion " + userdata + " no esta implementada"
                        gprint(mensaje)
        elif (reproductor == "rhythmbox"):
            if (NoDBus == 1):
                gprint("No esta disponible la libreria de acceso a Banshee")
            else:
                if DBusIniciado == 0:
                    bus = dbus.SessionBus()
                    bansheeobj = bus.get_object('org.gnome.Banshee', '/org/gnome/Banshee/Player')
                    banshee = dbus.Interface(bansheeobj, 'org.gnome.Banshee.Core')
                    gprint("Conectando con Banshee, por favor intentelo otra vez")
                    DBusIniciado = 1
                else:
                    if (userdata == "escuchando"):
                        titulo = banshee.GetPlayingTitle().encode('utf-8')
                        artista = banshee.GetPlayingArtist().encode('utf-8')
                        #album = banshee.GetPlayingAlbum().encode('utf-8')
                        tiempo = banshee.GetPlayingDuration()
                        if tiempo < 0:
                            longitud = "Radio"
                        else:
                            minutos = int(tiempo/60)
                            segundos = tiempo-(minutos*60)
                            longitud = str(minutos) + "m" + str(segundos) + "s"
                        xchat.command("me esta escuchando: %s - %s (%s) - %s" %(artista, titulo, longitud, "Rhythmbox"))
                    elif (userdata == "reproductor"):
                        gprint("Esta utilizando Banshee")
                    elif (userdata == "siguiente"):
                        banshee.Next()
                    elif (userdata == "anterior"):
                        banshee.Previous()
                    elif (userdata == "play"):
                        banshee.Play()
                    elif (userdata == "pausa"):
                        banshee.Pause()
                    elif (userdata == "stop"):
                        banshee.Stop()
                    else:
                        mensaje = "La funcion " + userdata + " no esta implementada"
                        gprint(mensaje)
        else:
            print "El reproductor seleccionado no esta soportado (aun)"
    else:
        print "Los controles multimedia estan desactivados"
    return xchat.EAT_ALL


#############################################################################
# Definimos las funciones para el modulo "Consejos del Gato"
#############################################################################
def consejo_aleatorio_cb(word, word_eol, userdata):
    """Muestra en el canal activo una linea aleatoria del archivo de consejos.
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook (ignorado)
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    if path.exists(consejos_path):
        archivo = open(consejos_path, "r")
        consejos = archivo.readlines()
        lin = len(consejos)
        aleatorio = randint(0, lin -1)
        consejo = consejos[aleatorio]
        xchat.command("say %s" %consejo[0:len(consejo)-1])
        archivo.close()
    else:
        gprint("Falta el archivo de consejos")
    return xchat.EAT_ALL

def consejo_cb(word, word_eol, userdata):
    """ Muestra consejos en funcion de un parametro o, a falta de este,
    aleatoriamente.
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    if len(word_eol) > 1:
        if word[1] == "preguntar":
            linea = 0
        elif word[1] == "ayudar":
            linea = 1
        elif word[1] == "noayudar":
            linea = 2
        elif word[1] == "planteamiento":
            linea = 3
        elif word[1] == "manual":
            linea = 4
        elif word[1] == "manual2":
            linea = 5
        elif word[1] == "manual3":
            linea = 6
        elif word[1] == "manual4":
            linea = 7
        elif word[1] == "buscador":
            linea = 8
        else:
            linea = "no"
        if path.exists(consejos_path):
            archivo = open(consejos_path, "r")
            consejos = archivo.readlines()
            if linea == "no":
                gprint("No hay ningun consejo que concuerde")
            else:
                consejo = (consejos[linea])[0:len(consejos[linea])-1]
                xchat.command("say %s" %consejo)
        else:
            gprint("Falta el archivo de consejos")
    else:
        gprint("No ha especificado un consejo")
    return xchat.EAT_ALL

def preguntar_cb(word, word_eol, userdata):
    xchat.command("say Consejos del Gato Nº1: No preguntes si puedes preguntar, plantea tu duda y si alguien sabe la solucion y tiene ganas te la dira")
    return xchat.EAT_ALL

def ayudar_cb(word, word_eol, userdata):
    xchat.command("say Consejos del Gato Nº1.1: No preguntes si alguien te puede ayudar, plantea tu problema y si alguien sabe y tiene ganas te ayudara")
    return xchat.EAT_ALL

def noayudar_cb(word, word_eol, userdata):
    xchat.command("say Consejos del Gato Nº2: Si preguntas y nadie te contesta no te pongas a repetir, o nadie sabe la respuesta o nadie tiene ganas de responder. Repitiendo solo molestas.")
    return xchat.EAT_ALL

def planteamiento_cb(word, word_eol, userdata):
    xchat.command("say Consejos del Gato Nº3: Cuando planteas un problema o una duda, procura hacerte entender lo mas claramente posible, incluyendo la informacion que pueda afectar a tu duda y expresandote bien (nada de 'q' o 'k' en vez de 'que' y mierdas asi).")
    return xchat.EAT_ALL

def privado_cb(word, word_eol, userdata):
    xchat.command("say No atiendo privados a menos que seas una tia buenorra o rica dispuesta a casarte conmigo")
    return xchat.EAT_ALL

def web_cb(word, word_eol, userdata):
    xchat.command("say http://www.gatoloko.org")
    return xchat.EAT_ALL

def repos_cb(word, word_eol, userdata):
    xchat.command("say deb http://www.gatoloko.org/repositorio/ VERSION RAMAS")
    xchat.command("say donde VERSION puede ser 'dapper', 'edgy' o 'feisty'")
    xchat.command("say donde RAMAS puede ser una o mas de: 'estable', 'inestable'")
    return xchat.EAT_ALL

def autent_cb(word, word_eol, userdata):
    xchat.command("say gpg --keyserver subkeys.pgp.net --recv-keys B3B042E7")
    xchat.command("say gpg --armor --export B3B042E7 | sudo apt-key add -")
    xchat.command("say sudo apt-get update")
    return xchat.EAT_ALL

#############################################################################
# Definimos las funciones del lector rss
#############################################################################
def rss_cb(word, word_eol, userdata):
    """ Muestra las noticias actuales contenidas en los feeds que hemos
    configurado en la pestaña/ventana GatoScript.
    aleatoriamente.
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    servidores = lee_conf("rss", "feeds").split(',')
    fecha = str(datetime.datetime.now())[:19]
    for servidor in servidores:
        priv_linea(servidor + " - " + fecha)
        priv_linea("")
        archivo = xml.dom.minidom.parse(urlopen(servidor))
        for objeto in archivo.getElementsByTagName('item'):
            titulo = objeto.getElementsByTagName('title')[0].firstChild.data
            enlace = objeto.getElementsByTagName('link')[0].firstChild.data
            priv_linea("Enlace: " + enlace.encode('latin-1', 'replace') + " <--> Titulo: " + titulo.encode('latin-1', 'replace'))
        priv_linea("")
    del servidores, fecha, servidor
    return xchat.EAT_ALL

def rsslista_cb(word, word_eol, userdata):
    """ Muestra la lista de feeds RSS/RDF que tenemos configurados.
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    servidores = lee_conf("rss", "feeds").split(',')
    priv_linea("")
    priv_linea("Lista de feeds RSS:")
    for servidor in servidores:
        priv_linea(servidor)
    priv_linea("")
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
        gprint("Debes añadir la direccion de un feed RSS")
    elif info_param > 2:
        gprint("De momento solo se admite un rss cada vez")
    else:
        #comprobar si el parametro es una url
        #if word[1] == "es una url":
        actuales = lee_conf("rss", "feeds")
        nuevos = actuales + "," + word[1]
        escribe_conf("rss", "feeds", nuevos)
        gprint("Se ha agregado '" + word[1] + "' a la lista de feeds")
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
        gprint("Debes añadir la direccion de un feed RSS")
    elif info_param > 2:
        gprint("De momento solo se admite un feed cada vez")
    else:
        actuales = lee_conf("rss", "feeds").split(',')
        try:
            actuales.remove(word_eol[1])
            temporal = ""
            for feed in range(len(actuales)):
                if (actuales[feed] != word_eol[1]) and (actuales[feed] != ""):
                    temporal = temporal + actuales[feed]
                    if feed < len(actuales)-1:
                        temporal = temporal + ','
            escribe_conf("rss", "feeds", temporal)
            gprint("Se ha eliminado '" + word_eol[1] + "'")
            del actuales, temporal, feed
        except ValueError:
            gprint("No existe ningun feed que coincida con el indicado")
    return xchat.EAT_ALL

#############################################################################
# Definimos las funciones para obtener la informacion del sistema
#############################################################################
def uptime_cb(word, word_eol, userdata):
    """Muestra en el canal activo el uptime del pc.
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook (ignorado)
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    archivo_uptime = open("/proc/uptime", "r")
    lineas_uptime = archivo_uptime.readline()
    archivo_uptime.close()
    uptime = eval((lineas_uptime.split())[0])
    resto_dias = uptime % 86400
    dias = int(uptime / 86400)
    if dias < 1:
        horas = int(uptime / 3600)
        resto_horas = int(uptime % 3600)
        minutos = int(resto_horas / 60)
        xchat.command("say ( Uptime ) %s horas y %s minutos" %(horas, minutos))
    else:
        if dias > 1:
            cadena_dias = "dias"
        else:
            cadena_dias = "dia"
        horas = int(resto_dias / 3600)
        resto_horas = int(resto_dias % 3600)
        minutos = int(resto_horas / 60)
        xchat.command("say ( Uptime ) %s %s, %s horas y %s minutos" %(dias, cadena_dias, horas, minutos))
    return xchat.EAT_ALL

def sistema_cb(word, word_eol, userdata):
    """Muestra en el canal activo informacion sobre el sistema operativo que usamos.
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook (ignorado)
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    if path.exists("/etc/lsb-release"):
        LSB = open("/etc/lsb-release", "r")
        lineas_LSB = LSB.readlines()
        LSB.close()
        distro = (lineas_LSB[0])[11:len(lineas_LSB[0])-1]
        version = (lineas_LSB[1])[16:len(lineas_LSB[1])-1]
        codigo = (lineas_LSB[2])[17:len(lineas_LSB[2])-1]
        entrada, salida, error = popen3("uname -r", "r")
        error2 = error.readlines()
        if len(error2) > 0:
            gprint(error2)
        else:
            kernel = salida.readlines()
            kernel2 = (kernel[0])[0:len(kernel[0])-1]
        xchat.command("say ( Distribucion ) %s   ( Version ) %s %s   ( Kernel ) %s" %(distro, version, codigo, kernel2))
    else:
        gprint("La distribucion no cumple con LSB")
    return xchat.EAT_ALL

def software_cb(word, word_eol, userdata):
    """Muestra en el canal activo informacion sobre las versiones del software basico.
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook (ignorado)
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    entrada, salida, error = popen3("uname -sr", "r")
    error2 = error.readlines()
    if len(error2) > 0:
        for i in range(len(error2)):
            gprint(error2[i])
        sistema = "Indeterminable"
    else:
        uname = salida.readlines()
        sistema = (uname[0])[0:len(uname[0])-1]
    entrada, salida, error = popen3("/lib/libc.so.6", "r")
    error2 = error.readlines()
    if len(error2) > 0:
        for i in range(len(error2)):
            gprint(error2[i])
        libc = "Indeterminable"
    else:
        libc_text = salida.readlines()
        if libc_text[0].split()[0] == "GNU":
            licencia = "GLIBC"
        libc = licencia + " " + libc_text[0].split()[6][:-1]
    entrada, salida, error = popen3("xdpyinfo | grep version:", "r")
    error2 = error.readlines()
    if len(error2) > 0:
        for i in range(len(error2)):
            gprint(error2[i])
        X11 = "Indeterminable"
    else:
        xserver = salida.readlines()
        servidor = xserver[0].split()
    entrada, salida, error = popen3('xdpyinfo | grep "vendor string"', "r")
    error2 = error.readlines()
    if len(error2) > 0:
        for i in range(len(error2)):
            gprint(error2[i])
        xversion = "Indeterminable"
    else:
        x_version = salida.readlines()
        xversion = x_version[0].split()
        X11 = xversion[3] + " " + servidor[len(servidor)-1]
    entrada, salida, error = popen3("gcc --version", "r")
    error2 = error.readlines()
    if len(error2) > 0:
        for i in range(len(error2)):
            gprint(error2[i])
        gcc = "Indeterminable"
    else:
        gcc_out = salida.readlines()
        if gcc_out[0] == "bash: gcc: command not found":
            gcc = "No instalado"
        else:
            gcc_partes = gcc_out[0].split()
            gcc = gcc_partes[2]
    xchat.command("say ( Sistema ) %s - ( LIBC ) %s - ( X11 ) %s - ( GCC ) %s" %(sistema, libc, X11, gcc))
    del entrada, salida, error
    return xchat.EAT_ALL

def fecha_cb(word, word_eol, userdata):
    """Muestra, en la pestaña "GatoScript", todas las lineas de la lista de filtros antispam.
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook (ignorado)
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    entrada, salida, error = popen3("date")
    error2 = error.readlines()
    if len(error2) > 0:
        for i in range(len(error2)):
            gprint(error2[i])
    else:
        fecha = salida.readlines()
        xchat.command("say %s" % (fecha[0][:-1]))
    del entrada, salida, error
    return xchat.EAT_ALL

def pc_cb(word, word_eol, userdata):
    """Muestra en el canal activo, informacion sobre el pc.
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook (ignorado)
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    # CPU
    cpuinfo = file("/proc/cpuinfo")
    archivo = cpuinfo.readlines()
    cpu = archivo[4].split(":")[1][1:-1]
    velocidad = archivo[6].split(":")[1][1:-1]
    # Memoria
    meminfo = file("/proc/meminfo")
    archivo = meminfo.readlines()
    partes = archivo[0].split(":")[1][:-1].split(" ")
    memoria = partes[len(partes)-2]
    unidad = partes[len(partes)-1]
    # Free
    partes = archivo[1].split(":")[1][:-1].split(" ")
    freemem = partes[len(partes)-2]
    # Buffer
    partes = archivo[2].split(":")[1][:-1].split(" ")
    bufmem = partes[len(partes)-2]
    # Cache
    partes = archivo[3].split(":")[1][:-1].split(" ")
    cachemem = partes[len(partes)-2]
    # Usada y libre
    usada = int(freemem) + int(bufmem) + int(cachemem)
    libre = int(memoria) - usada
    # Mensaje
    mensaje = "[Informacion del PC] CPU: " + cpu + " - Velocidad: " + velocidad + "MHz - Memoria instalada: " + memoria + unidad + " - Memoria usada: " + str(libre) + unidad
    xchat.command("say " + mensaje)
    return xchat.EAT_ALL

def red_cb(word, word_eol, userdata):
    """Muestra en el canal activo, informacion sobre la red.
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook (ignorado)
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    hostname = file("/etc/hostname").read()
    gprint("( Hostname ) " + hostname)


#############################################################################
# Funcion para el Kick/Ban temporal
#############################################################################
def kbtemporal_cb(word, word_eol, userdata):
    """Expulsa de forma temporal a un usuario del canal activo (si somos Operadores).
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook
    word_eol -- array de cadenas que envia xchat a cada hook
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    #gprint(len(word_eol))
    if (len(word_eol) > 2):
        xchat.command("ban %s!*@*" %word[1])
        xchat.command("kick %s Expulsado 5 minutos (%s)" %(word[1], word_eol[2]))
        xchat.command("timer -repeat 1 300 unban %s!*@*" %word[1])
    elif (len(word_eol) > 1):
        xchat.command("ban %s!*@*" %word[1])
        xchat.command("kick %s Expulsado 5 minutos" %word[1])
        xchat.command("timer -repeat 1 300 unban %s!*@*" %word[1])
    else:
        gprint("Hay que especificar un nick a patear")
    return xchat.EAT_ALL


#############################################################################
# Definimos las funciones para mostrar informacion P2P
#############################################################################
def amule_cb(word, word_eol, userdata):
    """Lee el archivo onlinesig (firma online) de amule y muestra parte de la informacion en el canal activo.
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook (ignorado)
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    if path.exists(amulesig):
        datos_amule = open(amulesig, "r")
        lineas_amule = datos_amule.readlines()
        datos_amule.close()
        if lineas_amule[0] == "0":
            gprint("No estas conectado a aMule")
        else:
            vdescarga = (lineas_amule[6])[0:len(lineas_amule[6])-1]
            vsubida = (lineas_amule[7])[0:len(lineas_amule[7])-1]
            desc_len = len(lineas_amule[11]) - 1
            if (int(lineas_amule[11]) < 1048576):
                total_descargado = str(lineas_amule[11][0:desc_len]) + 'Bytes'
            elif (int(lineas_amule[11][0:desc_len]) >= 1048576) and (int(lineas_amule[11][0:desc_len]) < 1073741824):
                total_descargado = str(int((lineas_amule[11])[0:desc_len])/1048576) + 'MB'
            else:
                total_descargado = str(int((lineas_amule[11])[0:desc_len])/1073741824) + 'GB'
            version = lineas_amule[13][0:len(lineas_amule[13]) - 1]
            xchat.command("say ( aMule %s ) Descarga: %sKB/s - Subida: %sKB/s - Total descargado: %s" %(version, vdescarga, vsubida, total_descargado))
    else:
        gprint("No existe el archivo " + amulesig + ", compruebe que activo la firma online en la configuracion de aMule")
    return xchat.EAT_ALL

def azureus_cb(word, word_eol, userdata):
    """Lee el archivo Azureus_Stats.xml (estadisticas) de azureus y muestra
    parte de la informacion en el canal activo.
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook (ignorado)
    word_eol -- array de cadenas que envia xchat a cada hook (ignorado)
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    if path.exists(azureusstats):
        dom1 = xml.dom.minidom.parse(azureusstats)
        stats = dom1.getElementsByTagName('STATS')[0]
        glob = stats.getElementsByTagName('GLOBAL')[0]
        descarga = glob.getElementsByTagName('DOWNLOAD_SPEED')[0]
        vdescarga = descarga.getElementsByTagName('TEXT')[0].firstChild.data
        subida = glob.getElementsByTagName('UPLOAD_SPEED')[0]
        vsubida = subida.getElementsByTagName('TEXT')[0].firstChild.data
        xchat.command("say ( Azureus ) Descarga: %s - Subida: %s" %(vdescarga, vsubida))
        del descarga, vdescarga, subida, vsubida, glob, stats, dom1
    else:
        gprint("No existe el archivo " + azureusstats + ", compruebe su configuracion de Azureus")
    return xchat.EAT_ALL


#############################################################################
# Definimos las funcion de controles remotos
#############################################################################
def remoto_cb(word, word_eol, userdata):
    """Esta funcion revisa los mensajes recibidos en busca de comandos remotos y cuando los encuentra, actua en consecuencia.
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook
    word_eol -- array de cadenas que envia xchat a cada hook
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    remotos_activo = lee_conf("comun", "remotos")
    if (remotos_activo == "1"):
        #Definimos la expresion regular que actuara como activador
        consejo_rem = re.compile("!consejo", re.IGNORECASE)
        gay_rem = re.compile ("!hola gay", re.IGNORECASE)
        hola_rem = re.compile("!hola", re.IGNORECASE)
        version_rem = re.compile("!version", re.IGNORECASE)
    #    sexo_rem = re.compile("!sexo", re.IGNORECASE)
        #Si se ha encontrado actuamos
        if consejo_rem.search(word[1]):
            consejo_aleatorio_cb("0", "0", "0")
        elif gay_rem.search(word[1]):
            xchat.command("say Otra vez buscando gays que te enculen?")
        elif hola_rem.search(word[1]):
            xchat.command("say Hola %s!!" %word[0])
        elif version_rem.search(word[1]):
            software_cb("", "", "")
            xchat.command("say (GatoScript) %s" % __module_version__)
    #    elif sexo_rem.search(word[1]):
    #       if word[0][3:] == "_CHRiSTiN":
    #            xchat.command("say _CHRiSTiN le echaria un polvo magico a GatoLoko pero no sabe como decirselo (GatoBotijo)")
    #        if word[0][3:] == "VeRiTTo":
    #            print word[0]
    #            xchat.command("say VeRiTTo le echaria un polvo a GatoLoko pero no sabe como decirselo (GatoBotijo)")
    #        else:
    #            print word[0]
    #            xchat.command("say a %s le gustaria echar un polvo pero no tiene con quien (GatoBotijo)" %word[0])


#############################################################################
# Configuracion del script
#############################################################################
def opciones_cb(word, word_eol, userdata):
    """Esta funcion se encarga de mostrar y modificar las configuraciones del script.
    Argumentos:
    word     -- array de palabras que envia xchat a cada hook
    word_eol -- array de cadenas que envia xchat a cada hook
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    info_param = len(word_eol)
    if info_param == 1:
        cp.read(configfile)
        priv_linea("")
        priv_linea("A continuacion se mostraran las secciones y opciones de configuracion:")
        for seccion in cp.sections():
            priv_linea(seccion)
            for opcion in cp.options(seccion):
                mensaje =  " " + opcion + "=" + cp.get(seccion, opcion)
                priv_linea(mensaje)
        priv_linea("")
    elif info_param == 2:
        if word[1] == "prueba":
            print "Prueba con un solo parametro"
        else:
            print "Parametro erroneo"
    elif info_param == 3:
        if word[1] == "media":
            if word[2] == "xmms":
                escribe_conf("media", "reproductor", "xmms")
                gprint("Se ha seleccionado XMMS")
                if NoXmms == 1:
                    try:
                        import xmms.control
                    except ImportError:
                        NoXmms = 1
                        gprint("No se pudo cargar la libreria 'xmms', no funcionaran los controles de XMMS")
            elif word[2] == "rhythmbox":
                escribe_conf("media", "reproductor", "rhythmbox")
                gprint("Se ha seleccionado Rythmbox")
            elif word[2] == "banshee":
                escribe_conf("media", "reproductor", "banshee")
                gprint("Se ha seleccionado Banshee")
            elif word[2] == "on":
                escribe_conf("media", "activo", "1")
                gprint("Controles multimedia activados")
            elif word[2] == "off":
                escribe_conf("media", "activo", "0")
                gprint("Controles multimedia desactivados")
            else:
                gprint("Parametro erroneo")
        elif word[1] == "debug":
            if word[2] == "on":
                escribe_conf("comun", "debug", "1")
                xchat.command("py console")
            elif word[2] == "off":
                escribe_conf("comun", "debug", "0")
    else:
        gprint("No mostramos nada")
    return xchat.EAT_ALL


#############################################################################
# Definimos la funcion para la descarga del programa
#############################################################################
def unload_cb(userdata):
    """Esta funcion debe desenlazar todas las funciones del GatoScript al descargarse el script
    Argumentos:
    userdata -- variable opcional que se puede enviar a un hook (ignorado)
    """
    # Desconectamos los comandos
    # Controles remotos
    xchat.unhook(hookremoto)
    # Informacion del script
    xchat.unhook(hook11)
    xchat.unhook(hook12)
    # Protecciones
    xchat.unhook(hookproteccion)
    xchat.unhook(hookanticlonerx)
    xchat.unhook(hootantictcp)
    xchat.unhook(hookantihoygan)
    xchat.unhook(hookantimayusculas)
    # Resaltados
    xchat.unhook(hookresaltados)
    # Antispam
    xchat.unhook(hook21)
    xchat.unhook(hook22)
    xchat.unhook(hook23)
    xchat.unhook(hook24)
    # Whois
    xchat.unhook(raw301)
    xchat.unhook(raw307)
    xchat.unhook(raw310)
    xchat.unhook(raw311)
    xchat.unhook(raw312)
    xchat.unhook(raw313)
    xchat.unhook(raw316)
    xchat.unhook(raw317)
    xchat.unhook(raw318)
    xchat.unhook(raw319)
    xchat.unhook(raw320)
    xchat.unhook(raw335)
    xchat.unhook(raw342)
    xchat.unhook(raw378)
    xchat.unhook(raw379)
    xchat.unhook(raw401)
    # Media
    xchat.unhook(hookescuchando)
    xchat.unhook(hookreproductor)
    xchat.unhook(hooksiguiente)
    xchat.unhook(hookanterior)
    xchat.unhook(hookplay)
    xchat.unhook(hookpausa)
    xchat.unhook(hookstop)
    # Peer to Peer
    xchat.unhook(hookamule)
    xchat.unhook(hookazureus)
    # Consejos
    xchat.unhook(hook31)
    xchat.unhook(hook32)
    xchat.unhook(hook33)
    xchat.unhook(hook34)
    xchat.unhook(hook35)
    xchat.unhook(hook36)
    xchat.unhook(hook37)
    xchat.unhook(hook38)
    xchat.unhook(hook39)
    xchat.unhook(hook30)
    # Lector de feeds RSS
    xchat.unhook(hookrss)
    xchat.unhook(hooklistarss)
    xchat.unhook(hookrssadd)
    xchat.unhook(hookrssdel)
    # Informacion del sistema
    xchat.unhook(hook51)
    xchat.unhook(hook52)
    xchat.unhook(hook53)
    xchat.unhook(hookpc)
    xchat.unhook(hooknet)
    # Kick/Ban temporal
    xchat.unhook(hook71)
    # Opciones del script
    xchat.unhook(hookopciones)
    # Descarga
    xchat.unhook(hook81)
    xchat.command("menu del GatoScript")
    print "Se ha descargado GatoScript %s" % __module_version__


#############################################################################
# Conectamos los "lanzadores" de xchat con las funciones que hemos definido
# para ellos
#############################################################################

# Controles remotos
hookremoto = xchat.hook_print('Channel Message', remoto_cb)
# Informacion del script
hook11 = xchat.hook_command('gato', gato_cb)
hook12 = xchat.hook_command('ginfo', gato_info_cb)
# Protecciones
hookproteccion = xchat.hook_server('PRIVMSG', proteccion_cb, userdata=None)
hookanticlonerx = xchat.hook_server('JOIN', anti_clonerx_cb, userdata=None)
hootantictcp = xchat.hook_server('PRIVMSG', anti_ctcp_cb, userdata=None)
hookantihoygan = xchat.hook_server('PRIVMSG', anti_hoygan_cb, userdata=None)
hookantimayusculas = xchat.hook_server('PRIVMSG', anti_mayusculas_cb, userdata=None)
# Resaltados
hookresaltados = xchat.hook_server('PRIVMSG', resaltados_cb, userdata=None)
# Antispam
hook21 = xchat.hook_server('PRIVMSG', antispam_cb, userdata=None)
hook22 = xchat.hook_command('antiadd', antispam_add_cb)
hook23 = xchat.hook_command('antilist', antispam_list_cb)
hook24 = xchat.hook_command('antidel', antispam_del_cb)
# Whois
raw301 = xchat.hook_server('301', whois_cb, userdata=None, priority=10) # Mensaje de AWA
raw307 = xchat.hook_server('307', whois_cb, userdata=None, priority=10) # whoisregnick
raw310 = xchat.hook_server('310', whois_cb, userdata=None, priority=10) # whoishelpop
raw311 = xchat.hook_server('311', whois_cb, userdata=None, priority=10) #whoisuser
raw312 = xchat.hook_server('312', whois_cb, userdata=None, priority=10) #whoisserver
raw313 = xchat.hook_server('313', whois_cb, userdata=None, priority=10) #whoisoperator
raw316 = xchat.hook_server('316', whois_cb, userdata=None, priority=10) #whoischanop
raw317 = xchat.hook_server('317', whois_cb, userdata=None, priority=10) #whoisidle
raw318 = xchat.hook_server('318', whois_cb, userdata=None, priority=10) #endofwhois
raw319 = xchat.hook_server('319', whois_cb, userdata=None, priority=10) #whoischannels
raw320 = xchat.hook_server('320', whois_cb, userdata=None, priority=10) #whoisspecial
raw335 = xchat.hook_server('335', whois_cb, userdata=None, priority=10) #whoisbot
raw342 = xchat.hook_server('342', whois_cb, userdata=None, priority=10) # Solo admite privados de usuarios registrados
raw378 = xchat.hook_server('378', whois_cb, userdata=None, priority=10) #whoishost (ip virtual)
raw379 = xchat.hook_server('379', whois_cb, userdata=None, priority=10) #whoismodes
raw401 = xchat.hook_server('401', whois_cb, userdata=None, priority=10) # No such nick
# Media
hookescuchando = xchat.hook_command('escuchando', media_cb, userdata="escuchando")
hookreproductor = xchat.hook_command('reproductor', media_cb, userdata="reproductor")
hooksiguiente = xchat.hook_command('siguiente', media_cb, userdata="siguiente")
hookanterior = xchat.hook_command('anterior', media_cb, userdata="anterior")
hookplay = xchat.hook_command('play', media_cb, userdata="play")
hookpausa = xchat.hook_command('pausa', media_cb, userdata="pausa")
hookstop = xchat.hook_command('stop', media_cb, userdata="stop")
# Peer to Peer
hookamule = xchat.hook_command('amule', amule_cb)
hookazureus = xchat.hook_command('azureus', azureus_cb)
# Consejos
hook31 = xchat.hook_command('consejos', consejo_aleatorio_cb)
hook32 = xchat.hook_command('consejo', consejo_cb)
hook33 = xchat.hook_command('preguntar', preguntar_cb)
hook34 = xchat.hook_command('ayudar', ayudar_cb)
hook35 = xchat.hook_command('noayudar', noayudar_cb)
hook36 = xchat.hook_command('planteamiento', planteamiento_cb)
hook37 = xchat.hook_command('privado', privado_cb)
hook38 = xchat.hook_command('web', web_cb)
hook39 = xchat.hook_command('repos', repos_cb)
hook30 = xchat.hook_command('autent', autent_cb)
# RSS
hookrss = xchat.hook_command('rss', rss_cb)
hooklistarss = xchat.hook_command('listarss', rsslista_cb)
hookrssadd = xchat.hook_command('rssadd', rssadd_cb)
hookrssdel = xchat.hook_command('rssdel', rssdel_cb)
# Informacion del sistema
hook51 = xchat.hook_command('gup', uptime_cb)
hook52 = xchat.hook_command('gos', sistema_cb)
hook53 = xchat.hook_command('gsoft', software_cb)
hookfecha = xchat.hook_command('fecha', fecha_cb)
hookpc = xchat.hook_command('gpc', pc_cb)
hooknet = xchat.hook_command('gnet', red_cb)
# Kick/Ban temporal
hook71 = xchat.hook_command('kb_temp', kbtemporal_cb, help="Uso: KB_TEMP <nick> <mensaje_opcional> Establece un baneo temporal de 5 minutos sobre el nick indicado y lo expulsa. Si se introduce un mensaje se usa como razon de la expulsion. (Necesita ser operador del canal)")
# Opciones del script
hookopciones = xchat.hook_command('opciones', opciones_cb)
# Descarga del script
hook81 = xchat.hook_unload(unload_cb)
xchat.command("load -e " + gatodir + "menu.conf")


# Si se ha llegado a este punto el script esta cargado completamente, asi que
# mostramos el mensaje de carga
mensaje = "Cargado GatoScript " + __module_version__
gprint(mensaje)
# Y si hemos desactivado las funciones de XMMS avisamos de que no se usaran
if NoXmms == 1:
    gprint("Las funciones de control sobre XMMS no estaran disponibles por no encontrarse python-xmms")


#############################################################################
#
# Codigos especiales en las cadenas:
#
#   X-Chat      Python      Resultado
#   "%C"    =   "\003"  =   Color
#   "%B"    =   "\002"  =   Negrilla
#   "%U"    =   "\037"  =   Subrallado
#   "%R"    =   "\026"  =   Color invertido
#   "%O"    =   "\017"  =   Desactiva los demas
#   "$t"    =   "\t"    =   $t
#
#############################################################################
