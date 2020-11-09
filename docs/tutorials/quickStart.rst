.. highlight:: python

Quick Start
===========

This Quick Start assumes you have some knowledge of making a discord bot in python.

Usage
^^^^^
1. Import bdbf
::
    import bdbf

2. Setup your client
::
   client = bdbf.Client(
                botName="BDBF Bot",
                commandPrefix="%",
                embedFooter={
                        "icon_url": "example.com/image.png",
                        "text": "Made using BDBF"
                    },
                embedColor=(123,123,123))

3. Setup the rest like normal
::
   @client.event
   async def on_message(message):
       #some code

   client.run("token")

4. To make a command use the wrapper ``client.command`` 
::
    @client.command("hi")
    async def hi(message):
        await message.channel.send(f"Hello {msg.author.mention}")

    @client.command("sayHelloTo")
    async def sayHelloTo(message, *args):
        await message.channel.send(f"Hello {args[0]}")

Beware that the command function has to be a coroutine and that args is a tuple with 0 or 1 items

And that's it, you should now have a working bot.