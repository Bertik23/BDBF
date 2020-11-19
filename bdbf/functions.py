"""Functions Docstring"""

import discord
import datetime
import re
import typing

last10messages: dict = {}

def IntToRgb(RGBint: int):# -> typing.Tuple[int,int,int]:
    """Converts a integer color value to a RGB tuple

    :param RGBint: :class:`int`
        The integer color value.

    :returns: :class:`tuple[int,int,int]`
        RGB tuple
    """
    blue =  RGBint & 255
    green = (RGBint >> 8) & 255
    red =   (RGBint >> 16) & 255
    return red, green, blue

def RgbToInt(rgb: typing.Tuple[int,int,int]):# -> int:
    """Converts a RGB tuple to a integer color value

    :param rgb: :class:`tuple[int,int,int]`
        RGB tuple
    :param no: :class:`tuple[int,int,int]`
        RGB tuple

    :returns: :class:`int`
        The integer color value.
    """
    red = rgb[0]
    green = rgb[1]
    blue = rgb[2]
    RGBint = (red<<16) + (green<<8) + blue
    return RGBint

def hasLink(text: str):# -> bool:
    """Returns if a string contains a link.

    :param text: :class:`str`
        String to check
    
    :returns: :class:`bool`
        If the string has a link.
    """
    regex = re.compile(
        "(([\w]+:)?//)?(([\d\w]|%[a-fA-f\d]{2,2})+(:([\d\w]|%[a-fA-f\d]{2,2})+)?@)?([\d\w][-\d\w]{0,253}[\d\w]\.)+[\w]{2,63}(:[\d]+)?(/([-+_~.\d\w]|%[a-fA-f\d]{2,2})*)*(\?(&?([-+_~.\d\w]|%[a-fA-f\d]{2,2})=?)*)?(#([-+_~.\d\w]|%[a-fA-f\d]{2,2})*)?"
    )
    if regex.match(text):
        return True
    else:
        return False

def embed(title, url = None, description = None, fields = None, image = None, thumbnail = None, author =  None, footer=None, color: typing.Union[typing.Tuple[int,int,int], int] = 0):# -> discord.Embed:
    """Returns discord embed from given parameters
    
    :param title: :class:`str`
        Title of the embed
    :param url: :class:`Optional[str]`
        url of the title
    :param description: :class:`Optional[str]`
        Description of the embed
    :param fields: :class:`Optional[List[Tuple[str,str,Optional[bool]]]]`
        Fields of the embed.
        A tuple with item 1 being the name of the field, item 2 the value and item 3 weather is inline or not, item 3 is optional
    :param image: :class:`Optional[str]`
        Url of the embed image
    :param thumbnail: :class:`Optional[str]`
        Url of the thumbnail image
    :param author: :class:`Optional[Dict[str,str]]`
        Author of the embed
    :param footer: :class:`Optional[Dict[str,str]]`
        Footer of the embed
    :param color: :class:`Optional[Union[Tuple[int,int,int],int]]`
        Color of the embed, eighter RGB tuple or int
        
    :returns: discord.Embed"""
    if type(color) == tuple:
        color = RgbToInt(color)

    if fields == None:
        fields = []

    fieldKeys = []
    for i,f in enumerate(fields):
        if len(f) == 2:
            fieldKeys.append(("name","value"))
        elif len(f) == 3:
            fieldKeys.append(("name","value","inline"))

    #print(fieldKeys, fields, [list(i) for i in [zip(j,fields[k]) for k,j in enumerate(fieldKeys)]])
    fields = [dict(l) for l in [list(i) for i in [zip(j,fields[k]) for k,j in enumerate(fieldKeys)]]]
    #print(fields)

    e = discord.Embed.from_dict({
            "title": title,
            "color": color,
            "description": description,
            "image": image,
            "thumbnail": thumbnail,
            "author": author,
            "fields": fields,
            "url": url,
            "footer": footer
            }
        )
    return e
