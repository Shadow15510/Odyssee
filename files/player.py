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
        stat += [randint(25, 50 * level), 0, randint(2, 10 * level), color]
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
            return max(match.keys()), match[max(match.keys())]

    def search_all(object_name):
        match = {}
        database = data_shop()

        for shop in database:
            rslt = auto_complete(database[shop], object_name)
            if rslt:
                match[rslt[0]] = (rslt[1], shop)

        if match:
            name, shop = match[max(match.keys())]
            statistic = database[shop][name]
            return name, list(statistic[0].values()), statistic[1]

        return "", [0 for _ in range(8)], -1

    def search_shop(object_name, shop_name):
        database = data_shop()[shop_name]

        _, name = auto_complete(database, object_name)
        if name:
            statistic = database[name]
            return name, list(statistic[0].values()), statistic[1]

        return "", [0 for _ in range(8)], -1

    object_name = object_name.lower()
    if shop_name:
        return search_shop(object_name, shop_name)
    else:
        return search_all(object_name)
            
# --- get the power --- #

def get_power_by_species(species_name):
    species_list = data_species()
    power_by_species = data_power_by_species()
            
    for species in power_by_species:
        if species_name in species_list[species]:
            return power_by_species[species]
    return []

# --------------------------------------------------
# Player object
# --------------------------------------------------

class Player:
    def __init__(self, identifier, name, species, stat=None, place="< inconnu >", inventory=None, note=None, power=None):
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

        if power: self.power = power
        else: self.power = get_power_by_species(self.species)

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
        return self.power

    def have(self, object_name):
        name, _, ref_check = object_stat(object_name)
        if name: object_name = name

        for index, item in enumerate(self.inventory):
            name, stat, stockable = object_stat(item[0])
            if (stockable == -1 and item[0] == object_name) or name == object_name: 
                return index, stat, stockable
        return -1, -1, ref_check

    def find_by_type(self, *object_type):
        for item in self.inventory:
            _, stat, check = object_stat(item[0])
            if check in object_type: return item[0], stat
        return None, None

    # --- Modify player --- #

    def stat_add(self, stat_to_add): # From Courage to Mana (include Health, but neither money nor color)
        for i in range(7): self.capacity_modify(i, stat_to_add[i])

    def stat_sub(self, stat_to_sub):
        for i in range(7): self.capacity_modify(i, -stat_to_sub[i])

    def object_add(self, object_name):
        index = self.have(object_name)[0]
        _, stat, stockable = object_stat(object_name)
        if stockable in (1, 5):           
            if index + 1:
                self.inventory[index][1] += 1
            else:
                self.inventory.append([object_name, 1])
            return True
        else:
            if stockable != 2: self.inventory.append([object_name, -1])
            if stockable == 0: self.stat_add(stat)

    def object_del(self, object_name):
        index, stat, stockable = self.have(object_name)
        if stockable in (1, 5):
            self.inventory[index][1] -= 1
            if self.inventory[index][1] <= 0: self.inventory.pop(index)
        else:
            self.inventory.pop(index)
            if stockable == 0: self.stat_sub(stat)

    def object_use(self, object_name):
        index, stat, _ = self.have(object_name)
        self.inventory[index][1] -= 1
        if self.inventory[index][1] <= 0:
            self.inventory.pop(index)

        self.stat_add(stat)

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

    def power_add(self, power_name):
        power_id = data_power_index(power_name)
        if not power_id:
            return 0
        elif power_id in self.power:
            return 1
        else:
            self.power.append(power_id)
            return 2

    def power_sub(self, power_name):
        power_id = data_power_index(power_name)
        if not power_id:
            return 0
        elif power_id not in self.power:
            return 1
        else:
            self.power.remove(power_id)
            return 2

# --------------------------------------------------
# Database
# --------------------------------------------------

# --- Colors --- #

def data_color():
    return {
        "noir":0x121212,
        "caramel":0xcc9900,
        "turquoise":0x00ced1,
        "vert":0x00ff00,
        "rouge":0xff0000,
        "bleu":0x0099ff,
        "jaune":0xffd700,
        "orange":0xffa500,
        "violet":0xff00ff,
        "rose":0xff69b4}


# --- Travel --- #
def data_travel_mean():
    return {
        # terre
        "marche lente": (2.5, 10, 0),
        "marche rapide": (5, 7, 0),
        "charrette": (4.8, 8, 0),
        "cheval": (8, 8, 0),
        "poney": (6.4, 5, 0),

        # mer
        "barque": (2.4, 5, 1),
        "voilier": (3.2, 8, 1),
        "goélette franche": (9.3, 10, 1),
        "frégate légère": (3.2, 10, 1),
        "caravelle": (4.8, 12, 1),
        "galion": (6.4, 12, 1)
    }


def data_travel_land():
    return {
        "plaine": (1, 1, 0.75),
        "colline": (1, 0.75, 0.5),
        "montagne": (0.75, 0.75, 0.5),
        "forêt": (1, 1, 0.5),
        "jungle": (1, 0.75, 0.25),
        "marécage": (1, 0.75, 0.25),
        "désert": (1, 0.5, 0.5),
        "neige": (1, 0.75, 0.75)
    }

def data_travel_weather():
    return {
        "canicule": (0.75, 0.75),
        "beau temps": (1, 1),
        "nuageux": (1, 1),
        "venteux": (0.75, 1.25),
        "pluie": (0.75, 0.5),
        "orage": (0.5, 0.25),
        "grêle": (0.5, 0.25),
        "brouillard": (0.5, 0.25)
    }


def get_speed(mean, weather, land):
    data_mean = data_travel_mean()
    data_land_type = data_travel_land()
    data_weather = data_travel_weather()

    if mean in data_mean:
        per_hour, hour_per_day, land_type = data_mean[mean]
    else:
        return f"*Erreur : '{mean}' n'est pas un moyen de transport connu.*", 0, 0, 0, False

    if not land or land_type: land = (1, 1, 1)
    elif land:
        if land in data_land_type:
            land = data_land_type[land]
        else:
            return f"*Erreur : '{land_type}' n'est pas un terrain connu.*", 0, 0, 0, False

    if weather in data_weather:
        weather = data_weather[weather][land_type]  
    else:
        return f"*Erreur : '{weather}' n'est pas une météo connue.*", 0, 0, 0, False

    per_hour *= weather

    return [per_hour * i for i in land], [per_hour * hour_per_day * i for i in land], hour_per_day, land_type, True
        

# --------------------------------------------------
# Conversion tool for the save file
# --------------------------------------------------

def object_to_save(player):
    return [player.id, player.name, player.species, player.stat, player.place, player.inventory, player.note, player.power]

def save_to_object(save):
    return Player(*save)


