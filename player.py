# --------------------------------------------------
# Odyssée (Version 1.0)
# by Sha-Chan~
# last version released on the 30 of July 2020
#
# code provided with licence :
# GNU General Public Licence v3.0
# --------------------------------------------------

# Statistiques : Courage (0), Force (1), Habileté (2), Rapidité (3) Défense (4), Vie (5), Mana (6), Argent (7), Couleur (8)

from random import randint
from save import *

# --------------------------------------------------
# Misceleanous
# --------------------------------------------------

# --- Statistics generator --- #

def stat_gen(level = 1, color = 0, enemy = False):
  stat = [randint(20*(level-1), 20*level) for i in range(4)]
  stat.append(0)
  
  if enemy:
    stat += [randint(25, 50 * level), 0, randint(10 * level, 50 * level), color]
  else:
    stat += [100, 5, 15, color]
  return stat

# --- Roll a die --- #

def roll_die(faces = 20, nb = 1):
  return randint(nb, nb * faces)

# --- Get the object's statistic --- #

def object_stat(object_name):
  database= data_shop()
  for shop_name in database:
    if object_name in database[shop_name]:
      return list(database[shop_name][object_name].values()), shop_name in ("auberge", "officine")

  return [0 for i in range(8)], False

# --------------------------------------------------
# Player object
# --------------------------------------------------

