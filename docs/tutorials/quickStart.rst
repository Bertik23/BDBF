.. highlight:: python

Quick Start
===========

This Quick Start assumes you have some knowledge of making a discord bot in python.

Instalation
^^^^^^^^^^^
1. Install the latest version of **bdbf** using ``pip install --upgrade bdbf``
2. Import **bdbf** using ``import bdbf``

Usage
^^^^^
1. Import bdbf and discord
::
	import bdbf
   	import discord

2. Setup your client
::
   client = discord.Client()

3. Name your bot
::
	bdbf.botName = "BDBF Bot"

4. Setup your embed color and footer
::
	bdbf.embedColor = (0,255,0)
   	bdbf.embedFooter = {
   		"icon_url": "example.com/image.png",
   		"text": "Made using BDBF"
   	}

5. Setup the rest like normal
::
   @client.event
   async def on_message(message):
       #come code

   client.run("token")

6. To make a command maka a class that will be the name of the command, that inherits from the ``bdbf.commands.Command`` class, than define the command function for the class
::
   	class info(bdbf.commands.Command):
		async def command(self, arguments):
			return "This is the info embed", embed(f"Information for {bdbf.botName}", description="This is the info command")

Beware that ``command`` is an *async* function and *arguments* is a single argument.
Also the ``command`` function has to return ``str, discord.Embed`` in that order (or None if you don't want that)

7. To be able to use the command you made, add it to the ``bdbf.commands.cmds`` dictionary. Use key "all" to use it in all guilds or the guild id to use it just there.
::
	bdbf.commands.cmds["all"].append(info(description="This is the info command",usage="%commandPrefix%info"))

8. Set a command prefix for your bot.
::
	bdbf.commands.commandPrefix = "&"

9. To be able to use the command, await the ``bdbf.commands.checkForCommands()`` function in ``on_message()``
::
	@client.event
	async def on_message(message):
		await bdbf.commands.checkForCommands(message)

And that's it you should now have a working bot.