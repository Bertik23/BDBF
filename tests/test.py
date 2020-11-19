import bdbf
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

client = bdbf.Client(commandPrefix="%", logging=True, caseSensitiveCommands=False)

print(bdbf.__version__)

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

@client.event
async def on_ready():
    print("Ready")

@client.event
async def on_message(msg):
    print(msg.content)
    if msg.content == "0":
        return {"log": False}

client.reactionRole(775405122137489458,"TheBot",700424827839971499)

client.embed("Ahoj",fields=[("ahoj","nice"),("nice","ahoj",True)])

client.run("NzMzOTg1MTk4NzgxNDk3NDA0.XxLG_A.azOtS2l_HF__lHkauJEvdY_E_Uk")
