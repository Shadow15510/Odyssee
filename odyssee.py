# --------------------------------------------------
# Odyssée (Version 2.8)
# by Sha-chan~
# last version released on the 23 of December 2020
#
# code provided with licence :
# GNU General Public Licence v3.0
# --------------------------------------------------

from piscord import Handler, Embed
from files.command import *

# TOKEN = 
PREFIX = "+"
SEP = ";"

odyssee = Handler(TOKEN, PREFIX)
player_file, kick_file, server_id, cmnd = {}, [], 0, None


def init_game():
    global player_file
    global kick_file
    global cmnd
    global server_id
    
    print("Initialisation...")
    try:
        save_file = eval(save_read())
    
        player_file, kick_file, server_id = save_file[0], save_file[1], save_file[2]
    
        player_file = [save_to_object(player) for player in player_file]
        player_file = {player.id : player for player in player_file}
    
        print("> save successfully loaded")

    except:
        save_delete()
        save_send("[[],[],0]")
        print("> save file didn't found\n> new game start")

    cmnd = Command(player_file, kick_file, server_id, PREFIX, SEP)


def help_display(message, command_help):
    def auto_detect(command_help, query):
        for i in command_help.items():
            if query in i[1][0]: return i[0]

    def formating_args(command):
        if len(command):
            return f" {SEP} ".join(command)
        else:
            return ""

    answer = Embed()
    answer.title = "Rubrique d'aide"
    answer.color = 8421504

    args = message.content.lower().split()
    
    if len(args) != 2:
        answer.description = "Liste des commandes disponibles"
        for i in command_help:
            answer.add_field(name=i, value=f"`{PREFIX}{command_help[i][0][0]} {formating_args(command_help[i][0][1:])}`", inline=False)
    else:
        key = auto_detect(command_help, args[1])
        if not key:
            message.channel.send(f"*Erreur : la commande '{args[1]}' n'existe pas.*")
            return None
        else:
            answer.description = f"Aide détaillée : {key.lower()}"
            answer.add_field(name="Syntaxe", value=f"`{PREFIX}{command_help[key][0][0]} {formating_args(command_help[key][0][1:])}`", inline=True)
            answer.add_field(name="Détails d'utilisation", value=(command_help[key][1], "< aucun >")[not command_help[key][1]], inline=True)

    message.channel.send(embed = answer.to_json())


def check_server_id(command):
    def wrapper(message):
        if not cmnd.server_id:
            cmnd.set_server_id(message)
        elif cmnd.server_id != message.channel.guild.id:
            return message.channel.send("*Erreur : Odyssée est déjà utilisé sur un autre serveur.*")
        command(message)

    wrapper.__name__ = command.__name__
    return wrapper


@odyssee.event
def on_ready(message):
    odyssee.set_presence(f"{PREFIX}aide", 3)
    init_game()

# --------------------------------------------------
# Commands
# --------------------------------------------------

# --- Settings --- #

@odyssee.command
@check_server_id
def couleur(message):
    message.channel.send(cmnd.color_change(message))
    cmnd.save()


@odyssee.command
@check_server_id
def espèce(message):
    message.channel.send(cmnd.species_change(message))
    cmnd.save()


@odyssee.command
@check_server_id
def liste(message):
    info, color = cmnd.player_list(message)
    if color + 1:
        answer = Embed()
        answer.title = "Joueurs"
        answer.description = "Liste des joueurs enregistrés"
        answer.color = color
        for i in info:
            answer.add_field(name=i[0], value=f"{i[1]} de niveau {i[3]}, vers {i[2]}", inline=False)

        message.channel.send(embed = answer.to_json())
        return None
    
    message.channel.send(info)


@odyssee.command
@check_server_id
def nouveau(message):
    message.channel.send(cmnd.player_new(message))
    cmnd.save()


@odyssee.command
@check_server_id
def pseudo(message):
    message.channel.send(cmnd.change_pseudo(message))
    cmnd.save()


@odyssee.command
@check_server_id
def note(message):
    message.channel.send(cmnd.modify_note(message))
    cmnd.save()


# --- Game --- #

@odyssee.command
@check_server_id
def combat(message):
    message.channel.send(cmnd.fight(message))
    cmnd.save() 


