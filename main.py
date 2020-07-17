# --------------------------------------------------
# Odyssée (Version dev)
# by LeRoiDesKiwis and Sha-Chan~
# last version released on the … of … 2020
#
# code provided with licence :
# GNU General Public Licence v3.0
# --------------------------------------------------

from piscord import Handler
from lib_RolePlay import role_play
import os

odyssee = Handler(os.environ['token'], "+")

@bot.event("on_ready")
def ready(ready):
  print(f"{ready.user.name} online and connected.")

@bot.event("on_message")
def message(messgage):
   answer = role_play(message.author.nick, message.author.id, message.content[1:])
    

