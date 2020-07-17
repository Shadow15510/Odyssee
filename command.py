# --------------------------------------------------
# Odyssée (Version dev)
# by LeRoiDesKiwis and Sha-Chan~
# last version released on the … of … 2020
#
# code provided with licence :
# GNU General Public Licence v3.0
# --------------------------------------------------



def analyse(message):
  def get_arg(arguments):
    args = [i.strip() for i in arguments.split(",")]
    return [int(i) if i.isdigit() else i for i in args]

  command, arguments = message.split(" ", 1)
  
  return command, get_arg(arguments)
    
def role_play(nickname, identifier, message):
  command, argument = analyse(message)
  
# === bot's functions without argument === #

  if command == "article": # Shows articles available
    show_articles(identifier)

  if command == "fuite": # Allows to run away from an enemy
    run_away(identifier)

  if command == "liste": # Get the list of registrated players
    player_list(identifier)

  if command == "sauvegarde": # Force the game save
    save(identifier)

# === bot's functions with optionnal argument === #

  if not command == "combat": # Start or continue a fight
    # expected argument : enemy's name [default : empty returns the fights list]                      
    fight_new(*argument, identifier)
    fight_continue(*argument, identifier)
    fight_list()

  if not command in ("stat", "stats", "info"): # Shows informations on the targeted player
    # expected argument : player's name [default : the player who called]
    information(identifier, *argument)

  if not command == "couleur": # Change the player's color
    # expected argument : new color's name or hexadecimal code [default : empty returns the list of the available color]
    color_change(*argument, identifier)
    color_list()

  if not command == "espèce": # Change the player's species
    # expected argument : the new player's spieces [default : empty return the list of available spieces]
    spieces_change(*argument, identifier)
    spieces_list()

  if not command == "pouvoir": # Have the description of the player's specials powers and use it
    # expected argument : special power's name, [target if needed] [default : empty returns the specials powers's list]
    specialpower_use(*argument, identifier)
    specialpower_list(identifier)

  if not command == "dé": # Roll a die
    # expected argument : dice numbers, number of faces per die [default : 1 die, 20 faces]
    roll_dice(*argument)

# === bot's functions with several argument == #

  if not command == "new": # Creating a new player
    # expected argument : player's spieces
    new_player(*argument, identifier)

  if not command == "lieu": # Changes the player's place
    # expected argument : the new place
    place_change(*argument, identifier)

  if not command == "achat": # Buying an item
    # expected argument : item's name
    buy(*argument, identifier)

  if not command == "lancer": # Roll a die in an ability
    # expected argument : the capacity's name
    roll_capacity(*argument, identifier)

  if not command == "prend": # Take an object
    # expected argument : the object's name
    object_take(*argument, identifier)

  if not command == "donne": # Give an object to a player, this can be money (object_name == Drachmes)
    # expected argument : the player's name, the object's name
    object_give(identifier, *argument)

  if not command == "jette": # Throw an object
    # expected argument : the object's name
    object_throw(*argument, identifier)

# === bot's function for administration === #

  if not command == "modifier": # Change the player or enemy statistics
    # expected argument : player's name, stat's name, amount
    player_modify(*argument, identifier)

  if not command == "kick": # Delete the player from the save and block him (he can't recreate a player)
    # expected argument : the player's name
    player_kick(*argument, identifier)

  if not command == "unkick": # Allow to the kicked user to create a player
    # expected argument : the player's name
    player_unkick(*argument, identifier)

  if command == "vider": # Clear the kick of kicked users
    clear_kick(identifier)

  if command == "formater": # Clear all the player, and reset the save file
    clear_player(identifier)
    

# === Without argument === #

def show_articles(identifier):
  return None

def run_away(identifier):
  return None

def player_list(identifier):
  return None

def save(identifier):
  return None

# === With optionnal argument === #

def fight_new(enemy_name, identifier):
  return None

def fight_continue(enemy_name, identifier):
  return None

def fight_list():
  return None

def information(player_name, identifier):
  return None

def color_change(new_color, identifier):
  return None

def color_list():
  return None

def spieces_change(new_spiecies, identifier):
  return None

def spieces_list():
  return None

def specialpower_use(power_name, target, identifier):
  return None

def specialpower_list(identifier):
  return None

def roll_dice(faces = 20, nb = 1):
  return None

# === With several argument === #

def new_player(species, identifier):
  return None

def place_change(new_place, identifier):
  return None

def buy(object_name, identifier):
  return None

def roll_capacity(capacity_name, identifier):
  return None

def object_take(object_name, identifier):
  return None

def object_give(identifier, player_name, object_name, amount = 0):
  return None

def object_throw(object_name, identifier):
  return None

# === Administration functions === #

def player_modify(player_name, capacity_name, amount, identifier):
  return None

def player_kick(player_name, identifier):
  return None

def player_unkick(player_name, identifier):
  return None

def clear_kick(identifier):
  return None

def clear_player(identifier):
  return None
    
