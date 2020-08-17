import sys

sys.path.append("/home/bertik23/Programming/BDBF")
#print(sys.path)

import bdbf

import discord

print(discord.version_info)

bdbf.commands.commandPrefix = "%"

class ahoj(bdbf.commands.Command):
	async def command(self, args, message):
		return f"Ahoj {message.author.mention}", None

class zdar(bdbf.commands.Command):
	async def command(self, args, message):
		for i in range(int(args)):
			yield f"Zdravím {i}", None

bdbf.commands.cmds["all"].extend([ahoj(),zdar()])

client = discord.Client()

@client.event
async def on_message(message):
	await bdbf.commands.checkForCommands(message)

client.run("token")
