# --------------------------------------------------
# Odyssée (Version 1.0)
# by Sha-Chan~
# last version released on the 30 of July 2020
#
# code provided with licence :
# GNU General Public Licence v3.0
# --------------------------------------------------

from player import *

# --------------------------------------------------
# Get informations from the message
# --------------------------------------------------

# --- Command and argument --- #

def analyse(message):
  def get_arg(arguments):
    args = [i.strip() for i in arguments.split(",")]
    return [i if i[0].isalpha() else int(i) for i in args]

  arguments = message.content.split(" ", 1)

  if len(arguments) == 1:
    return None
  return get_arg(arguments[1])

# --- Author's information --- #

def get_user(message):
  return message.author.nick, int(message.author.id)

class Command:
  def __init__(self, players, kick):
    self.players = players
    self.kick = kick

# --- Information about the targeted player --- #

  def nick_to_id(self, player_nick):
    for player_id in self.players:
      if self.players[player_id].name == player_nick: return player_id
    return False

  def id_to_nick(self, player_id):
    if player_id in self.players:
      return self.players[player_id].name
    return False

  def id_to_object(self, player_id):
    if player_id in self.players:
      return self.players[player_id]
    else:
      return False

# --------------------------------------------------
# Commands
# --------------------------------------------------

# --- Settings --- #

  def color_change(self, message):
    user = self.id_to_object(get_user(message)[1])
    if not user:
      return "*Erreur : {get_user(message)[0]} n'est pas un joueur enregistré.*"
    color_name = analyse(message)
    color_available = data_color()

    if color_name:
      color_name = color_name[0]
      if color_name.startswith("0x"): color_name = int(color_name, 16)
    else:
      return self.color_list()

    if type(color_name) == str and color_name in color_available.keys():
      color_id = color_available[color_name]
    elif type(color_name) == int:
      color_id = color_name
    else:
      return self.color_list()
  
    
    user.stat[8] = color_id
    
    return f"La couleur de {user.name} et devenue {color_name}"
  
  def color_list(self):
    return f"Entrez le code héxadécimal, ou le nom de la couleur souhaitée.\n**Liste des couleurs disponibles**\n - " + "\n - ".join(data_color())

  def species_change(self, message):
    user = self.id_to_object(get_user(message)[1])
    if not user:
      return self.species_list()
    
    new_species = analyse(message)
    
    if not new_species:
      return self.species_list()

    new_species = new_species[0].capitalize()
    
    user.species = new_species
    return f"{user.name} devient un(e) {new_species}"

  def species_list(self):
    species_category = data_species()
    msg = "Pour changer d'espèce, la syntaxe est : `+espèce < nom_de_la_nouvelle_espèce >`\n**Liste des espèces gérées**"
    for species in species_category:
      msg += "\n - " + ", ".join(species)
      
    return msg

  def player_list(self, message):
    if get_user(message)[1] not in self.players:
      return f"*Erreur : {get_user(message)[0]} n'existe pas.*", -1
    return [[self.players[player_id].name, self.players[player_id].species, self.players[player_id].place, self.players[player_id].get_level()] for player_id in self.players], self.players[get_user(message)[1]].stat[8]

  def player_new(self, message):
    user = get_user(message)
    species = analyse(message)

    if user[1] in self.kick:
      return f"*Erreur : {user[0]} a été kické.*"
    
    if species:
      species = species[0].capitalize()
    else:
      return "*Erreur : syntaxe invalide : `+new < nom_de_l'espèce >`.*"
    
    if not user[1] in self.players:
      self.players.update({user[1] : Player(user[1], user[0], species)})
      return f"{user[0]}, un(e) {species}, est apparu(e)."
    else:
      return f"*Erreur : {user[0]} est déjà enregistré(e).*"

