import bdbf.main
from bdbf.main import embed
from bdbf.exceptions import  *
import discord

cmds = {"all": []}
commandPrefix : str = None

class Command:
	def __init__(self, description:str= None, usage: str= None):
		if description:
			self.description = description
		else:
			self.description = f"{self} description"
		self.usage = usage

	async def command(self,args):
		pass
	def __str__(self):
		return f"{type(self)}".split("'")[1].split(".")[-1]
	def __repr__(self):
		return self.__str__()

class help(Command):
	async def command(self,args):
		fields = []
		for cmd in cmds["all"]:
			fields.append({"name": f"{commandPrefix}{cmd}", "value": f"{cmd.usage.replace('%commandPrefix%',commandPrefix) if cmd.usage else ''}"+('\n' if cmd.usage else '')+f"{cmd.description}"})
		try:
			for cmd in cmds[args]:
				fields.append({"name": f"{commandPrefix}{cmd}", "value": f"{cmd.usage.replace('%commandPrefix%',commandPrefix) if cmd.usage else ''}"+('\n' if cmd.usage else '')+f"{cmd.description}"})
		except KeyError:
			pass
		return "",embed(f"Help for {bdbf.botName}",fields=fields)

async def checkForCommands(msg: discord.Message):
	message = msg.content
	commandOut = None
	try:
		if len(message) != 0:
			if message[:len(commandPrefix)] == commandPrefix:
				if len(message[len(commandPrefix):].split(" ", 1)) == 1:
					cmd, args = message[len(commandPrefix):], None
				else:
					cmd, args = message[len(commandPrefix):].split(" ", 1)[0], message[1:].split(" ",1)[1]
			else:
				cmd, args = None, None
		else:
			cmd, args = None, None
		for command in cmds["all"]:
			if cmd == str(command):
				if cmd == "help":
					args = msg.channel.guild.id
				commandOut = await command.command(args)

		try:
			for command in cmds[msg.channel.guild.id]:
				if cmd == str(command):
					commandOut = await command.command(args)
		except KeyError:
			pass

		if commandOut != None:
			await msg.channel.send(commandOut[0], embed=commandOut[1])

	except TypeError:
		if commandPrefix == None:
			raise NoCommandPrefix("You haven't set a command prefix")
		else:
			raise NoCommandPrefix(f"Your commandPrefix is {type(commandPrefix)}, but it must be a string")



h = help("Returns this","%commandPrefix%help")

cmds["all"].append(h)

"""print(c.description)
print(h.description)

class TestMSG:
	def __init__(self):
		self.content = "~help"
tstMsg = TestMSG()

#print(h.command(None))

checkForCommands(tstMsg, cmds)"""