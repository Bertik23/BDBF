import discord
from bdbf.exceptions import *
from bdbf.functions import *
import asyncio
import logging
import traceback
import time
from discord_slash import SlashCommand

log = logging.getLogger(__name__)


class Client(discord.Client):
    r"""Discord client class inherited from discord.Client.
    This documentation covers only the changes. For the inherited
    functions please head to the `discord.py documentation
    <https://discordpy.readthedocs.io/en/latest/api.html#discord.Client>`_

    :param embedFooter: Optional[:class:`dict`]
        The footer of embeds.

    :param embedColor: Optional[:class:`tuple[int,int,int]`]
        The color of embeds.

    :param botName: Optional[:class:`str`]
        The name of the bot.

    :param commandPrefix: Optional[:class:`str`]
        The prefix of all commands.

    :param useDefaultHelp: Optional[:class:`bool`]
        Whether to use the default help.
        Default: True

    :param isHelpInline: Optional[:class:`bool`]
        If using the default help. Wheter it is inline or not.
        Default: True

    :param logging: Optional[:class:`bool`]
        If message logging is enabled.
        Default: False

    :param caseSensitiveCommands: Optional[:class:`bool`]
        If commands are case sensitive.
        Default: True

    :param sendExceptions: Optional[:class:`bool`]
        If sending exceptions to discord is enabled.
        Default: True
    """

    def __init__(self, *, loop=None, **options):
        super().__init__(loop=loop, **options)
        self.commands = {}
        self.embedFooter = options.pop("embedFooter", {})
        self.embedColor = options.pop("embedColor", (0, 0, 0))
        self.botName = options.pop("botName", None)
        self.commandPrefix = options.pop("commandPrefix", None)
        self.logging = options.pop("logging", False)
        self.loggingFunction = None
        self.commandLoggingFunction = None
        self.caseSensitiveCommands = options.pop("caseSensitiveCommands", True)
        self.sendExceptions = options.pop("sendExceptions", True)
        self.createTaskCommands = options.pop("createTaskCommands", False)
        self.slash = SlashCommand(self)

        self.roleToReaction = {}

        if options.pop("useDefaultHelp", True):
            @self.command("help")
            async def help(msg, *args):
                """Help"""
                fields = [
                    (
                        command,
                        self.commands[command].__doc__
                        if self.commands[command].__doc__ is not None
                        else f"{command} help",
                        options.pop("isHelpInline", True)
                    ) for command in self.commands.keys()
                ]
                e = self.embed(f"Help for {self.botName}", fields=fields)
                await msg.channel.send(embed=e)

        @self.event
        async def on_raw_reaction_add(payload):
            pass

        @self.event
        async def on_raw_reaction_remove(payload):
            pass

    def command(self, commandName, **options):
        r"""Wrapper fuction for making commands.

        :param worksOnlyInGuilds: Optional[:class:`List[int]`]
            List of guild where the command will work. List of guild where the
            command will work.

        :param worksOnlyInChannels: Optional[:class:`List[int]`]
            List of channels where the command will work. If not provided will
            for in all.

        :param doesntWorkInGuilds: Optional[:class:`List[int]`]
            List of guilds where the command wont work. List of guild where
            the command will work.

        :param doesntWorkInChannels: Optional[:class:`List[int]`]
            List of guilds where the command wont work. List of guild where
            the command will work.

        Example
        -------

            @client.command("command")
            def command(message):
                print(message.content)"""
        def register(function):
            try:
                fName = function.__name__
            except AttributeError:
                fName = "No function name found"
            # function = self.slash.slash(name=commandName)(function)
            if function.__doc__ is not None:
                function.__doc__ = function.__doc__.replace(
                    "%commandPrefix%", self.commandPrefix)
            for option in options:
                setattr(function, option, options[option])
            if not self.caseSensitiveCommands:
                name = commandName.lower()
            else:
                name = commandName
            if name in self.commands.keys():
                raise CommandNameAlreadyRegistered(
                    f"The command name {name} is already"
                    "registered and can't be used again."
                )
            self.commands[name] = function
            log.debug(
                f"Function {fName}"
                f"has been registered for command {name}"
            )
            return function
        return register

    async def tryCommand(self, msg, command, *options):
        startTime = time.time()
        state = "Succeded"
        e = ""
        try:
            if command in self.commands.keys():
                if hasattr(self.commands[command], "worksOnlyInGuilds"):
                    if msg.channel.guild.id in self.commands[
                            command].worksOnlyInGuilds:
                        await self.commands[command](msg, *options)
                elif hasattr(self.commands[command], "worksOnlyInChannels"):
                    if msg.channel.id in self.commands[
                            command].worksOnlyInChannels:
                        await self.commands[command](msg, *options)
                elif hasattr(self.commands[command], "doesntWorkInGuilds"):
                    if msg.channel.guild.id not in self.commands[
                            command].doesntWorkInGuilds:
                        await self.commands[command](msg, *options)
                elif hasattr(self.commands[command], "doesntWorkInChannels"):
                    if msg.channel.id not in self.commands[
                            command].doesntWorkInChannels:
                        await self.commands[command](msg, *options)
                else:
                    await self.commands[command](msg, *options)
            else:
                state = "Failed"
                e = "Command not existent"
        except Exception:
            state = "Failed"
            e = traceback.format_exc()
            if self.sendExceptions:
                await msg.channel.send(f"```{e}```"[:2000])
        if (
            self.logging
            and command is not None
            and self.commandLoggingFunction is not None
        ):
            if asyncio.iscoroutinefunction(self.commandLoggingFunction):
                await self.commandLoggingFunction(msg)
            else:
                self.commandLoggingFunction(
                    command, msg, time.time()-startTime, e)

    async def useCommand(self, msg):
        message = msg.content
        if len(message) != 0:
            if message[:len(self.commandPrefix)] == self.commandPrefix:
                if len(message[len(self.commandPrefix):].split(" ", 1)) == 1:
                    cmd, args = message[len(self.commandPrefix):], None
                else:
                    cmd, args = message[
                        len(self.commandPrefix):
                    ].split(" ", 1)[
                        0
                    ], message[1:].split(" ", 1)[1]
            else:
                cmd, args = None, None
        else:
            cmd, args = None, None

        if not self.caseSensitiveCommands and cmd is not None:
            cmd = cmd.lower()

        if not self.createTaskCommands:
            await self.tryCommand(msg, cmd, args)
        else:
            await self.loop.create_task(self.tryCommand(msg, cmd, args))

    def event(self, coro):
        r"""A decorator that registers an event to listen to.

        You can find more info about the events on the :ref:`documentation
        below <discord-api-events>`.

        The events must be a :ref:`coroutine <coroutine>`, if not,
        :exc:`TypeError` is raised.

        Example
        ---------

        .. code-block:: python3

            @client.event
            async def on_ready():
                print('Ready!')

        Raises
        --------
        TypeError
            The coroutine passed is not actually a coroutine.
        """
        if coro.__name__ == "on_message":
            async def on_message(msg, **options):
                a = await coro(msg, **options)
                if a is None:
                    a = {}
                if a.pop("command", True):
                    await self.useCommand(msg)
                if a.pop("log", True) and self.logging:
                    if self.loggingFunction is not None:
                        if asyncio.iscoroutinefunction(self.loggingFunction):
                            await self.loggingFunction(msg)
                        else:
                            self.loggingFunction(msg)
                return a
            return super().event(on_message)

        elif coro.__name__ == "on_raw_reaction_add":
            async def on_raw_reaction_add(payload):
                a = await coro(payload)
                await self.tryReactionRole("add", payload)
                return a
            return super().event(on_raw_reaction_add)

        elif coro.__name__ == "on_raw_reaction_remove":
            async def on_raw_reaction_remove(payload):
                a = await coro(payload)
                await self.tryReactionRole("remove", payload)
                return a
            return super().event(on_raw_reaction_remove)

        return super().event(coro)

    async def tryReactionRole(self, a, payload):
        if a == "add":
            try:
                await payload.member.add_roles(
                    discord.Object(
                        self.roleToReaction[
                            payload.message_id
                        ][
                            payload.emoji.name
                        ]
                    )
                )
            except KeyError:
                pass
        elif a == "remove":
            try:
                await self.get_guild(
                    payload.guild_id
                ).get_member(
                    payload.user_id
                ).remove_roles(
                    discord.Object(
                        self.roleToReaction[
                            payload.message_id
                        ][
                            payload.emoji.name
                        ]
                    )
                )
            except KeyError:
                pass

    def logMessage(self, function):
        r"""Wrapper fuction for making a logging function.
        Like ::

            @client.logMessage
            def log(message):
                print(message.content)"""

        self.loggingFunction = function
        log.debug(
            f"Function {function.__name__} has been "
            "registered as message logging function."
        )
        return function

    def logCommand(self, function):
        r"""Wrapper fuction for making a logging function.
        Like ::

            @client.logCommand
            def log(command, message, time, state, exception):
                print(message.content)"""

        self.commandLoggingFunction = function
        log.debug(
            f"Function {function.__name__} has been "
            "registered as command logging function."
        )
        return function

    def reactionRole(self, msg, emoji, role):
        r"""Function to add reaction role functions to a message.

        :param msg: :class:`Union[discord.Message,int]`
            Message or message id of the message you want to add
            the reaction role functionality.
        :param emoji: :class:`str`
            Emoji. If a unicode emoji use it, if a custom emoji use it's name.
        :param role: :class:`int`
            Role id of the role you want to add to the emoji."""
        if type(msg) == discord.Message:
            msg = msg.id
        elif type(msg) != int:
            raise TypeError(
                f"Message has to be eighter "
                f"int or discord.Message not {type(msg)}")

        self.roleToReaction[msg] = {emoji: role}

    def embed(self, title, **options):
        """Returns discord embed from given parameters with automatic
        footer and color options.

        :param title: :class:`str`
            Title of the embed
        :param url: :class:`Optional[str]`
            url of the title
        :param description: :class:`Optional[str]`
            Description of the embed
        :param fields: :class:`Optional[List[Tuple[str,str,Optional[bool]]]]`
            Fields of the embed.
            A tuple with item 1 being the name of the field, item 2 the value
            and item 3 weather is inline or not, item 3 is optional
        :param image: :class:`Optional[str]`
            Url of the embed image
        :param thumbnail: :class:`Optional[str]`
            Url of the thumbnail image
        :param author: :class:`Optional[Dict[str,str]]`
            Author of the embed

        :returns: :class:`discord.Embed`"""
        return embed(
            title,
            footer=self.embedFooter,
            color=self.embedColor,
            **options
        )
