
import asyncio
import random
import logging
from typing import List

import discord
import requests
from discord import Message
from discord.ext import commands, tasks
from constants import CHANNEL_IDS

logger = logging.getLogger(__name__)
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# https://github.com/Rapptz/discord.py/blob/v2.3.2/examples/basic_bot.py
description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='?', description=description, intents=intents, help_command=None)

RESOURCES_MD_LINK = "https://raw.githubusercontent.com/LabAsim/discord_bot/master/resources.md"


@bot.event
async def on_ready() -> None:
    """The function which is called upon startup. Do not change the name!"""
    logger.info(f'Logged in as {bot.user} (ID: {bot.user.id})')
    # logger.info('------'*10)
    # Start polling
    check_file.start()

    text_channel_list = []
    for guild in bot.guilds:
        for channel in guild.text_channels:
            text_channel_list.append(channel)
    logger.info(f"{text_channel_list=}")


@tasks.loop(seconds=60)
async def check_file() -> None:
    """
    Checks if the file is updated on GitHub
    See: https://discordpy.readthedocs.io/en/stable/ext/tasks/index.html
    """
    logger.info(f"Checking Github..")
    for _id in CHANNEL_IDS:
        channel = bot.get_channel(_id)
        await check_if_pinned(channel=channel)


async def check_if_pinned(channel: discord.abc.Messageable) -> None:
    """Checks if there is a pinned message on the server"""
    pins: List[Message] = await channel.pins()
    # If there is no pinned message in this channel
    if len(pins) == 0:
        logger.debug("No pinned messages")
        resource_md = requests.get(url=RESOURCES_MD_LINK)
        text = resource_md.text
        msg = await channel.send(content=text)
        await msg.pin()
        logger.debug(f"Message pinned")
    else:
        await edit_pinned_message(channel=channel)


async def edit_pinned_message(channel: discord.abc.Messageable) -> None:
    """
     Edits the pinned message of channel passed as an argument.
     It compares the msg against the md file on GitHub
     """
    pins: List[Message] = await channel.pins()  # a list of all the channel's pins
    logger.debug(f"{pins=}")
    # await ctx.send(pins)  # sends all the information in the channel's first pin
    logger.debug(f"{pins[-1]=}")
    logger.debug(f"{pins[-1].content=}")
    # await ctx.send(pins[0].content)  # sends the content of the message.
    logger.debug(f"{pins[-1].id=}")
    # msg = await discord.Message()
    msg = await channel.fetch_message(int(pins[-1].id))
    logger.debug(f"{msg=}")

    resource_md = requests.get(url=RESOURCES_MD_LINK)
    text = resource_md.text
    logger.debug(f"{text=}")
    if text != msg.content:
        try:
            msg = await msg.edit(content=text)
            logger.debug(f"new {msg=}")
            logger.info("File updated!")
        except discord.errors.Forbidden as err:
            logger.exception(err)

    else:
        logger.info(f"File is up-to-date")


@bot.command()
async def edit_pin(ctx: discord.ext.commands.Context) -> None:
    """
    Note that only the user can edit their message, no one else, including a bot.
    See: https://stackoverflow.com/a/77166679
    """
    current_channel = ctx.channel
    current_channel_name = ctx.channel.name
    if current_channel_name != "resources":
        logger.debug(f"Not a resources channel")
        return None
    await edit_pinned_message(current_channel)


@bot.command()
async def add(ctx, left: int, right: int) -> None:
    """Adds two numbers together."""
    await ctx.send(left + right)


@bot.command()
async def roll(ctx, dice: str) -> None:
    """Rolls a die in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)


@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str) -> None:
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))


@bot.command()
async def repeat(ctx, times: int, content='repeating...') -> None:
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)


@bot.command()
async def joined(ctx, member: discord.Member) -> None:
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')


@bot.group()
async def cool(ctx) -> None:
    """Says if a user is cool.

    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await ctx.send(f'No, {ctx.subcommand_passed} is not cool')


@cool.command(name='bot')
async def _bot(ctx) -> None:
    """Is the bot cool?"""
    await ctx.send('Yes, the bot is cool.')


@bot.command()
async def edit(message) -> None:
    msg = await message.channel.send('10')
    await asyncio.sleep(1.0)
    await msg.edit(content='40')


async def on_message_edit(before, after) -> None:
    msg = f'**{before.author}** edited their message:\n{before.content} -> {after.content}'
    await before.channel.send(msg)
