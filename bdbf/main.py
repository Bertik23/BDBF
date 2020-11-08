import discord
from bdbf.exceptions import *
from bdbf.functions import *
import typing

class Client(discord.Client):
    r"""Represents a client connection that connects to Discord.
    This class is used to interact with the Discord WebSocket and API.

    A number of options can be passed to the :class:`Client`.

    Parameters
    -----------
    embedFooter: Optional[:class:`dict`]
        The footer of embeds.

    embedColor: Optional[:class:`tuple[int,int,int]`]
        The color of embeds.

    botName: Optional[:class:`str`]
        The name of the bot.

    commandPrefix: Optional[:class:`str`]
        The prefix of all commands.

    useDefaultHelp: Optional[:class:`bool`]
        Whether to use the default help.

    isHelpInline: Optional[:class:`bool`]
        If using the default help. Wheter it is inline or not.

    max_messages: Optional[:class:`int`]
        The maximum number of messages to store in the internal message cache.
        This defaults to ``1000``. Passing in ``None`` disables the message cache.

        .. versionchanged:: 1.3
            Allow disabling the message cache and change the default size to ``1000``.
    loop: Optional[:class:`asyncio.AbstractEventLoop`]
        The :class:`asyncio.AbstractEventLoop` to use for asynchronous operations.
        Defaults to ``None``, in which case the default event loop is used via
        :func:`asyncio.get_event_loop()`.
    connector: :class:`aiohttp.BaseConnector`
        The connector to use for connection pooling.
    proxy: Optional[:class:`str`]
        Proxy URL.
    proxy_auth: Optional[:class:`aiohttp.BasicAuth`]
        An object that represents proxy HTTP Basic Authorization.
    shard_id: Optional[:class:`int`]
        Integer starting at ``0`` and less than :attr:`.shard_count`.
    shard_count: Optional[:class:`int`]
        The total number of shards.
    fetch_offline_members: :class:`bool`
        Indicates if :func:`.on_ready` should be delayed to fetch all offline
        members from the guilds the client belongs to. If this is ``False``\, then
        no offline members are received and :meth:`request_offline_members`
        must be used to fetch the offline members of the guild.
    status: Optional[:class:`.Status`]
        A status to start your presence with upon logging on to Discord.
    activity: Optional[:class:`.BaseActivity`]
        An activity to start your presence with upon logging on to Discord.
    allowed_mentions: Optional[:class:`AllowedMentions`]
        Control how the client handles mentions by default on every message sent.

        .. versionadded:: 1.4
    heartbeat_timeout: :class:`float`
        The maximum numbers of seconds before timing out and restarting the
        WebSocket in the case of not receiving a HEARTBEAT_ACK. Useful if
        processing the initial packets take too long to the point of disconnecting
        you. The default timeout is 60 seconds.
    guild_ready_timeout: :class:`float`
        The maximum number of seconds to wait for the GUILD_CREATE stream to end before
        preparing the member cache and firing READY. The default timeout is 2 seconds.

        .. versionadded:: 1.4
    guild_subscriptions: :class:`bool`
        Whether to dispatch presence or typing events. Defaults to ``True``.

        .. versionadded:: 1.3

        .. warning::

            If this is set to ``False`` then the following features will be disabled:

                - No user related updates (:func:`on_user_update` will not dispatch)
                - All member related events will be disabled.
                    - :func:`on_member_update`
                    - :func:`on_member_join`
                    - :func:`on_member_remove`

                - Typing events will be disabled (:func:`on_typing`).
                - If ``fetch_offline_members`` is set to ``False`` then the user cache will not exist.
                  This makes it difficult or impossible to do many things, for example:

                    - Computing permissions
                    - Querying members in a voice channel via :attr:`VoiceChannel.members` will be empty.
                    - Most forms of receiving :class:`Member` will be
                      receiving :class:`User` instead, except for message events.
                    - :attr:`Guild.owner` will usually resolve to ``None``.
                    - :meth:`Guild.get_member` will usually be unavailable.
                    - Anything that involves using :class:`Member`.
                    - :attr:`users` will not be as populated.
                    - etc.

            In short, this makes it so the only member you can reliably query is the
            message author. Useful for bots that do not require any state.
    assume_unsync_clock: :class:`bool`
        Whether to assume the system clock is unsynced. This applies to the ratelimit handling
        code. If this is set to ``True``, the default, then the library uses the time to reset
        a rate limit bucket given by Discord. If this is ``False`` then your system clock is
        used to calculate how long to sleep for. If this is set to ``False`` it is recommended to
        sync your system clock to Google's NTP server.

        .. versionadded:: 1.3

    Attributes
    -----------
    ws
        The websocket gateway the client is currently connected to. Could be ``None``.
    loop: :class:`asyncio.AbstractEventLoop`
        The event loop that the client uses for HTTP requests and websocket operations.
    """
    def __init__(self, *, loop=None, **options):
        super().__init__(loop=loop, **options)
        self.commands = {}
        self.embedFooter = options.pop("embedFooter", {})
        self.embedColor = options.pop("embedColor", (0,0,0))
        self.botName = options.pop("botName", None)
        self.commandPrefix = options.pop("commandPrefix", None)
        if options.pop("useDefaultHelp", True):
            @self.command("help")
            async def help(msg):
                """Help"""
                fields = [(command, self.commands[command].__doc__, options.pop("isHelpInline", True)) for command in self.commands.keys()]
                e = self.embed(f"Help for {self.botName}", fields=fields)
                await msg.channel.send(embed=e)
    
    def command(self, name, **options):
        r"""Wrapper fuction for making commands.
        Like ::

            @client.command("command")
            def command(message):
                print(message.content)"""
        def register(function):
            if name in self.commands.keys():
                raise CommandNameAlreadyRegistered(f"The command name {name} is already registered and can't be used again.")
            self.commands[name] = function

            return function
        return register

    async def tryCommand(self, msg, command, *options):
        try:
            if None not in options:
                await self.commands[command](msg, *options)
            else:
                await self.commands[command](msg)
        except KeyError:
            pass

    async def useCommand(self, msg):
        message = msg.content
        if len(message) != 0:
            if message[:len(self.commandPrefix)] == self.commandPrefix:
                if len(message[len(self.commandPrefix):].split(" ", 1)) == 1:
                    cmd, args = message[len(self.commandPrefix):], None
                else:
                    cmd, args = message[len(self.commandPrefix):].split(" ", 1)[0], message[1:].split(" ",1)[1]
            else:
                cmd, args = None, None
        else:
            cmd, args = None, None

        await self.tryCommand(msg, cmd, args)

    def event(self, coro):
        """A decorator that registers an event to listen to.

        You can find more info about the events on the :ref:`documentation below <discord-api-events>`.

        The events must be a :ref:`coroutine <coroutine>`, if not, :exc:`TypeError` is raised.

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
        if coro.__name__ == "on_message" and "on_message" not in vars(self):
            async def on_message(msg, **options):
                await self.useCommand(msg)
                return await coro(msg, **options)
            return super().event(on_message)


        return super().event(coro)

    def embed(self, title, **options):
        """Returns discord embed from given parameters with automatic footer and color options.

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
            
        :returns: discord.Embed"""
        return embed(title,footer=self.embedFooter, color=self.embedColor, **options)
