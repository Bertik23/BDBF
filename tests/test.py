import bdbf
import logging
from discord_slash import SlashCommand

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

client = bdbf.Client(
    commandPrefix="%",
    logging=True,
    caseSensitiveCommands=False)

print(bdbf.__version__)

slash = SlashCommand(client)

thebotas = 540563312857841714


@client.command("test", doesntWorkInChannels=[727212369117446252])
async def test(msg, *args):
    """Test"""
    print("ahoj", args)


@client.command("test2")
async def test1(msg, *args):
    print("ahoj2")
    raise ValueError("Test")


@client.logMessage
def loging(msg):
    log.info(msg.content)


@client.logCommand
def loging(*args):
    log.info(args)


@client.event
async def on_ready():
    print("Ready")


@client.event
async def on_message(msg):
    # print(msg.content)
    if msg.content == "0":
        return {"log": False}

client.reactionRole(775405122137489458, "TheBot", 700424827839971499)


@client.command("t")
async def test_command(msg, args):
    await msg.reply(
        embed=client.embed(
            "Ahoj",
            fields=[
                (
                    "ahoj",
                    "nice"
                ),
                (
                    "nice",
                    "ahoj",
                    True
                )
            ]
        )
    )


@client.command("slashTest2")
@slash.slash(name="slashTest2", guild_ids=[thebotas])
async def command_slashTest(*args):
    print(args)

client.run("")
