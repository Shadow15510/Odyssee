# --------------------------------------------------
# Odyssée (Version 3.0)
# by Sha-chan~
# last version released on the December 24 2020
#
# code provided with licence :
# GNU General Public Licence v3.0
# --------------------------------------------------

from piscord import Handler, Embed
import json

from files.command import *

with open("Odyssée/config.json", "r") as file:
    config = json.load(file)

odyssee = Handler(config["TOKEN"], config["PREFIX"])
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

    cmnd = Command(player_file, kick_file, server_id, config["PREFIX"], config["SEP"])


def help_display(message, command_help):
    def auto_detect(command_help, query):
        for i in command_help.items():
            if query in i[1][0]: return i[0]

    def formating_args(command):
        if len(command):
            return f" {config['SEP']} ".join(command)
        else:
            return ""

    answer = Embed()
    answer.title = "Rubrique d'aide"
    answer.color = 8421504

    args = message.content.lower().split()
    
    if len(args) != 2:
        answer.description = "Liste des commandes disponibles"
        for i in command_help:
            answer.add_field(name=i, value=f"`{config['PREFIX']}{command_help[i][0][0]} {formating_args(command_help[i][0][1:])}`", inline=False)
    else:
        key = auto_detect(command_help, args[1])
        if not key:
            message.channel.send(f"*Erreur : la commande '{args[1]}' n'existe pas.*")
            return None
        else:
            answer.description = f"Aide détaillée : {key.lower()}"
            answer.add_field(name="Syntaxe", value=f"`{config['PREFIX']}{command_help[key][0][0]} {formating_args(command_help[key][0][1:])}`", inline=True)
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

def check_admin(command):
    def wrapper(message):
        if message.author.id in config["ADMIN"]:
            return command(message)
        return message.channel.send("*Erreur : commande non-autorisée.*")
    
    wrapper.__name__ = command.__name__
    return wrapper

@odyssee.event
def on_ready(message):
    odyssee.set_presence(f"{config['PREFIX']}aide", 3)
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
            answer.add_field(name=i[0], value=f"{i[1]} de niveau {i[3]}, vers {i[2]}{('', ' (PnJ)')[i[4] <= 0]}", inline=False)

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

@odyssee.command
@check_server_id
def vitesse(message):
    per_hour, per_day, _, sea, success = cmnd.speed_travel(message)
    if success:
        answer = Embed()
        answer.title = "Vitesse"
        answer.color = 8421504

        if sea:
            answer.description = "Détail des vitesses, en kilomètres"

            answer.add_field(name="Sur la mer", value=f"`Par heure .: {per_hour[0]}`\n`Par jour ..: {per_day[0]}`", inline=False)
        else:
            answer.description = "Détail des vitesses par type de route, en kilomètres"

            answer.add_field(name="Sur une route", value=f"`Par heure .: {per_hour[0]}`\n`Par jour ..: {per_day[0]}`", inline=False)
            answer.add_field(name="Sur un chemin", value=f"`Par heure .: {per_hour[1]}`\n`Par jour ..: {per_day[1]}`", inline=False)
            answer.add_field(name="Hors chemin", value=f"`Par heure .: {per_hour[2]}`\n`Par jour ..: {per_day[2]}`", inline=False)
        message.channel.send(embed=answer.to_json())
    else:
        message.channel.send(per_hour)


@odyssee.command
@check_server_id
def temps(message):
    time_hour, time_day, distance, sea, success = cmnd.time_travel(message)
    if success:
        answer = Embed()
        answer.title = "Temps"
        answer.color = 8421504
        answer.description = f"Temps nécessaire pour parcourir {distance} kilomètre{('', 's')[distance > 1]}"

        if sea:
            answer.add_field(name="Sur la mer", value=f"`jour(s) ..: {time_day[0]}`\n`heure(s) .: {time_hour[0]}`", inline=False)
        else:
            answer.add_field(name="Sur une route", value=f"`jour(s) ..: {time_day[0]}`\n`heure(s) .: {time_hour[0]}`", inline=False)
            answer.add_field(name="Sur un chemin", value=f"`jour(s) ..: {time_day[1]}`\n`heure(s) .: {time_hour[1]}`", inline=False)
            answer.add_field(name="Hors chemin", value=f"`jour(s) ..: {time_day[2]}`\n`heure(s) .: {time_hour[2]}`", inline=False)
        message.channel.send(embed=answer.to_json())
    
    else:
        message.channel.send(time_hour)


# --- Administration --- #

@odyssee.command
def sauvegarde(message):
    cmnd.save()
    message.channel.send(f"Partie sauvegardée.\n\n**Fichier local**\n{save_read()}")


@odyssee.command
@check_admin
def charger(message):
    message.channel.send(cmnd.load(message))
    init_game()


@odyssee.command
@check_admin
def modifier(message):
    message.channel.send(cmnd.player_modify(message))
    cmnd.save()


@odyssee.command
@check_admin
def ajout_joueur(message):
    message.channel.send(cmnd.player_create(message))
    cmnd.save()

@odyssee.command
@check_admin
def kick(message):
    message.channel.send(cmnd.player_kick(message))
    cmnd.save()


@odyssee.command
@check_admin
def unkick(message):
    message.channel.send(cmnd.player_unkick(message))
    cmnd.save()


@odyssee.command
@check_admin
def formatage_kick(message):
    message.channel.send(cmnd.clear_kick(message))
    cmnd.save()


@odyssee.command
@check_admin
def formatage_joueur(message):
    message.channel.send(cmnd.clear_player(message))
    cmnd.save()


