# Statistiques : Courage (0), Force (1), Habileté (2), Rapidité (3) Défense (4), Vie (5), Mana (6), Argent (7), Couleur (8)

from random import randint
from files.shop import *
from files.power import *
from files.save import *

# --------------------------------------------------
# Misceleanous
# --------------------------------------------------

# --- Statistics generator --- #

def stat_gen(level=1, color=None, enemy=False):
    if level < 1: level = 1
    if not color: color = randint(0, 16777215)
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

def object_stat(object_name, shop_name=None):
    def auto_complete(database, name):
        match = {len(item_name): item_name for item_name in database if item_name in name}
        if match:
            return match[max(match.keys())]

    def search(shop, object_name):
        name = auto_complete(shop, object_name)
        if name:
            statistic = shop[name]
            return name, list(statistic[0].values()), statistic[1]

        return "", [0 for i in range(8)], -1

    database = data_shop()
    if shop_name:
        return search(database[shop_name], object_name)
    else:
        for shop_name in database:
            name, stat, check = search(database[shop_name], object_name)
            if check != -1: return name, stat, check
        return "", [0 for _ in range(8)], -1
        
            

# --------------------------------------------------
# Player object
# --------------------------------------------------

class Player:
    def __init__(self, identifier, name, species, stat=None, place="< inconnu >", inventory=None, note=None):
        self.id = identifier
        self.name = name
        self.species = species
        self.place = place

        if stat: self.stat = stat
        else: self.stat = stat_gen()
        
        if inventory: self.inventory = inventory
        else: self.inventory = list()

        if note: self.note = note
        else: self.note = [[0, ""]]

    # --- Get information from player --- #

    def isalive(self):
        return self.stat[5] > 0

    def get_level(self):
        return (sum(self.stat[:4]) // 80) + 1

    def capacity_roll(self, capacity_index):
        point = ((roll_die() + self.stat[capacity_index]) / (40 * self.get_level()))
        if point >= 0.75:
            return 3
        elif point >= 0.5:
            return 2
        elif point >= 0.25:
            return 1
        else: return 0

    def get_stat(self):
        return [self.name, self.species, self.get_level()] + self.stat + [self.place, self.inventory, self.note]

    def inshop(self):
        for shop_key, all_shop_name in data_shop_name().items():
            for name_to_detect in all_shop_name:
                if name_to_detect in self.place.lower(): return shop_key
        return False

    def get_special_powers(self):
        species_list = data_species()
        power_by_species = data_power_by_species()
        
        for species in power_by_species:
            if self.species in species_list[species]:
                return power_by_species[species]
        return []

    def have(self, object_name):
        name, _, _ = object_stat(object_name)
        if name: object_name = name

        for index, item in enumerate(self.inventory):
            name, stat, stockable = object_stat(item[0])
            if (stockable == -1 and item[0] == object_name) or name == object_name: 
                return index, stat, stockable
        return -1, -1, -1

    # --- Modify player --- #

    def stat_add(self, stat_to_add): # From Courage to Mana (include Health, but neither money nor color)
        for i in range(7): self.capacity_modify(i, stat_to_add[i])

    def stat_sub(self, stat_to_sub):
        for i in range(7): self.capacity_modify(i, -stat_to_sub[i])

    def object_add(self, object_name):
        index = self.have(object_name)[0]
        _, stat, stockable = object_stat(object_name)
        if stockable == 1:           
            if index + 1:
                self.inventory[index][1] += 1
            else:
                self.inventory.append([object_name, 1])
            return True
        else:
            if stockable != 2: self.inventory.append([object_name, -1])
            self.stat_add(stat)


    def object_del(self, object_name):
        index, stat, stockable = self.have(object_name)
        if stockable == 1:
            self.inventory[index][1] -= 1
            if self.inventory[index][1] <= 0: self.inventory.pop(index)
        else:
            self.inventory.pop(index)
            self.stat_sub(stat)

    def object_use(self, object_name):
        index = self.have(object_name)[0]
        self.inventory[index][1] -= 1
        if self.inventory[index][1] <= 0:
            self.inventory.pop(index)

        self.stat_add(object_stat(object_name)[1])

    def capacity_modify(self, capacity_index, amount):
        self.stat[capacity_index] += amount
        if self.stat[capacity_index] < 0: self.stat[capacity_index] = 0

    def add_note(self, note):
        if len(self.note) == 1 and not self.note[0][0]:
            self.note[0] = [1, note]
        else:
            self.note.append([len(self.note) + 1, note])

    def del_note(self, note_index):
        if len(self.note) >= note_index:                
            for index in range(note_index - 1, len(self.note)): self.note[index][0] -= 1

            content = self.note[note_index - 1][1]
            del(self.note[note_index - 1])
            if not self.note:
                self.note.append([0, ""])
            return content

# --------------------------------------------------
# Database
# --------------------------------------------------

# --- Colors --- #

def data_color():
    return {
        "noir":0x000000,
        "caramel":0xcc9900,
        "turquoise":0x00ced1,
        "vert":0x00ff00,
        "rouge":0xff0000,
        "bleu":0x0099ff,
        "jaune":0xffd700,
        "orange":0xffa500,
        "violet":0xff00ff,
        "rose":0xff69b4}

# --- Species --- #

def data_species():
    return [
        ["Elfe", "Elfe sylvestre", "Druide"],
        ["Humain", "Mage", "Magicienne", "Magicien", "Cavalière", "Cavalier"],
        ["Troll", "Orque", "Ogre", "Cyclope"],
        ["Naine", "Nain"],
        ["Gnome", "Gobelin"],
        ["Nazgul", "Cavalière noire", "Cavalier noir"],
        ["Succube", "Incube"],
        ["Vampire"],
        ["Hobbit"],
        ["Satyre"],
        ["Nymphe"],
        ["Guivre"],
        ["Centaure"],
        ["Dragon", "Dragonne"],
        ["Minotaure"],
        ["Efrit", "Démon"],
        ["Follasse"],
        ["Dieu", "Déesse"]]

# --- Special powers --- #

def data_power_by_species():
    return {
        0: [0, 3, 7],      # Elfe
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
        16: [0, 3],        # Follasse
        17: [3, 10, 11],   # Dieu
        }

# --------------------------------------------------
# Conversion tool for the save file
# --------------------------------------------------

def object_to_save(player):
    return [player.id, player.name, player.species, player.stat, player.place, player.inventory, player.note]

def save_to_object(save):
    return Player(*save)


