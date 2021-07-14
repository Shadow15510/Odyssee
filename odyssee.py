# --------------------------------------------------
# Odyssée (version 5.0.1)
# by Sha-chan~
# last modification on July 13, 2021
#
# code provided with licence :
# GNU General Public Licence v3.0
# --------------------------------------------------

# [odyssee.py] > commands.py > lib_odyssee.py > objects.py > shop.py

import json
import discord
from discord.ext import commands

from libs.commands import OdysseeCommands, load_save
from libs.administration import AdminCommands

with open("config.json", "r") as file:
    config = json.load(file)

odyssee = commands.Bot(command_prefix=config["PREFIX"], strip_after_prefix=True)

save = load_save()

for cmnd_module in (OdysseeCommands, AdminCommands):
    odyssee.add_cog(cmnd_module(config, save))

odyssee.run(config["TOKEN"])
