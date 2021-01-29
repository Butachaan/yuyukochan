import textwrap
from discord import Intents
import typing
import aiohttp
from datetime import datetime, timedelta
from typing import Optional
from typing import Union
import time
import platform
from discord.ext import commands
from platform import python_version
from discord import __version__ as discord_version
from asyncio import sleep
import json
from discord.utils import get
import os
import logging
import asyncio, discord
import random
import secrets
from io import BytesIO
import ast

import functools
import inspect
from discord.ext.commands import clean_content
from discord import Embed
from discord.ext.commands import Cog
import sys


class fun(commands.Cog, name="Fun"):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["ps"], description="password")
    async def password(self, ctx, nbytes: int = 18):
        """ Generates a random password string for you
        This returns a random URL-safe text string, containing nbytes random bytes.
        The text is Base64 encoded, so on average each byte results in approximately 1.3 characters.
        """
        if nbytes not in range(3, 1401):
            return await ctx.send("I only accept any numbers between 3-1400")
        if hasattr(ctx, 'guild') and ctx.guild is not None:
            await ctx.send(f"Sending you a private message with your random generated password **{ctx.author.name}**")
        await ctx.author.send(f"🎁 **Here is your password:**\n{secrets.token_urlsafe(nbytes)}")

    @commands.command(aliases=["sl"], description="スロット")
    async def slot(self, ctx):
        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)

        slotmachine = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"

        if (a == b == c):
            await ctx.send(f"{slotmachine} All matching, you won! 🎉")
        elif (a == b) or (a == c) or (b == c):
            await ctx.send(f"{slotmachine} 2 in a row, you won! 🎉")
        else:
            await ctx.send(f"{slotmachine} No match, you lost 😢")


def setup(bot):
    bot.add_cog(fun(bot))