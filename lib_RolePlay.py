# --------------------------------------------------
# Odyssée (Version dev)
# by LeRoiDesKiwis and Sha-Chan~
# last version released on the … of … 2020
#
# code provided with licence :
# GNU General Public Licence v3.0
# --------------------------------------------------

def get_arg(message[0]):
  args = [i.strip() for i in message[0].split(",")]
  for i in range(len(args)):
    if args[i].isdigit(): args[i] = int(args[i])
  return args    
    
def role_play(nickname, identifier, message[0]):
  message = get_arg(message)
  
# === bot's functions with one argument === #

  if message[0] == "article": # Shows articles available
    show_articles()

  if message[0] == "fuite": # Allows to run away from an enemy
    run_away()

  if message[0] == "liste": # Get the list of registrated players
    player_list()

  if message[0] == "sauvegarde": # Force the game save
    save()

# === bot's functions with optionnal argument === #

  if not message[0].find("combat"): # Start or continue a fight
    # expected argument : enemy's name [default : empty returns the fights list]
    fight_new(message[1:])
    fight_continue(message[1:])
    fight_list(message[1:])

  if not message[0].find("stat"): # Shows informations on the targeted player
    # expected argument : player's name [default : the player who called]
    information()

  if not message[0].find("couleur"): # Change the player's color
    # expected argument : new color's name or hexadecimal code [default : empty returns the list of the available color]
    color_change()
    color_list()

  if not message[0].find("espèce"): # Change the player's species
    # expected argument : the new player's spieces [default : empty return the list of available spieces]
    spieces_change()
    spieces_list()

  if not message[0].find("pouvoir"): # Have the description of the player's specials powers and use it
    # expected argument : special power's name, [target if needed] [default : empty returns the specials powers's list]
    specialpower_list()
    sepcialpower_use()

  if not message[0].find("dé"): # Roll a die
    # expected argument : dice numbers, number of faces per die [default : 1 die, 20 faces]
    roll_dice()

# === bot's functions with several argument == #

  if not message[0].find("new"): # Creating a new player
    # expected argument : player's spieces
    new_player()

  if not message[0].find("lieu"): # Changes the player's place
    # expected argument : the new place
    place_change()

  if not message[0].find("achat"): # Buying an item
    # expected argument : item's name
    buy()

  if not message[0].find("drachme"): # Donate some Drachmes to another player
    # expected argument : player's name, amount
    donate()

  if not message[0].find("lancer"): # Roll a die in an ability
    # expected argument : the capacity's name
    roll_capacity()

  if not message[0].find("prend"): # Take an object
    # expected argument : the object's name
    object_take()

  if not message[0].find("donne"): # Give an object to a player
    # expected argument : the player's name, the object's name
    object_give()

  if not message[0].find("jette"): # Throw an object
    # expected argument : the object's name
    object_throw()

# === bot's function for administration === #

  if not message[0].find("modifier"): # Change the player or enemy statistics
    # expected argument : player's name, stat's name, amount
    player_modify()

  if not message[0].find("kick"): # Delete the player from the save and block him (he can't recreate a player)
    # expected argument : the player's name
    player_kick()

  if not message[0].find("unkick"): # Allow to the kicked user to create a player
    # expected argument : the player's name
    player_unkick()

  if message[0] == "vider": # Clear the kick of kicked users
    clear_kick()

  if message[0] == "formater": # Clear all the player, and reset the save file
    clear_player()
    
  
    

  
  
    