# --- Game --- #

  def fight(self, message):
    user = self.id_to_object(get_user(message)[1])
    if not user:
      return f"*Erreur : {get_user(message)[0]} n'existe pas.*"

    elif not analyse(message):
      return "*Erreur : syntaxe invalide `+combat < nom_de_l'ennemi >`.*"
    
    return self.fight_new(message)
    
  def fight_new(self, message):
    user = self.id_to_object(get_user(message)[1])
    enemy_id = -len(self.players)
    enemy_name = analyse(message)[0].capitalize()
    
    if self.nick_to_id(enemy_name) < 0:
      return self.fight_continue(message)
    
    elif enemy_name in [player.name.capitalize() for player in self.players.values()]:
      return f"*Erreur : vous ne pouvez pas attaquer {enemy_name}.*"
    
    self.players.update({enemy_id : Player(enemy_id, enemy_name, "Ennemi", stat_gen(user.get_level(), user.stat[8], True), user.place)})

    return f"{user.name} se prépare pour combattre {enemy_name}.\nEntrez `+combat {enemy_name}` pour attaquer."

  def fight_continue(self, message):
    user = self.id_to_object(get_user(message)[1])
    enemy = self.id_to_object(self.nick_to_id(analyse(message)[0].capitalize()))

    if not enemy:
      return f"*Erreur : {analyse(message)[0]} n'existe pas.*"

    if user.place != enemy.place:
      return f"*Erreur : {user.name} et {enemy.name} ne sont pas au même endroit.*"

    def phase_1(player, target):
      pt_player, pt_target = 0, 0
      
      while pt_player == pt_target:
        pt_player = player.stat[0] + player.stat[3] + roll_die()
        pt_target = target.stat[0] + target.stat[3] + roll_die()
      return pt_player > pt_target

    def phase_2(player):
      return player.capacity_roll(2)

    def phase_3(player, target):
      pt_damage = player.stat[1] + roll_die(10, player.get_level())
      if target.stat[4] >= pt_damage:
        return 0
      elif target.stat[5] < pt_damage:
        return -1
      return pt_damage

    def comment_on_damage(player, target, pt_damage):
      if pt_damage == -1:
        target.stat[5] = 0
        return f"__{target.name}__ meurt sur le coup.\n"
      
      elif not pt_damage:
        return f"__{target.name}__ parvient à parer le coup.\n"
      
      else:
        target.stat[5] -= pt_damage
        return f"__{target.name}__ subit {pt_damage} dégâts.\n"

    def turn(player, target):
      result = f"__{player.name}__ s'avance pour attaquer…\n"
      if phase_2(player):
        result += f"Le coup porte !\n"
        result += comment_on_damage(player, target, phase_3(player, target))

        if target.isalive():
          result += f"__{target.name}__ se redresse.\n"
  
        else:
          result += f"__{player.name}__ fouille le cadavre et trouve {target.stat[7]} Drachmes."
          player.stat[7] += target.stat[7]
          self.players.pop(target.id)
          return result, True

      else:
        result = f"Mais __{target.name}__ esquive le coup…\n"

      return result, False
          
    if phase_1(user, enemy):
      fighters = (user, enemy)
    else:
      fighters = (enemy, user)
      
    result = f"__{fighters[0].name}__ engage le combat.\n"

    fight = turn(fighters[0], fighters[1])
    result += fight[0]
      
    if fight[1]: return result

    result +=f"__{fighters[1].name}__ se redresse pour riposter…\n"
      
    fight = turn(fighters[1], fighters[0])
    result += fight[0]

    if not fight[1]: result += f"\n**Points de vie restant**\n - __{user.name}__ : {user.stat[5]} Pv restant\n - __{enemy.name}__ : {enemy.stat[5]} Pv restant"
    return result
      
  def player_information(self, message):
    target = analyse(message)
    
    if target:
      target = self.id_to_object(self.nick_to_id(target[0]))
      if not target: return analyse(message)[0]
    else:
      target = self.id_to_object(get_user(message)[1])
      if not target: return get_user(message)[0]
      
    return target.get_stat()

  def specialpower(self, message):
    user = self.id_to_object(get_user(message)[1])

    if not user:
      return f"*Erreur : {get_user(message[0])} n'existe pas.*"

    args = analyse(message)

    if not args:
      return self.specialpower_list(user)

    args[0] = args[0].capitalize()
    power_available = user.get_specialPowers()

    if data_powerIndex(args[0]) not in power_available:
      return "*Erreur : {user.name} n'a pas le pouvoir : '{args[0]}'.*"
    
    if len(args) == 1:
      if data_powers()[data_powerIndex(args[0])][2]:
        return f"*Erreur : syntaxe invalide `+pouvoir {args[0]}, < nom_de_l'ennemi >`.*"
      return self.specialpower_use(args[0], user)

    args[1] = args[1].capitalize()
    
    target = self.id_to_object(self.nick_to_id(args[1]))
    
    if not target:
      return f"*Erreur : {args[1]} n'existe pas.*"

    if len(args) == 2:
      if not data_powers()[data_powerIndex(args[0])][2]:
        return f"*Erreur : syntaxe invalide `+pouvoir {args[0]}`.*"
      if target.place != user.place:
        return f"*Erreur : {user.name} et {target.name} ne sont pas au même endroit.*"
      return self.specialpower_use(args[0], user, target)
      
  def specialpower_list(self, user):
    power_available = user.get_specialPowers()
    if not power_available:
      return f"{user.name} n'a pas de pouvoir."
    
    all_power = data_powers()
    rslt = f"Pouvoirs disponibles pour {user.name}. Pour utiliser un pouvoir : `+pouvoir < nom_du_pouvoir > [, < nom_de_l'ennemi >]`"

    for power_index in power_available:
      rslt += f"\n - __{all_power[power_index][0]}__ : {all_power[power_index][1]}"
      if all_power[power_index][2]: rslt += " Nom de l'ennemi à spécifier."

    return rslt

  def specialpower_use(self, power_name, user, target = None):
    user.capacity_modify(6, -1)
    
    if not user.stat[6]:
      return f"{user.name} tente de lancer {power_name}… Mais rate le sort."

    msg = f"{user.name} lance {power_name}.\n"
  
    if power_name == "Nyctalopie":
      pts = 5 * user.get_level()
      user.stat[2] += pts
      user.stat[3] += pts
      msg += f"{user.name} gagne {pts} points d'Habileté et de Rapidité."

    elif power_name == "Vol":
      if user.capacity_roll(2):
        amount = target.stat[7]
        user.stat[7] += amount
        target.stat[7] = 0
        msg += f"{user.name} vole {amount} Drachmes à {target.name}."

    elif power_name == "Effroi":
      pts = 10 * user.get_level()
      target.capacity_modify(3 -pts)
      msg += f"{target.name} perd {pts} points de Courage."

    elif power_name == "Guérison":
      for player_id in self.players:
        if player_id < 0: next
        player = self.id_to_object(player_id)
        if player.place == user.place and player.stat[5] < 100:
          player.stat[5] = 100
          msg += f" - {players.name} a retrouvé 100 points de Vie.\n"

    elif power_name == "Chant":
      pts = 5 * user.get_level()
      for player_id in self.players:
        if player_id < 0: next
        player = self.id_to_object(player_id)
        if player.place == user.place:
          player.stat[0] += pts
          player.stat[1] += pts
          msg += f" - {player.name} gagne {pts} points de Courage et de Force.\n"

    elif power_name == "Invocation":
      pts = 5 * user.get_level()
      for capacity_index in (1, 2):
        target.capacity_modify(capacity_index, -pts)
      msg += f"{target.name} perd {pts} points de Force et d'Habileté."

    elif power_name == "Poison":
      pts = 10 * user.get_level()
      target.capacity_modify(5, -pts)
      msg += f"{target.name} perd {pts} points de Vie."

    elif power_name == "Régénération":
      pts = 3 * user.get_level()
      for capacity_index in range(4): # From Courage to Rapidity
        user.capatity_modify(capacity_index, pts)
      msg += f"{user.name} gagne {pts} points de Courage, de Force, d'Habileté et de Rapidité."

    elif power_name == "Charme":
      pts = 3 * user.get_level()
      for capacity_index in range(4):
        target.capacity_modify(capacity_index, -pts)
      msg += f"{target.name} perd {pts} points de Courage, de Force, d'Habileté et de Rapidité."

    elif power_name == "Boule de feu":
      pts = 10 * user.get_level()
      for capacity_index in (0, 1, 5):
        target.capacity_modify(capacity_index, -pts)
      msg += f"{target.name} perd {pts} points de Courage, de Force et de Vie."
      
    return msg

  def roll_dice(self, message):
    user = self.id_to_object(get_user(message)[1])
    
    if not user:
      return f"*Erreur : {get_user(message)[0]} n'existe pas.*"

    args = analyse(message)
    
    if not args:
      faces, nb = 20, 1
      
    elif len(args) == 1:
      faces, nb = args[0], 1
      
    elif len(args) == 2:
      faces, nb = args[0], args[1]
      
    else:
      return "*Erreur : syntaxe invalide `+dé < nb_de_faces >, < nb_de_dés >`.*"
    
    return f"{user.name} lance {nb} dé(s) à {faces} faces. Résultat obtenu : {roll_die(faces, nb)} / {faces * nb}."

  def roll_capacity(self, message):
    user = self.id_to_object(get_user(message)[1])
    if not user:
      return f"*Erreur : {get_user(message)[0]} n'est pas un joueur enregistré.*"
    
    capacity_name = analyse(message)[0].capitalize()
    
    try:
      capacity_index = ["Courage", "Force", "Habileté", "Rapidité", "Défense", "", "Mana"].index(capacity_name)
    except:
      return f"*Erreur : {capacity_name} n'est pas une capacité.*"
    
    if user.capacity_roll(capacity_index):
      result = f"{user.name} a réussi"
    else:
      result = f"{user.name} a râté"

    result += " son lancer "
    
    if capacity_index == 2:
      result += "d'Habileté."
    else:
      result += f"de {capacity_name}."

    return result

  def place_change(self, message):
    user = self.id_to_object(get_user(message)[1])
    if not user:
      return "*Erreur : {get_user(message)[0]} n'est pas un joueur enregistré.*"

    new_place = analyse(message)
    if not new_place:
      return "*Erreur : syntaxe invalide `+lieu < nom_du_lieu >`.*"
    
    user.place = new_place[0]
    return f"{user.name} se dirige vers {user.place}."

  def show_articles(self, message):
    user = self.id_to_object(get_user(message)[1])
    if not user:
      return f"*Erreur : {get_user(message)[0]} n'est pas un joueur enregistré.*", -1

    shop_name = user.inshop()
    if not shop_name:
      return f"*Erreur : {user.name} n'est pas dans un magasin.*", -1

    item_name = analyse(message)
    
    if item_name:
      item_name = item_name[0]
      if item_name in data_shop()[shop_name]:
        stat = object_stat(item_name)[0]
        return f"**{item_name}**\n - Courage : {stat[0]}\n - Force : {stat[1]}\n - Habileté : {stat[2]}\n - Rapidité : {stat[3]}\n - Défense : {stat[4]}\n - Vie : {stat[5]}\n - Mana : {stat[6]}\n - Prix : {abs(stat[7])} Drachmes", -1
      else:
        return "*Erreur : cet objet n'est pas vendu ici. Consultez les objets disponibles via : `+article`.*", -1

    else:
      return (user.place, data_shop()[shop_name]), user.stat[8]

  def buy(self, message):
    user = self.id_to_object(get_user(message)[1])
    if not user:
      return f"*Erreur : {get_user(message)[0]} n'est pas un joueur enregistré.*"

    shop_name = user.inshop()
    if not shop_name:
      return f"*Erreur : {user.name} n'est pas dans un magasin.*"
    
    item_name = analyse(message)
    if not item_name:
      return f"*Erreur : syntaxe invalide `+achat < nom_de_l'objet >`."

    item_name = item_name[0]
    
    if item_name not in data_shop()[shop_name]:
      return "*Erreur : cet objet n'est pas vendu ici. Consultez les objets disponibles via : `+article`.*"

    price = object_stat(item_name)[0][7]
    user.object_add(item_name)
    user.stat[7] += price
    return f"{user.name} a acheté {item_name} pour le prix de {abs(price)} Drachmes."

  def object_take(self, message):
    user = self.id_to_object(get_user(message)[1])
    if not user:
      return "*Erreur : {get_user(message)[0]} n'est pas un joueur enregistré.*"

    object_name = analyse(message)

    if not object_name:
      return "*Erreur : syntaxe invalide `+prend < nom_de_l'objet >`.*"

    object_name = object_name[0]
    
    if object_name in user.inventory:
      return f"*Erreur : {user.name} a déjà cet objet.*"
    
    user.object_add(object_name)
    return f"{user.name} prend {object_name}."

  def object_give(self, message):
    user = self.id_to_object(get_user(message)[1])
    if not user:
      return f"*Erreur : {get_user(message)[0]} n'est pas un joueur enregistré.*"
    args = analyse(message)

    if len(args) > 3:
      return "*Erreur : syntaxe invalide `+donne < nom_du_receveur >, < nom_de_l'objet >`.*"
    
    player = self.id_to_object(self.nick_to_id(args[0]))
    
    if not player:
      return f"*Erreur : {args[0]} n'existe pas.*"
    
    if args[1].lower() == "argent":
      amount = abs(args[2])
      
      if amount > user.stat[7]:
        return f"*Erreur : {user.name} ne peut pas donner de Drachmes.*"

      user.stat[7] -= amount
      player.stat[7] += amount

      return f"{user.name} donne {amount} Drachmes à {player.name}."
      
    else:
      object_name = args[1]
      if object_name not in user.inventory:
        return f"*Erreur : {user.name} ne possède pas cet objet : '{object_name}'.*"
      elif object_name in player.inventory:
        return f"*Erreur : {player.name} a déjà cet objet.*"
    
      user.object_del(object_name)
      player.object_add(object_name)
    
      return f"{user.name} donne {object_name} à {player.name}."

  def object_throw(self, message):
    user = self.id_to_object(get_user(message)[1])
    if not user:
      return "*Erreur : {get_user(message)[0]} n'est pas un joueur enregistré.*"
    
    object_name = analyse(message)

    if not object_name:
      return "*Erreur : syntaxe invalide `+jette < nom_de_l'objet >`.*"

    object_name = object_name[0]

    if object_name not in user.inventory:
      return f"*Erreur : {user.name} ne possède pas cet objet : '{object_name}'*."

    user.object_del(object_name)
    
    return f"{user.name} jette {object_name}." 

