import __init__
from __init__ import embed
import discord

cmds = []
__init__.commandPrefix = "~"

class Command:
	def __init__(self, description:str= None, usage: str= None):
		if description:
			self.description = description
		else:
			self.description = f"{self} description"
		self.usage = usage

	def command(self,args):
		pass
	def __str__(self):
		return f"{type(self)}".split("'")[1].split(".")[1]

class help(Command):
	def command(self,args):
		fields = []
		for cmd in cmds:
			fields.append({"name": f"{__init__.commandPrefix}{cmd}", "value": f"{cmd.usage if cmd.usage else ''}"+('\n' if cmd.usage else '')+f"{cmd.description}"})
		print(fields)
		return fields
		return embed(f"Help for {__init__.botName}",fields=fields)

def checkForCommands(msg: discord.Message ,commandsList:list):
	message = msg.content
	if len(message) != 0:
		if message[0] == __init__.commandPrefix:
			if len(message[1:].split(" ", 1)) == 1:
				cmd, args = message[1:], None
			else:
				cmd, args = message[1:].split(" ", 1)[0], message[1:].split(" ",1)[1]
		else:
			cmd, args = None, None
	else:
		cmd, args = None, None
	for command in commandsList:
		if cmd == str(command):
			command.command(args)


c = Command()
h = help("Returns this",f"{__init__.commandPrefix}help")
print(c.description)
print(h.description)


cmds = [h]

class TestMSG:
	def __init__(self):
		self.content = "~help"
tstMsg = TestMSG()

#print(h.command(None))

checkForCommands(tstMsg, cmds)