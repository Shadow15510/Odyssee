# --------------------------------------------------
# Odyssée (Version dev)
# by LeRoiDesKiwis and Sha-Chan~
# last version released on the … of … 2020
#
# Code provided with licence (CC BY-NC-SA 4.0)
# for more information about licence :
# https://creativecommons.org/licenses/by-nc-sa/4.0/
# --------------------------------------------------

from piscord import Handler
import os

odyssee = Handler(os.environ['token'], "+")

@bot.event("on_ready")
def ready(ready):
  print(f"{ready.user.name} online and connected.")

@bot.event("on_message")
def message(messgage):
   answer = role_play(message.author.nick, message.author.id, message.content[1:])
    