# --- Administration --- #

  def save(self):
    save_delete()
    player_file = [object_to_save(player) for player in self.players.values()]
    save_file = [player_file, self.kick]
    save_send(str(save_file))
    print("Partie sauvegardée.")

  def player_modify(self, message):
    if get_user(message)[1] not in data_admin():
      return "*< commande non autorisée >*"
    
    user = self.id_to_object(get_user(message)[1])

    player_name, capacity_name, new_value = analyse(message)
    player = self.id_to_object(self.nick_to_id(player_name))


    capacity_name = capacity_name.lower()
    capacity_list = ("courage", "force", "habileté", "rapidité", "défense", "vie", "mana", "argent")
    
    if capacity_name in capacity_list:
      player.capacity_modify(capacity_list.index(capacity_name), new_value)
      result = f"{player.name} " + ("perd", "gagne")[new_value > 0] + f" {new_value} "
      
      if capacity_name == "habileté":
        result += "point(s) d'Habileté."
        
      elif capacity_name == "argent":
        result += "Drachmes."
        
      else:
        result += f"point(s) de {capacity_name}."

    elif capacity_name == "lieu":
      player.place = new_value
      result = f"{player.name} se dirige vers {new_value}."

    elif capacity_name == "objet+":
      if new_value not in player.inventory:
        player.object_add(new_value)
        result = f"{player.name} reçoit {new_value}."
      else:
        resutl = f"{player.name} a déjà {new_value}."

    elif capacity_name == "objet-":
      if new_value in player.inventory:
        player.object_del(new_value)
        result = f"{player.name} a perdu {new_value}."
      else:
        result = f"{player.name} ne possède pas cet objet : '{new_value}'."
      

    else:
      result = "*Erreur : la capacité saisie ne correspond à aucune capacité connue.*"

    if not player.isalive():
      result += f"\n{player.name} a succombé a ses blessures."
      self.players.pop(player.id)
    
    return result

  def player_kick(self, message):
    if get_user(message)[1] not in data_admin():
      return "*< commande non autorisée >*"

    player_name = analyse(message)[0]
    player_id = self.nick_to_id(player_name)
    
    if not player_id:
      return f"*Erreur : {player_name} n'existe pas.*"
      
    self.kick.append(int(player_id))
    self.players.pop(player_id)
    return f"{player_name} a été kické."

  def player_unkick(self, message):
    if get_user(message)[1] not in data_admin():
      return "*< commande non autorisée >*"

    player_id = int(analyse(message)[0])
    for i in self.kick:
      if i == player_id:
        self.kick.remove(player_id)
        return f"Le joueur n°{player_id} a été unkick."

    return f"*Erreur : le joueur ciblé n'est pas kické.*"

  def clear_kick(self, message):
    if get_user(message)[1] not in data_admin():
      return "*< commande non autorisée >*"

    self.kick = []
    
    return "Tous les joueurs kickés ont été unkick."

  def clear_player(self, message):
    if get_user(message)[1] not in data_admin():
      return "*< commande non autorisée >*"

    self.players = {}
    
    return "Tous les joueurs ont été supprimés."

  def clear_all(self, message):
    if get_user(message)[1] not in data_admin():
      return "*< commande non autorisée >*"

    self.player = {}
    self.kick = []

    return "Sauvegarde effacée."

  
