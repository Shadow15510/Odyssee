# --------------------------------------------------
# Odyssée (Version dev)
# by LeRoiDesKiwis and Sha-Chan~
# last version released on the … of … 2020
#
# code provided with licence :
# GNU General Public Licence v3.0
# --------------------------------------------------

# Statistiques : Courage (0), Force (1), Habileté (2), Rapidité (3) Défense (4), Vie (5), Mana (6), Argent (7), Couleur (8)

from random import randint

def stat_gen(level = 1, enemy = False):
  stat = [randint(20*(level-1), 20*level) for i in range(4)]
  stat.append(0)
  
  if enemy:
    stat += [randint(0, 5 * level), randint(50, 100), 0, randint(5, 25 * level), 0]
  else:
    stat += [100, 5, 15, 0]
  return stat

def roll_die(faces = 20, nb = 1):
  return randint(nb, nb * faces)

class Player:
  def __init__(self, identifier, name, species, stat = stat_gen(), place = "< inconnu >", inventory = []):
    self.id = identifier
    self.name = name
    self.stat = stat
    self.species = species
    self.place = place
    self.inventory = inventory

  # --- Get information from player --- #

  def isalive(self):
    return self.stat[5] > 0

  def get_level(self):
    return (sum(self.stat[:4]) // 80) + 1

  def capacity_roll(self, capacity_index):
    return ((roll_die() + self.stat[capacity_index]) / 40 * self.get_level()) >= 0.5

  def get_stat(self):
    return [self.name, self.species, self.get_level()] + self.stat + [self.place, self.inventory]

  # --- Modify player --- #

  def stat_add(self, stat_to_add): # From Courage to Mana (include Health, but neither money nor color)
    for i in range(7): self.stat[i] += stat_to_add[i]

  def stat_sub(self, stat_to_sub):
    for i in range(7): self.stat[i] -= stat_to_add[i]

  def object_add(self, object_name, object_stat):
    self.inventory.append(object_name)
    self.stat_add(object_stat)

  def object_del(self, object_name, object_stat):
    self.inventory.remove(object_name)
    self.stat_sub(object_stat)

  def capacity_modify(self, capacity_index, amount):
    self.stat[capacity] += amount

  def place_modify(self, new_place):
    self.place = new_place

  def species_modify(self, new_species):
    self.species = new_species

  def color_modify(self, new_color):
    self.color = new_color
    

  

  