@odyssee.command
@check_server_id
def article(message):
    info, color, message_type = cmnd.show_articles(message)

    if not message_type:
        answer = Embed()
        answer.title = info[0].capitalize()
        answer.description = "Listes des articles disponibles"
        answer.color = color

        for item_name in info[1]:
            item_stat = info[1][item_name][0]
            
            stat = ""
            for stat_name in item_stat:
                if item_stat[stat_name]: stat += f"{stat_name} : {item_stat[stat_name]}, "
             
            answer.add_field(name=item_name.capitalize(), value=stat[:-2], inline=False)
            
        message.channel.send(embed = answer.to_json())
        return None

    elif message_type == 1:
        answer = Embed()
        answer.title = info[0].capitalize()
        answer.description = "Détails de l'article"
        answer.color = color

        value = "\n".join([f"`{name}.: {info[1][0][index]}`" for index, name in enumerate(("Courage .", "Force ...", "Habileté ", "Rapidité ", "Défense .", "Vie .....", "Mana ...."))])
        answer.add_field(name="Caractéristiques", value=value, inline=True)
        answer.add_field(name="Divers", value=f"`Prix ..: {abs(info[1][0][7])} Drachmes`\n`Usage .: {('à stocker', 'à consommer', 'consommation immédiate')[info[1][1]]}`", inline=True)
        message.channel.send(embed = answer.to_json())
        return None

    message.channel.send(info)


@odyssee.command
@check_server_id
def stat(message):
    info = cmnd.player_information(message)
    
    if type(info) == str:
        message.channel.send(f"*Erreur : {info} n'existe pas.*")
        return None
    
    answer = Embed()
    answer.title = info[0]
    answer.description = f"Statistiques de {info[0]}, {info[1]}\n de niveau {info[2]}"
    answer.color = info[11]
    for index, capacity_name in enumerate(("Courage", "Force", "Habileté", "Rapidité", "Défense")):
        answer.add_field(name=capacity_name, value=info[3 + index], inline=True)

    
    answer.add_field(name="Mana", value=info[9], inline=True)
    answer.add_field(name="Vie", value=info[8], inline=True)
    answer.add_field(name="Argent", value=info[10], inline=True)
    
    answer.add_field(name="Lieu", value=info[12], inline=True)

    if len(info[13]):
        object_in_inventory = ""
        for item in info[13]:
            object_in_inventory += f" - {item[0]} {('', f' ({item[1]})')[item[1] != -1]}\n"
        answer.add_field(name="Inventaire", value=object_in_inventory, inline=True)
    else:
        answer.add_field(name="Inventaire", value="< vide >", inline=True)
    
    if info[14][0][0]:
        note = "\n".join([f"{i[0]} - {i[1]}" for i in info[14]])
    else:
        note = "< aucune >"

    answer.add_field(name="Notes", value=note, inline=True)
    message.channel.send(embed = answer.to_json())


@odyssee.command
@check_server_id
def pouvoir(message):
    message.channel.send(cmnd.specialpower(message))


@odyssee.command
@check_server_id
def dé(message):
    message.channel.send(cmnd.roll_dice(message))


@odyssee.command
@check_server_id
def capacité(message):
    message.channel.send(cmnd.roll_capacity(message))


@odyssee.command
@check_server_id
def lieu(message):
    message.channel.send(cmnd.place_change(message))
    cmnd.save()


@odyssee.command
@check_server_id
def achat(message):
    message.channel.send(cmnd.buy(message))
    cmnd.save()

@odyssee.command
@check_server_id
def prend(message):
    message.channel.send(cmnd.object_take(message))
    cmnd.save()


@odyssee.command
@check_server_id
def donne(message):
    message.channel.send(cmnd.object_give(message))
    cmnd.save()


@odyssee.command
@check_server_id
def jette(message):
    message.channel.send(cmnd.object_throw(message, False))
    cmnd.save()
  

@odyssee.command
@check_server_id
def utilise(message):
    message.channel.send(cmnd.object_throw(message, True))
    cmnd.save()


# --- Administration --- #

@odyssee.command
def sauvegarde(message):
    cmnd.save()
    message.channel.send(f"Partie sauvegardée.\n\n**Fichier local**\n{save_read()}")


@odyssee.command
def charger(message):
    message.channel.send(cmnd.load(message))
    init_game()


@odyssee.command
def modifier(message):
    message.channel.send(cmnd.player_modify(message))
    cmnd.save()


@odyssee.command
def kick(message):
    message.channel.send(cmnd.player_kick(message))
    cmnd.save()


@odyssee.command
def unkick(message):
    message.channel.send(cmnd.player_unkick(message))
    cmnd.save()


@odyssee.command
def formatage_kick(message):
    message.channel.send(cmnd.clear_kick(message))
    cmnd.save()


@odyssee.command
def formatage_joueur(message):
    message.channel.send(cmnd.clear_player(message))
    cmnd.save()


