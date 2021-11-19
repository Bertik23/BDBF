import bdbf
import logging

logging.basicConfig(level=logging.FATAL)
log = logging.getLogger(__name__)

client = bdbf.Client(
    commandPrefix="%",
    logging=True,
    caseSensitiveCommands=False)

print(bdbf.__version__)


@client.command("test")
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


@client.command(
    "longHelp",
    longHelp=[
        ("Title1", "This is a long help"),
        ("Title2", "This is a second subhelp")
    ]
)
async def longHelp_command(msg, *args):
    await msg.reply("long help test")


client.run("")
