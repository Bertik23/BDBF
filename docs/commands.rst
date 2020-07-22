Commands
========
This part is all about the commands submodule.

Classes
^^^^^^^

Command
"""""""
The command class used to make other commands

``__init__(description, usage)``
********************************
Sets variables, that will be used by the premade help command.

| *description*: str - the description of the command
| *usage*: str - the usage of the command, use %commandPrefix% to indicate the commandPrefix

``command(args)``
*****************
Command placeholder function, will be executed if someone runs the command

| async function
| **Returns**: str|None, discord.Embed|None - the text of send the message and the embed of the send message, if None nothing is send

help
""""
Premade help command

``command(args)``
*****************
| async function
| **Returns**: None, discord.Embed - embed of the help command

Functions
^^^^^^^^^

``checkForCommands(msg)``
"""""""""""""""""""""""""
Checks if the message is a command and executes it.

msg: discord.Message - the message you want to check for

Variables
^^^^^^^^^

``commandPrefix``
"""""""""""""""""
the prefix, that indicates a command

str

``cmds``
""""""""
| dict
| {
|	"all": list, - commands for all guilds
|	[int: list]  - commands only for the guild id
| }