@odyssee.command
@check_admin
def formatage(message):
    message.channel.send(cmnd.clear_all(message))
    init_game()


@odyssee.command
@check_admin
def administration(message):
    command_help = {
        "Sauvegarder la partie et obtenir une copie locale": (["sauvegarde"], ""),
        "Charger une partie externe": (["charger"], ""),
        "Modifier les statistiques d'un joueur": (["modifier", "< nom_joueur >", "< nom_capacité >", "< valeur >"], "__Capacité disponibles :__ Courage, Force, Habileté, Rapidité, Défense, Vie, Mana, Argent, Lieu, objet+, objet-, nom, espèce, toutes"),
        "Créer un nouveau joueur": (["ajout_joueur", "< nom >", "< espèce >"], ""),
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
        "Connaitre ses statistiques ou celles d'un joueur": (["stat", "[< nom_du_joueur >]"], f"Pour voir vos propre stat entrez uniquement `{config['PREFIX']}stat`."),
        "Changer sa couleur": (["couleur", "< nom_de_la_couleur >"], f"Vous pouvez également entrer le code hexadécimal en utilisant `{config['PREFIX']}couleur 0xRRVVBB`."),
        "Connaître les espèces enregistrées et changer son espèce": (["espèce", "[< nouvelle_espèce >]"], f"Pour voir la liste entrez seulement `{config['PREFIX']}espèce`."),
        "Avoir la liste des joueurs": (["liste"], ""),
        "Démarrer ou poursuivre un combat": (["combat", "< nom_de_l'adversaire >"], "Lors d'un combat, vous devez impérativement être sur le même lieu que votre adversaire."),
        "Connaitre les articles disponible, consulter les statistiques d'un article": (["article", "[< nom_de_l'article >]"], "Ne pas spécifier de nom d'article renvoie la liste de tous les articles disponibles. Vous ne pouvez consulter les articles que si vous êtes dans un magasin."),
        "Avoir la description de ses pouvoirs et les utiliser": (["pouvoir", "[< nom_du_pouvoir > [", "< nom_de_l'ennemi >]]"], f"Pour avoir la liste de vos pouvoirs entrez seulement `{config['PREFIX']}pouvoir`. Si vous voulez utiliser un de vos pouvoirs il faut spécifier le nom du pouvoir.\nCertains pouvoir nécessite d'avoir un adversaire : pensez à préciser son nom."),
        "Effectuer un lancer de dé": (["dé", "[< nombre_de_faces > [", "< nombre_de_dés >]]"], "Par défaut, un dé à 20 faces est lancé."),
        "Effectuer un lancer dans une capacité": (["capacité", "< nom_de_la_capacité >"], ""),
        "Changer de lieu": (["lieu", "< nom_du_nouveau_lieu >"], "Pensez à bien préciser l'article. (i.e. : '__la__ plage' et non pas 'plage')"),
        "Acheter un objet": (["achat", "< nom_de_l'objet > [", "< nombre > ]"], "Vous ne pouvez acheter plusieurs articles que si l'article désiré est à consommer."),
        "Ramasser un objet": (["prend", "< nom_de_l'objet >"], ""),
        "Donner un objet à un joueur": (["donne", "< nom_du_joueur >", "< nom_de_l'objet > [", "< montant >]"], f"Vous devez être dans le même lieu.\nVous pouvez donner de l'argent à un autre joueur, le nom de l'objet devient 'Argent' et vous devez préciser un troisième paramètre `montant`. La syntaxe devient donc : `{config['PREFIX']}donne < nom_du_joueur > {config['SEP']} Argent {config['SEP']} < montant >`."),
        "Jetter un objet": (["jette", "< nom_de_l'objet >"], ""),
        "utiliser un objet": (["utilise", "< nom_de_l'objet > [", "< nombre >]"], "Permet de manger de la nourriture achetée ou d'utiliser du poison. Préciser un nombre consommera autant d'unité que précisée de l'objet visé."),
        "Sauvegarder, ou supprimer, une note": (["note", "< contenu_ou_numero >", "< + | - >"], f"Pour ajouter une note utilisez la syntaxe : `{config['PREFIX']}note < contenu > {config['SEP']} +`. Pour supprimer une note entrez : `{config['PREFIX']}note < numéro > {config['SEP']} -`.\nVos notes sont visibles sur vos statistiques."),
        "Avoir sa vitesse de déplacement": (["vitesse", "< moyen_de_transport >", "< météo > [", "< type_de_terrain >]"], "Si vous êtes sur l'eau, ne précisez pas le type de terrain.\n\n__Moyen de transport reconnus :__ " + ", ".join(list(data_travel_mean().keys())) + "\n\n__Conditions météorologique connues :__ " + ", ".join(list(data_travel_weather().keys())) + "\n\n__Terrains connus :__ " + ", ".join(list(data_travel_land().keys()))),
        "Connaître le temps nécessaire pour franchir une distance": (["temps", "< distance >", "< moyen_de_transport >", "< météo > [", "< type_de_terrain >]"], "Si vous êtes sur l'eau, ne précisez pas le type de terrain.\n\n__Moyen de transport reconnus :__ " + ", ".join(list(data_travel_mean().keys())) + "\n\n__Conditions météorologique connues :__ " + ", ".join(list(data_travel_weather().keys())) + "\n\n__Terrains connus :__ " + ", ".join(list(data_travel_land().keys())))
    }

    help_display(message, command_help)


odyssee.start()

