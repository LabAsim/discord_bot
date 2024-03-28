import logging
from typing import List
import asyncio
import random
import logging
from typing import List

import colorama
import discord
from discord import Message
from discord.ext import commands


logger = logging.getLogger(__name__)
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# https://github.com/Rapptz/discord.py/blob/v2.3.2/examples/basic_bot.py
description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='?', description=description, intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)


@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)


@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))


@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)


@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')


@bot.group()
async def cool(ctx):
    """Says if a user is cool.

    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await ctx.send(f'No, {ctx.subcommand_passed} is not cool')


@cool.command()  # name='bot')
async def _bot(ctx):
    """Is the bot cool?"""
    await ctx.send('Yes, the bot is cool.')


@bot.command()
async def edit(message):
    msg = await message.channel.send('10')
    await asyncio.sleep(1.0)
    await msg.edit(content='40')


async def on_message_edit(before, after):
    msg = f'**{before.author}** edited their message:\n{before.content} -> {after.content}'
    await before.channel.send(msg)


@bot.command()
async def edit_pin(ctx: discord.ext.commands.Context):
    """
    Note that only the user can edit their message, no one else, including a bot.
    See: https://stackoverflow.com/a/77166679
    """

    pins: List[Message] = await ctx.channel.pins()  # a list of all the channel's pins
    logger.debug(f"{pins=}")
    # await ctx.send(pins)  # sends all the information in the channel's first pin
    logger.debug(f"{pins[0]=}")
    logger.debug(f"{pins[0].content=}")
    # await ctx.send(pins[0].content)  # sends the content of the message.
    logger.debug(f"{pins[0].id}")
    # msg = await discord.Message()
    msg = await ctx.fetch_message(int(pins[0].id))
    logger.debug(f"{msg=}")
    msg = await msg.edit(content=msg.content + " test")
    logger.debug(f"{msg=}")
    # An error will occur if there is no message content

