import sys

sys.path.append("/home/bertik23/Programming/BDBF")
print(sys.path)

import bdbf

import discord

bdbf.commands.commandPrefix = "%"

client = discord.Client()

@client.event
async def on_message(message):
	await bdbf.commands.checkForCommands(message)

client.run("token")
