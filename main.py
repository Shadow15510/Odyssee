# --------------------------------------------------
# Odyssée (Version 1.1)
# by Sha-chan~
# last version released on the 28 of September 2020
#
# code provided with licence :
# GNU General Public Licence v3.0
# --------------------------------------------------

from piscord import Handler, Embed
from command import *

odyssee = Handler(os.environ["token"], "+")

def init_game():
  print("Initialisation...")
  try:
    save_file = eval(save_read())
  
    player_file, kick_file = save_file[0], save_file[1]
  
    player_file = [save_to_object(player) for player in player_file]
    player_file = {player.id : player for player in player_file}
  
    cmnd = Command(player_file, kick_file)
    print("> save successfully loaded")

  except:
    save_delete()
    save_send("[[],[]]")
    cmnd = Command({}, [])
    print("> save file didn't found\n> new game start")

@odyssee.event
def on_ready(message):
  odyssee.set_presence("+aide", 3)
  init_game()
  
  
# --------------------------------------------------
# Commands
# --------------------------------------------------

# --- Settings --- #

@odyssee.command
def couleur(message):
  message.channel.send(cmnd.color_change(message))
  cmnd.save()

@odyssee.command
def espèce(message):
  message.channel.send(cmnd.species_change(message))
  cmnd.save()

@odyssee.command
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
def new(message):
  message.channel.send(cmnd.player_new(message))
  cmnd.save()

# --- Game --- #

@odyssee.command
def combat(message):
  message.channel.send(cmnd.fight(message))
  cmnd.save() 

@odyssee.command
def article(message):
  info, color = cmnd.show_articles(message)
  if color + 1:
    answer = Embed()
    answer.title = info[0]
    answer.description = "Listes des articles disponibles"
    answer.color = color
    for item_name in info[1]:
      item_stat = info[1][item_name]
      
      stat = ""
      for stat_name in item_stat:
        if item_stat[stat_name]: stat += f"{stat_name} : {item_stat[stat_name]}, "
       
      answer.add_field(name=item_name, value=stat[:-2], inline=False)
      
    message.channel.send(embed = answer.to_json())
    return None

  message.channel.send(info)

@odyssee.command
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
    answer.add_field(name="Inventaire", value=" - " + "\n - ".join(info[13]), inline=False)
  else:
    answer.add_field(name="Inventaire", value="< vide >", inline=False)
    
  message.channel.send(embed = answer.to_json())

@odyssee.command
def pouvoir(message):
  message.channel.send(cmnd.specialpower(message))

@odyssee.command
def dé(message):
  message.channel.send(cmnd.roll_dice(message))

@odyssee.command
def capacité(message):
  message.channel.send(cmnd.roll_capacity(message))

@odyssee.command
def lieu(message):
  message.channel.send(cmnd.place_change(message))
  cmnd.save()

@odyssee.command
def achat(message):
  message.channel.send(cmnd.buy(message))
  cmnd.save()

@odyssee.command
def prend(message):
  message.channel.send(cmnd.object_take(message))
  cmnd.save()

@odyssee.command
def donne(message):
  message.channel.send(cmnd.object_give(message))
  cmnd.save()

@odyssee.command
def jette(message):
  message.channel.send(cmnd.object_throw(message))
  cmnd.save()
  
# --- Administration --- #

@odyssee.command
def sauvegarde(message):
  cmnd.save()
  message.channel.send(f"Partie sauvegardée.\n\n**Fichier local**\n{save_read()}")

@odyssee.command
def charger(message):
  message.channel.send(cmnd.load(message.content[8:]))
  cmnd.save()

@odyssee.command
def modifier(message):
  message.channel.send(cmnd.player_modify(message))
  init_game()
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
  cmnd.save()

@odyssee.command  
def aide(message):
  answer = Embed()
  answer.title = "Rubrique d'aide"
  answer.description = "Liste des commandes disponibles"
  answer.color = 8421504

  answer.add_field(name="Créer un nouveau joueur", value="`+new < nom_de_l'espèce >`", inline=False)
  answer.add_field(name="Connaitre ses statistiques ou celles d'un joueur", value="`+stat [< nom_du_joueur >]`", inline=False)
  answer.add_field(name="Changer sa couleur", value="`+couleur < nom_de_la_couleur >` (ou code héxadécimal)", inline=False)
  answer.add_field(name="Connaître les espèces enregistrées", value="`+espèce`", inline=False)
  answer.add_field(name="Changer son espèce", value="`+espèce < nouvelle_espèce >`", inline=False)
  answer.add_field(name="Avoir la liste des joueurs", value="`+liste`", inline=False)
  answer.add_field(name="Démarrer ou poursuivre un combat", value="`+combat < nom_de_l'adversaire >`", inline=False)
  answer.add_field(name="Connaitre les articles disponible, consulter les statistiques d'un article", value="`+article [< nom_de_l'article >]`", inline=False)
  answer.add_field(name="Avoir la description de ses pouvoir et les utiliser", value="`+pouvoir [< nom_du_pouvoir >] [, < nom_de_l'ennemi >]`", inline=False)
  answer.add_field(name="Effectuer un lancer de dé", value="`+dé [< nombre_de_faces >] [, < nombre_de_dés >]`", inline=False)
  answer.add_field(name="Effectuer un lancer dans une capacité", value="`+capacité < nom_de_la_capacité >`", inline=False)
  answer.add_field(name="Changer de lieu", value="`+lieu < nom_du_nouveau_lieu >`", inline=False)
  answer.add_field(name="Acheter un objet", value="`+achat < nom_de_l'objet >`", inline=False)
  answer.add_field(name="Ramasser un objet", value="`+prend < nom_de_l'objet >`", inline=False)
  answer.add_field(name="Donner un objet à un joueur", value="`+donne < nom_du_joueur >, < nom_de_l'objet >`", inline=False)
  answer.add_field(name="Donner de l'argent à un joueur", value="`+donne < nom_du_joueur >, Argent, < montant >`", inline=False)
  answer.add_field(name="Jetter un objet", value="`+jette < nom_de_l'objet >`", inline=False)

  if int(message.author.id) in data_admin():
    answer.add_field(name="Forcer la sauvegarde et obtenir une copie locale", value="`+sauvegarde`", inline=False)
    answer.add_field(name="Charger une sauvegarde", value="`+charger < sauvegarde >`", inline=False)
    answer.add_field(name="Modifier un joueur", value="`+modifier < nom_du_joueur >, < caractéristique à changer >, < nouvelle_valeur >`", inline=False)
    answer.add_field(name="Kicker un joueur", value="`+kick < nom_du_joueur >`", inline=False)
    answer.add_field(name="Unkick un joueur", value="`+unkick < id_du_joueur >`", inline=False)
    answer.add_field(name="Unkick tout les joueurs kické", value="`+formatage_kick`", inline=False)
    answer.add_field(name="Supprimer tous les joueurs", value="`+formatage_joueur`", inline=False)
    answer.add_field(name="Formater la sauvegarde", value="`+formatage`", inline=False)
  message.channel.send(embed = answer.to_json())

odyssee.run()

