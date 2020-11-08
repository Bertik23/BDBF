import bdbf

client = bdbf.Client(commandPrefix="%")

@client.command("test")
async def test(msg):
    """Test"""
    print("ahoj")

@client.command("test2")
async def test(msg):
    """Test 2"""
    print("ahoj2")


@client.event
async def on_message(msg):
    print(msg.content)

client.embed("Ahoj",fields=[("ahoj","nice"),("nice","ahoj",True)])

client.run("NzMzOTg1MTk4NzgxNDk3NDA0.XxLG_A.ZRH2bEW0MgdqOJOB6UyxzQSfEz8")
