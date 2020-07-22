Basic
=====

Here are explained the basic functions and variables you need to know.

Functions
^^^^^^^^^

``IntToRgb(RGBint)``
""""""""""""""""""""
*RGBint*: int - the int value of an RGB color

**Returns**: (int,int,int) - tuple of RGB colors

``RgbToInt(rgb)``
"""""""""""""""""
*rgb*: (int,int,int) - the RBG tuple of a color

**Returns**: int - the int value of a RGB color

``hasLing(text)``
"""""""""""""""""
If the provided text has links in it.

*text*: str - the text you want to check for

**Returns**: bool - if the text has a link in it

``embed(title,[url],[description], [fields], [image], [thumbnail], [author])``
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
| *title*: str - Title of the embed
| *url*: str - url of the embed
| *description*: str - the text of the embed
| *fields*: dict - {
|					"name": str, - the title of the field
|					"value": str, - the text of the field
|					"inline": bool - if it is inline or not
|				 } - the fields of the embed
| *image*: dict - {"url": str} - the image of the embed
| *thumbnail*: dict - {"url": str} - a smaller image
| *author*: dict - {
|					"name": str, - name of the author
|					"url": str - link to his profile
|				 }

**Returns**: discord.Embed

``spamProtection(message, spamValue, [spamWarnMsg], [spamDelWarnMsg], [spamDelValue])``
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
| *message*: discord.Message - the message you want to check spam for
| *spamValue*: int - how many messages are considered spa
| *spamWarnMsg*: str - the message you want to send as a warning not to spam
| *spamDelWarnMsg*: str - the message you want to send as a warning that all other messages will be deleted
| *spamDelValue*: int - the number of the last message, that will not be deleted, to not delete any use ``-1``, which is the default

Variables
^^^^^^^^^

``embedFooter``
"""""""""""""""
The footer of every embed created by the ``embed`` function

| dict
| {
| 	"icon_url": str, - the url of the icon in the footer
|	"text": str - the text of the footer
| }

``embedColor``
""""""""""""""
The color of all embeds created by the ``embed`` function in RGB

| (
|	int, - red
|	int, - green
|	int  - blue
| )

``botName``
"""""""""""
The name of the bot

str