class Player:
  def __init__(self, identifier, name, species, stat = stat_gen(), place = "< inconnu >", inventory = None):
    self.id = identifier
    self.name = name
    self.stat = stat
    self.species = species
    self.place = place
    
    if inventory:
      self.inventory = inventory
    else:
      self.inventory = list()

  # --- Get information from player --- #

  def isalive(self):
    return self.stat[5] > 0

  def get_level(self):
    return (sum(self.stat[:4]) // 80) + 1

  def capacity_roll(self, capacity_index):
    return ((roll_die() + self.stat[capacity_index]) / 40 * self.get_level()) >= 0.5

  def get_stat(self):
    return [self.name, self.species, self.get_level()] + self.stat + [self.place, self.inventory]

  def inshop(self):
    for shop_key, all_shopName in data_shopName().items():
      for name_to_detect in all_shopName:
        if name_to_detect in self.place.lower(): return shop_key
    return False

  def get_specialPowers(self):
    species_list = data_species()
    power_by_species = data_powerBySpecies()
    
    for species in power_by_species:
      if self.species in species_list[species]:
        return power_by_species[species]

    return []
    
  # --- Modify player --- #

  def stat_add(self, stat_to_add): # From Courage to Mana (include Health, but neither money nor color)
    for i in range(7): self.stat[i] += stat_to_add[i]

  def stat_sub(self, stat_to_sub):
    for i in range(7): self.stat[i] -= stat_to_sub[i]

  def object_add(self, object_name):
    stat, eatable = object_stat(object_name)
    if not eatable: self.inventory.append(object_name)
    self.stat_add(stat)

  def object_del(self, object_name):
    self.inventory.remove(object_name)
    self.stat_sub(object_stat(object_name)[0])

  def capacity_modify(self, capacity_index, amount):
    self.stat[capacity_index] += amount
    if self.stat[capacity_index] < 0: self.stat[capacity_index] = 0

# --------------------------------------------------
# Database
# --------------------------------------------------

# --- Shop and items --- #

def data_shopName():
  return {"auberge" : ["l'auberge","la taverne", "la gargote", "l'hôtel"],
          "forge" : ["la forge", "l'armurerie"],
          "officine" : ["la pharmacie", "l'herboristerie", "l'officine", "l'apothicairerie"],
          "tannerie" : ["la maroquinerie", "la tannerie"],
          "écurie" : ["l'écurie", "le haras"],
          "port" : ["le port"]}

def data_shop():
  return {"auberge":
     {"une chambre" : {"Courage":10, "Force":10, "Habileté":10, "Rapidité":10, "Défense":0, "Vie":25, "Mana":5, "Argent":-10},
      "un repas chaud" : {"Courage":10, "Force":10, "Habileté":0, "Rapidité":10, "Défense":0, "Vie":10, "Mana":0, "Argent":-7},
      "un repas frois" : {"Courage":5, "Force":5, "Habileté":0, "Rapidité":5, "Défense":0, "Vie":5, "Mana":0, "Argent":-5},
      "une bière" : {"Courage":2, "Force":2, "Habileté":2, "Rapidité":2, "Défense":0, "Vie":0, "Mana":0, "Argent":-2},
      "un lait de chèvre" : {"Courage":5, "Force":5, "Habileté":5, "Rapidité":5, "Défense":0, "Vie":5, "Mana":0, "Argent":-5},
      "du vin" : {"Courage":5, "Force":5, "Habileté":-2, "Rapidité":-1, "Défense":0, "Vie":1, "Mana":0, "Argent":-5},
      "de la viande séchée" : {"Courage":2, "Force":2, "Habileté":2, "Rapidité":2, "Défense":0, "Vie":2, "Mana":0, "Argent":-5},
      "du pain" : {"Courage":5, "Force":0, "Habileté":5, "Rapidité":0, "Défense":0, "Vie":5, "Mana":0, "Argent":-2},
      "du fromage" : {"Courage":0, "Force":10, "Habileté":0, "Rapidité":5, "Défense":0, "Vie":5, "Mana":0, "Argent":-5}},

   "forge":
     {"une épée" : {"Courage":0, "Force":0, "Habileté":15, "Rapidité":15, "Défense":10, "Vie":0, "Mana":0, "Argent":-20},
      "un arc" : {"Courage":25, "Force":0, "Habileté":15, "Rapidité":15, "Défense":0, "Vie":0, "Mana":0, "Argent":-70},
      "une hache" : {"Courage":10, "Force":10, "Habileté":15, "Rapidité":20, "Défense":0, "Vie":0, "Mana":0, "Argent":-50},
      "une arbalète" : {"Courage":5, "Force":0, "Habileté":15, "Rapidité":25, "Défense":0, "Vie":0, "Mana":0, "Argent":-40},
      "une côte de maille" : {"Courage":5, "Force":0, "Habileté":-5, "Rapidité":-5, "Défense":15, "Vie":0, "Mana":0, "Argent":-20},
      "une armure" : {"Courage":15, "Force":0, "Habileté":-10, "Rapidité":-10, "Défense":100, "Vie":0, "Mana":0, "Argent":-100},
      "un bouclier" : {"Courage":10, "Force":0, "Habileté":-10, "Rapidité":-5, "Défense":25, "Vie":0, "Mana":0, "Argent":-30},
      "une armure souple" : {"Courage":10, "Force":0, "Habileté":-5, "Rapidité":-10, "Défense":25, "Vie":0, "Mana":0, "Argent":-15},
      "une dague" : {"Courage":-5, "Force":-5, "Habileté":10, "Rapidité":10, "Défense":0, "Vie":0, "Mana":0, "Argent":-10},
      "un katana" : {"Courage":10, "Force":15, "Habileté":5, "Rapidité":5, "Défense":5, "Vie":0, "Mana":0, "Argent":-30},
      "une épée batarde" : {"Courage":10, "Force":15, "Habileté":-5, "Rapidité":-10, "Défense":10, "Vie":0, "Mana":0, "Argent":-30},
      "un arc long" : {"Courage":20, "Force":0, "Habileté":15, "Rapidité":10, "Défense":0, "Vie":0, "Mana":0, "Argent":-40},
      "un arc à double courbure" : {"Courage":10, "Force":20, "Habileté":10, "Rapidité":5, "Défense":0, "Vie":0, "Mana":0, "Argent":-50}},

   "officine":
     {"une potion de courage" : {"Courage":10, "Force":0, "Habileté":0, "Rapidité":0, "Défense":0, "Vie":0, "Mana":0, "Argent":-15},
      "une potion de force" : {"Courage":0, "Force":10, "Habileté":0, "Rapidité":0, "Défense":0, "Vie":0, "Mana":0, "Argent":-15},
      "une potion d'habileté" : {"Courage":0, "Force":0, "Habileté":10, "Rapidité":0, "Défense":0, "Vie":0, "Mana":0, "Argent":-15},
      "une potion de rapidité" : {"Courage":0, "Force":0, "Habileté":0, "Rapidité":10, "Défense":0, "Vie":0, "Mana":0, "Argent":-15},
      "une potion de vie" : {"Courage":0, "Force":0, "Habileté":0, "Rapidité":0, "Défense":0, "Vie":10, "Mana":0, "Argent":-15},
      "une potion de mana" : {"Courage":0, "Force":0, "Habileté":0, "Rapidité":0, "Défense":0, "Vie":0, "Mana":10, "Argent":-15},
      "une potion de puissance" : {"Courage":20, "Force":20, "Habileté":20, "Rapidité":20, "Défense":20, "Vie":20, "Mana":20, "Argent":-100}},

   "tannerie":
     {"des bottes" : {"Courage":10, "Force":0, "Habileté":0, "Rapidité":0, "Défense":5, "Vie":0, "Mana":0, "Argent":-15},
      "une cape" : {"Courage":0, "Force":5, "Habileté":0, "Rapidité":0, "Défense":10, "Vie":0, "Mana":0, "Argent":-15},
      "des bottes enchantées" : {"Courage":10, "Force":0, "Habileté":0, "Rapidité":0, "Défense":5, "Vie":0, "Mana":5, "Argent":-30},
      "une cape enchantée" : {"Courage":0, "Force":5, "Habileté":0, "Rapidité":0, "Défense":10, "Vie":0, "Mana":5, "Argent":-30}},

   "écurie":
     {"un cheval" : {"Courage":0, "Force":0, "Habileté":0, "Rapidité":0, "Défense":0, "Vie":0, "Mana":0, "Argent":-30}},

   "port":
     {"une barque" : {"Courage":0, "Force":0, "Habileté":0, "Rapidité":0, "Défense":0, "Vie":0, "Mana":0, "Argent":-40},
      "un voilier" : {"Courage":0, "Force":0, "Habileté":0, "Rapidité":0, "Défense":0, "Vie":0, "Mana":0, "Argent":-100},
      "une goélette franche" : {"Courage":0, "Force":0, "Habileté":0, "Rapidité":0, "Défense":0, "Vie":0, "Mana":0, "Argent":-200}}
   }


# --- Colors --- #

def data_color():
  return {"noir":0x000000,
          "caramel":0xcc9900,
          "turquoise":0x00ced1,
          "vert":0x00ff00,
          "rouge":0xff0000,
          "bleu":0x0099ff,
          "jaune":0xffd700,
          "orange":0xffa500,
          "violet":0xff00ff,
          "rose":0xff69b4}

# --- Administration --- #

def data_admin():
  return [565177655645962242]

# --- Species --- #

def data_species():
  return [
    ["Elfe", "Elf", "Druide", "Elfe sylvestre"],
    ["Humain", "Mage", "Magicienne", "Magicien", "Cavalière", "Cavalier"],
    ["Troll", "Orque", "Ogre", "Cyclope"],
    ["Naine", "Nain"],
    ["Gnome", "Gobelin"],
    ["Nazgul", "Cavalière noire", "Cavalier noir"],
    ["Succube"],
    ["Vampire"],
    ["Hobbit"],
    ["Satyre"],
    ["Nymphe"],
    ["Guivre"],
    ["Centaure"],
    ["Dragon", "Dragonne"],
    ["Minotaure"],
    ["Efrit", "Démon"],
    ["Follasse"]]

# --- Special powers --- #

def data_powers():
  return {
    0: ["Nyctalopie",
        "augmente votre Habilité et votre Rapidité.",
        False],
    
    1: ["Vol",
        "vous permet de voler votre adversaire sans le tuer.",
        True],
    
    2: ["Effroi",
        "fait chuter la Rapidité de votre adversaire.",
        True],
    
    3: ["Guérison",
        "soigne tous les joueurs à votre proximité, vous compris.",
        False],

    4: ["Chant",
        "augmente le Courage et la Force des joueurs qui écoutent.",
        False],

    5: ["Invocation",
        "fait chuter la Force et l'Habileté de votre adversaire.",
        True],

    6: ["Poison",
        "empoisonne votre adversaire.",
        True],

    7: ["Régénération",
        "fait monter toutes vos capacités.",
        False],

    8: ["Charme",
        "fait chuter toutes les capacités de votre adversaire.",
        True],

    9: ["Boule de feu",
        "fait brûler votre adversaire.",
        True]}

def data_powerIndex(power_name):
# Special power list :
#
# - Nyctalopie ..0
# - Vol .........1
# - Effroi ......2
# - Guérison ....3
# - Chant .......4
# - Invocation ..5
# - Poison ......6
# - Régénération 7
# - Charme ......8
# - Boule de feu 9
  powers = [
    "Nyctalopie",
    "Vol",
    "Effroi",
    "Guérison",
    "Chant",
    "Invocation",
    "Poison",
    "Régénération",
    "Charme",
    "Boule de feu"]
  
  if power_name in powers:
    return powers.index(power_name)

  return None

def data_powerBySpecies():
  return {0: [0, 5, 7], # Elfe
     1: [3, 6],         # Humain
     2: [2, 7],         # Troll
     3: [3, 4],         # Nain 
     4: [1, 3, 5],      # Gnome
     5: [1, 2, 6],      # Nazgul
     6: [3, 4, 8],      # Succube
     7: [0, 2, 7],      # Vampire 
     8: [4],            # Hobbit
     9: [1, 4],         # Satyre
     10: [4, 7, 8],     # Nymphe
     11: [6],           # Guivre
     12: [0, 4, 8],     # Centaure
     13: [2, 9],        # Dragon
     14: [2, 6],        # Minotaure
     15: [3, 5, 6],     # Démon
     16: [0, 3]}        # Follasse
 
# --------------------------------------------------
# Conversion tool for the save file
# --------------------------------------------------

def object_to_save(player):
  inventory = [save_convert(item) for item in player.inventory]
  return [player.id, save_convert(player.name), save_convert(player.species), player.stat, save_convert(player.place), inventory]

def save_to_object(save):
  save[1] = save_revert(save[1])
  save[2] = save_revert(save[2])
  save[4] = save_revert(save[4])
  save[5] = [save_revert(item) for item in save[5]]
  return Player(*save)


