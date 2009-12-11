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
    ANTISPAM = 1
    SPAMBOTS = int(auxiliar.lee_conf("protecciones", "spambots"))
    filtros = auxiliar.gatodb_cursor_execute("SELECT filtro FROM filtros")
    compilados = []
    for filtro in filtros:
        compilados.append(re.compile(".*" + filtro[0] + ".*", re.IGNORECASE))
else:
    auxiliar.gprint("AntiSpam esta desactivado o no se puede cargar la lista de filtros")
    ANTISPAM = 0
    SPAMBOTS = 0

#prueba = re.compile("FREE FREE!! Don't Register , Don't Money Only Click Here =>|Full teen girls|Girlss\.tr\.cx|Hard & teens|http://adult\.edu\.tc|Http://AduLts\.eu\.tp|Http://Beklenen\.Net|Http://downloads\.fr\.mn|Http://Movies\.jp\.tp|http://nehirim\.net/freemoney\.htm|http://tamer\.us\.pn|http://www\.dartanyan\.net/girls\.exe|http://www\.seker\.net\.ms|Http://www\.sexymovies\.tr\.cx|naked from msn|p0rn|pornstar|realcoder\.net|sexgirl\.tc\.gs|sexigirls\.it|Simge\.tk|SizinAlem\.Net|sonia21\.firez\.org|www\.belesvideo\.ne|\www\.guapa\.now\.nu|WWW\.LOVEORHONEY\.COM|WWW\.LOVEORLOVE\.COM|You Win To For Money|bahanem\.org|grupsgirl\.net|porno\.exe|bestupload|analtime\.us\.pn|www\.moviesus\.net|hot-teens\.such\.info|/teengirl\.|Http://AduLt\.tc\.vg|pikolata|NAZ\.tr\.cx|free girls|KralHack\.cjb\.net|Free porno|Http://hanibana\.net|http://Moviesus\.net|http://lolita\.dd\.am|Moviesus\.net|bulusturma|Sunucumuz sohbete|olita\.dd\.am|kizadresleri\.bulunur\.com|v1rg1n|g1rl|http://sexhouse\.dd\.am|Bedava filim|Http://pikoLata\.net|video\.exe|Annelerinizi|www\.LIGUEYA\.COM|gelmeyenin|KnightonLine\.exe|AduLt\.es\.tp|http://arzuLu|http://mitglied\.lycos\.de|PikoLata|lolita\.exe|kirazLi|Sende indir izle|En cok oLduqu|F-ree P-orno V-ideo|Double ClicK|manymany|virgin girl|superkizmsnleri|hersey Burda|supernacho|www\.suskun\.net|free-movie-mpeg\.exe|http://www\.camlisex\.com|karagece|rap-fm|free adult|qelsin Bari|xicasendirecto|www\.mamellas\.com|maria1cam|\?santos|Miraquegolfas|gracia_lagolosa|erotikam|www\.doreag\.es|asdgo\.com|consupermiso\.com|www\.slordjp\.tk|www\.tuylostuyos\.com|traviesas_mv88|yamile_mb87|koonymara|jesica_sexy_amor|www\.geocities\.com/octubre122005|www\.dominiosteca\.biz|es-facil.com/ganar|WWW\.ELECTRIKSOUND\.COM|www\.fororelax\.net|www\.shateros\.com|www\.chaterosforever\.com|neverendingnovel\.wordpress\.com|criticonomicon\.wordpress\.com|crazyvideos\.zapto\.org|youtube\.com/mryorx|myminicity\.es|nokia n73|lasegundapuerta\.com|www\.myspace\.com/joaquinbello|www\.ircap\.es|\@hotmail\.com|www\.proteinasyfitness\.com|WWW\.SERIALCRACK\.ES|suellencastillo|UnVoto\.asp|mileurazos\.es\.tl|web/mviiiax|anhely_cielo|yorxpatri|www\.antitaurino\.org|midmind|usadastangas|carolina-cerezuela|lordserer|WWW\.CHEO\.HAZBLOG\.COM|moccia|jordiponsi|tuatubolayyoalamia\.blogspot\.com|AGREGAME AMI KORREO|calientita_sexyxcam|quelocochat\.com|morenita_cam_luciax|#m7x0|www\.13mensistas\.com|WWW\.MISECRETITO\.COM\.AR|loscirculosviciosos\.blogspot\.com|esohavuelto\.blogspot\.com|www\.darkzone\.ar\.kz|esohavuelto|usuarios\.lycos\.es/girasfotos|numberone\.foroactivo\.net|slordjp|nutricionysalud3000|messagemagic|hombres-maltratados|acceso-virtual|WWW\.NEWSTD\.COM\.AR|CONTACTOS REALES|diabulusradio|agregame.*hotmail\.com|paiporta\.creatuforo\.com|tiasjuguetonas\.com|chatrd\.net|xag-mamporros|diariodeoriente|rincondeleuro|LA LL!!|primigratis|gandisex|contactoreal\.tk|trinityatierra\.wordpress\.com|canaltravestis|samburinya\.blogspot\.com|www\.tuloarreglas\.com|http.elbruto\.es|verme por webcam, sin tener que mandar .* sms .*|www\.elotrolado\.net/foro_xbox-360_137|www\.masmediamail\.com/durarealidad/|www\.readysoft\.es|zebal|ganadinerocon|contactos\.esmiweb\.com|kedar\.es|chatdeligar\.com|www\.chatconvideo\.com|caramelito\.xbox-site\.info", re.IGNORECASE)

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
    if auxiliar.CONECTADO == 1:
        ANTISPAM = 1
        SPAMBOTS = int(auxiliar.lee_conf("protecciones", "spambots"))
        # Cargamos la nueva lista de filtros y compilamos las regexps
        filtros = auxiliar.gatodb_cursor_execute("SELECT filtro FROM filtros")
        compilados = []
        for filtro in filtros:
            compilados.append(re.compile(".*" + filtro[0] + ".*", \
                                         re.IGNORECASE))
    else:
        auxiliar.gprint("No se pueden cargar los filtros, AntiSpam desactivado")
        ANTISPAM = 0
        SPAMBOTS = 0


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
    if auxiliar.lee_conf("protecciones", "spam") == "1":
        for spam_exp in compilados:
            if (spam_exp.search(word_eol[3][1:])):
                ban = "1"
                mensaje = " Spam/Troll"
                auxiliar.expulsa(mensaje, ban, word)
    # Comprobamos si el mensaje se ha recibido en un privado o en alguno de
    # nuestros canales protegidos
    canales = auxiliar.gatodb_cursor_execute("SELECT canales FROM canales")
    if (word[2] in canales) or (word[2] == xchat.get_info("nick")):
        # Si esta activada la gestion de bots spammers...
        if SPAMBOTS == 1:
            # Si es asi, comprobamos si el mensaje contiene spam
            for spam_exp in compilados:
                if (spam_exp.search(word_eol[3][1:])):
                    # Si contiene spam, expulsamos al bot responsable
                    auxiliar.expulsa(" Bot spammer", "1", word)
                    # Y quitamos su nick de la lista de niños buenos
                    nick = word[0].split("!")[0].split(":")[1]
                    if nick in auxiliar.gatodb_cursor_execute("SELECT goodboy FROM goodboys"):
                        auxiliar.gatodb_cursor_execute("DELETE FROM goodboys WHERE goodboy \
                            IN (?)", (nick,))
                        auxiliar.gatodb_commit()
                    if word[2] in canales:
                        ban = "1"
                        mensaje = " Spam"
                        auxiliar.expulsa(mensaje, ban, word)
        # Comprobamos si esta activada la funcion anti spam
        if ANTISPAM == 1:
            # Si esta activada, comprobamos si el texto recibido contiene spam y
            # si es asi, ignoramos la linea    
            for spam_exp in compilados:
                if (spam_exp.search(word_eol[3][1:])):
                    return xchat.EAT_ALL


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
            sql = "INSERT INTO goodboys VALUES (null, %s)" % usuario.nick
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
xchat.command('menu ADD "GatoScript/AntiSpam/Añadir filtro" "getstr # \
              "antiadd" "Filtro:""')
xchat.command('menu ADD "GatoScript/AntiSpam/Eliminar filtro" "getstr # \
              "antidel" "Filtro:""')
