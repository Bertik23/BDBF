import discord
import datetime

commandPrefix : str = None
embedFooter: dict = {}

def embed(title, url = None, description = None, fields = None, image = None, thumbnail = None, author =  None) -> discord.Embed:
    e = discord.Embed.from_dict({
            "title": title,
            "color": 2480439,
            "description": description,
            "image": image,
            "thumbnail": thumbnail,
            "author": author,
            "fields": fields,
            "url": url,
            "footer": embedFooter
            }
        )
    return e

def command(message) -> (str, str):
    if len(message) != 0:
        if message[0] == commandPrefix:
            if len(message[1:].split(" ", 1)) == 1:
                return message[1:], None
            else:
                return message[1:].split(" ", 1)[0], message[1:].split(" ",1)[1]
        else:
            return None, None
    else:
        return None, None

async def spamProtection(message: discord.Message, spamWarnMsg: str, spamValue: int):
    last10messages: dict = {}
    if message.channel not in last10messages:
        last10messages[message.channel] = []
    if not message.author.bot and message.content[0] != commandPrefix:
        last10messages[message.channel].append({"author": message.author, "time": message.created_at, "content": message.content})
    if len(last10messages[message.channel]) > spamValue:
        del last10messages[message.channel][0]
    a = 0
    print(len(last10messages[message.channel]), last10messages)
    for msg in last10messages[message.channel]:
        for i in msg:
            print(msg[i])
        if msg["author"] == message.author:
            a += 1
        else:
            break
    try:
        if (a >= spamValue and message.created_at - last10messages[message.channel][-2]["time"] < datetime.timedelta(seconds = 60)) or last10messages[message.channel][-2]["content"] == message.content:
            await message.channel.send(f"{message.author.mention} nespamuj!")
    except:
        pass