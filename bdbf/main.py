import discord
import datetime
import re
import bdbf.options

last10messages: dict = {}

def IntToRgb(RGBint: int) -> (int,int,int):
    blue =  RGBint & 255
    green = (RGBint >> 8) & 255
    red =   (RGBint >> 16) & 255
    return red, green, blue

def RgbToInt(rgb: (int,int,int)) -> int:
    red = rgb[0]
    green = rgb[1]
    blue = rgb[2]
    RGBint = (red<<16) + (green<<8) + blue
    return RGBint

def hasLink(text: str) -> bool:
        regex = re.compile(
            "(([\w]+:)?//)?(([\d\w]|%[a-fA-f\d]{2,2})+(:([\d\w]|%[a-fA-f\d]{2,2})+)?@)?([\d\w][-\d\w]{0,253}[\d\w]\.)+[\w]{2,63}(:[\d]+)?(/([-+_~.\d\w]|%[a-fA-f\d]{2,2})*)*(\?(&?([-+_~.\d\w]|%[a-fA-f\d]{2,2})=?)*)?(#([-+_~.\d\w]|%[a-fA-f\d]{2,2})*)?"
        )
        if regex.match(text):
            return True
        else:
            return False

def embed(title, url = None, description = None, fields = None, image = None, thumbnail = None, author =  None) -> discord.Embed:
    e = discord.Embed.from_dict({
            "title": title,
            "color": RgbToInt(bdbf.options.embedColor),
            "description": description,
            "image": image,
            "thumbnail": thumbnail,
            "author": author,
            "fields": fields,
            "url": url,
            "footer": bdbf.options.embedFooter
            }
        )
    return e

async def spamProtection(message: discord.Message, spamValue: int, spamWarnMsg: str = None, spamDelWarnMsg: str = None, spamDelValue: int = -1):
    if message.channel not in last10messages:
        last10messages[message.channel] = []
    if not message.author.bot and message.content[0] != commandPrefix:
        last10messages[message.channel].append({"author": message.author, "time": message.created_at, "content": message.content})
    if len(last10messages[message.channel]) > (spamValue + max(0,spamDelValue) + 1):
        del last10messages[message.channel][0]
    a = 0
    #print(len(last10messages[message.channel]), last10messages)
    for msg in last10messages[message.channel]:
        if msg["author"] == message.author:
            a += 1
        else:
            break
    try:
        if ((a >= spamValue and message.created_at - last10messages[message.channel][-2]["time"] < datetime.timedelta(seconds = 60)) or last10messages[message.channel][-2]["content"] == message.content) and a < (spamValue+max(0,spamDelValue)):
            await message.channel.send(spamWarnMsg)
        elif a == (spamValue+max(0, spamDelValue)):
            await message,channel.send(spamDelWarnMsg)
        elif a > (spamValue+max(0, spamDelValue)):
            await message.delete()
    except:
        pass