@odyssee.command
def formatage(message):
    message.channel.send(cmnd.clear_all(message))
    init_game()


@odyssee.command
def administration(message):
    command_help = {
        "Sauvegarder la partie et obtenir une copie locale": (["sauvegarde"], ""),
        "Charger une partie externe": (["charger"], ""),
        "Modifier les statistiques d'un joueur": (["modifier", "< nom_joueur >", "< nom_capacité >", "< valeur >"], "Capacité disponibles :\nCourage, Force, Habileté, Rapidité, Défense, Vie, Mana, Argent, Lieu, objet+, objet-, nom, toutes"),
        "Kicker un joueur": (["kick", "< pseudo_joueur >"], ""),
        "Autoriser un joueur kické à refaire un joueur": (["unkick", "< id_joueur >"], ""),
        "Remettre à zéro les kicks": (["formatage_kick"], ""),
        "Remettre à zéro les joueurs": (["formatage_joueur"], ""),
        "Tout remettre à zéro": (["formatage"], ""),
    }

    help_display(message, command_help)


@odyssee.command
def aide(message):
    command_help = {
        "Créer un nouveau joueur": (["nouveau", "< nom_de_l'espèce >"], ""),
        "Changer son pseudo": (["pseudo", "< nouveau_pseudo >"], ""),
        "Connaitre ses statistiques ou celles d'un joueur": (["stat", "[< nom_du_joueur >]"], f"Pour voir vos propre stat entrez uniquement `{PREFIX}stat`."),
        "Changer sa couleur": (["couleur", "< nom_de_la_couleur >"], f"Vous pouvez également entrer le code hexadécimal en utilisant `{PREFIX}couleur 0xRRVVBB`."),
        "Connaître les espèces enregistrées et changer son espèce": (["espèce", "[< nouvelle_espèce >]"], f"Pour voir la liste entrez seulement `{PREFIX}espèce`."),
        "Avoir la liste des joueurs": (["liste"], ""),
        "Démarrer ou poursuivre un combat": (["combat", "< nom_de_l'adversaire >"], "Lors d'un combat, vous devez impérativement être sur le même lieu que votre adversaire."),
        "Connaitre les articles disponible, consulter les statistiques d'un article": (["article", "[< nom_de_l'article >]"], "Ne pas spécifier de nom d'article renvoie la liste de tous les articles disponibles. Vous ne pouvez consulter les articles que si vous êtes dans un magasin."),
        "Avoir la description de ses pouvoirs et les utiliser": (["pouvoir", "[< nom_du_pouvoir > [", "< nom_de_l'ennemi >]]"], f"Pour avoir la liste de vos pouvoirs entrez seulement `{PREFIX}pouvoir`. Si vous voulez utiliser un de vos pouvoirs il faut spécifier le nom du pouvoir.\nCertains pouvoir nécessite d'avoir un adversaire : pensez à préciser son nom."),
        "Effectuer un lancer de dé": (["dé", "[< nombre_de_faces > [", "< nombre_de_dés >]]"], "Par défaut, un dé à 20 faces est lancé."),
        "Effectuer un lancer dans une capacité": (["capacité", "< nom_de_la_capacité >"], ""),
        "Changer de lieu": (["lieu", "< nom_du_nouveau_lieu >"], "Pensez à bien préciser l'article. (i.e. : '__la__ plage' et non pas 'plage')"),
        "Acheter un objet": (["achat", "< nom_de_l'objet >"], ""),
        "Ramasser un objet": (["prend", "< nom_de_l'objet >"], ""),
        "Donner un objet à un joueur": (["donne", "< nom_du_joueur >", "< nom_de_l'objet > [", "< montant >]"], f"Vous devez être dans le même lieu.\nVous pouvez donner de l'argent à un autre joueur, le nom de l'objet devient 'Argent' et vous devez préciser un troisième paramètre `montant`. La syntaxe devient donc : `{PREFIX}donne < nom_du_joueur > {SEP} Argent {SEP} < montant >`."),
        "Jetter un objet": (["jette", "< nom_de_l'objet >"], ""),
        "utiliser un objet": (["utilise", "< nom_de_l'objet >"], "Permet de manger de la nourriture achetée ou d'utiliser du poison."),
        "Sauvegarder, ou supprimer, une note": (["note", "< contenu_ou_numero >", "< + | - >"], f"Pour ajouter une note utilisez la syntaxe : `{PREFIX}note < contenu > {SEP} +`. Pour supprimer une note entrez : `{PREFIX}note < numéro > {SEP} -`.\nVos notes sont visibles sur vos statistiques."),
    }

    help_display(message, command_help)


odyssee.start()

