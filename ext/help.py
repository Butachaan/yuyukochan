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

from collections import OrderedDict, deque, Counter
import datetime
import os

import asyncio, discord
import random
import secrets
from io import BytesIO
import ast
import psutil
import functools
import inspect
from discord.ext.commands import clean_content
from discord import Embed
from discord.ext.commands import Cog
import sys
import json
import traceback
import wikipedia
import io
from contextlib import redirect_stdout
import re

import tracemalloc


class help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def helps(self, ctx):
        first_run = True
        while True:
            if first_run:
                page1 = discord.Embed(title='Page 1/7', description='Description1',  color=0x5d00ff)
                page1.add_field(name="**Helpコマンド2**", value="Moderation")
                page1.add_field(name="**Helpコマンド3**", value="Information")
                page1.add_field(name="**Helpコマンド4**", value="Admin")
                page1.add_field(name="**Helpコマンド5**", value="Fun")
                page1.add_field(name="**Helpコマンド6**", value="other")
                page1.add_field(name="**Helpコマンド7**", value="report")
                page1.add_field(name="招待リンク",
                                value="https://discord.com/api/oauth2/authorize?client_id=757807145264611378&permissions=70647361&scope=bot")
                page1.set_thumbnail(
                    url="https://images-ext-2.discordapp.net/external/svQAPh7v9BBNiUgs3Fx4e27C1yhQ1KMp5h1KOhkKH3U/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/757807145264611378/f6e2d7ff1f8092409983a77952670eae.png")

                first_run = False
                msg = await ctx.send(embed=page1)

                reactmoji = ["1️⃣", "2️⃣", "3️⃣", "4⃣", "5⃣", "6⃣", "7⃣"]

                for react in reactmoji:
                    await msg.add_reaction(react)

            def check_react(reaction, user):
                if reaction.message.id != msg.id:
                    return False
                if user != ctx.message.author:
                    return False
                if str(reaction.emoji) not in reactmoji:
                    return False
                return True

            try:
                res, user = await self.bot.wait_for('reaction_add', check=check_react)
            except asyncio.TimeoutError:
                return await msg.clear_reactions()

            if user != ctx.message.author:
                pass
            elif '1️⃣' in str(res.emoji):

                print('<<1️⃣>>')
                await msg.remove_reaction("1️⃣", user)
                await msg.edit(embed=page1)
            elif '2️⃣' in str(res.emoji):
                print('<<2️⃣>>')
                page2 = discord.Embed(title='Page 2/7', description='prefix:[y/]', color=0x5d00ff)
                page2.add_field(name="**userinfo <user>**", value="ユーザーの情報を表示します", inline=False)
                page2.add_field(name="**user <user>**", value="外部ユーザーの情報を表示します", inline=False)
                page2.add_field(name="**serverinfo <server>**", value="サーバーの情報を表示します", inline=False)
                page2.add_field(name="**roleinfo <role>**", value="役職の情報を表示します", inline=False)
                page2.add_field(name="**channelinfo <channel>**", value="チャンネルの情報を表示します", inline=False)
                page2.add_field(name="**messageinfo <message>**", value="メッセージの情報を表示します", inline=False)
                page2.add_field(name="**avatar <user>**", value="ユーザーのアバターの情報を表示します", inline=False)
                page2.set_thumbnail(
                    url="https://images-ext-2.discordapp.net/external/svQAPh7v9BBNiUgs3Fx4e27C1yhQ1KMp5h1KOhkKH3U/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/757807145264611378/f6e2d7ff1f8092409983a77952670eae.png")
                await msg.remove_reaction("2️⃣", user)
                await msg.edit(embed=page2)
            elif '3️⃣' in str(res.emoji):
                print('<<3️⃣>>')
                page3 = discord.Embed(title='Page 3/7', description='prefix:[y/]', color=0x5d00ff)
                page3.add_field(name="**kick <user> <reason>**", value="ユーザーをサーバーからkickします", inline=False)
                page3.add_field(name="**ban <user> <reason>**", value="ユーザーをサーバーからbanします", inline=False)
                page3.add_field(name="**unban <user>**", value="BANされたユーザーをban解除します", inline=False)
                page3.add_field(name="**hackban <user> <reason>**", value="ユーザーをhackbanします", inline=False)
                page3.add_field(name="**baninfo <user>**", value="banされたユーザーのban情報を表示します", inline=False)
                page3.add_field(name="**banlist**", value="banされたユーザー一覧を表示します", inline=False)
                page3.add_field(name="**poll <質問内容>**", value="アンケートを取れます", inline=False)
                page3.set_thumbnail(
                    url="https://images-ext-2.discordapp.net/external/svQAPh7v9BBNiUgs3Fx4e27C1yhQ1KMp5h1KOhkKH3U/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/757807145264611378/f6e2d7ff1f8092409983a77952670eae.png")

                await msg.remove_reaction("3️⃣", user)
                await msg.edit(embed=page3)
            elif '4⃣' in str(res.emoji):
                print('<<4⃣>>')
                page4 = discord.Embed(title='Page 4/7', description='prefix:[y/]', color=0x5d00ff)
                page4.add_field(name="**load/unload/reload <extension名>**", value="ファイルをロード/アンロード/リロードします",
                                inline=False)
                page4.add_field(name="**eval <コード>**", value="コードをevaluate(評価)します")
                page4.add_field(name="**changestatus <status>**", value="幽々子のステータスを変えます")
                page4.add_field(name="**changenick <名前>**", value="ユーザーのニックネームを変えます")
                page4.add_field(name="**set_playing <game名>**", value="幽々子のplaying statuを変えます")
                page4.add_field(name="**announce <内容>**", value="運営がアナウンスをします")
                page4.add_field(name="**dm <user> <内容>**", value="指定したユーザーにDMを送ります")
                page4.add_field(name="**servers**", value="botが入ってるサーバー一覧を表示します")
                page4.add_field(name="**system_shutdown**", value="botを停止します")
                page4.add_field(name="**log <数>**", value="指定された数分のメッセージを保存します")
                page4.set_thumbnail(
                    url="https://images-ext-2.discordapp.net/external/svQAPh7v9BBNiUgs3Fx4e27C1yhQ1KMp5h1KOhkKH3U/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/757807145264611378/f6e2d7ff1f8092409983a77952670eae.png")
                await msg.remove_reaction("4⃣", user)
                await msg.edit(embed=page4)
            elif '5⃣' in str(res.emoji):
                print('<<5⃣>>')
                page5 = discord.Embed(title='Page 5/7', description='prefix:[y/]', color=0x5d00ff)
                page5.add_field(name="**password**", value="DMに暗号文を表示します")
                page5.add_field(name="**slot**", value="スロットをします")
                page5.set_thumbnail(
                    url="https://images-ext-2.discordapp.net/external/svQAPh7v9BBNiUgs3Fx4e27C1yhQ1KMp5h1KOhkKH3U/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/757807145264611378/f6e2d7ff1f8092409983a77952670eae.png")
                await msg.remove_reaction("5⃣", user)
                await msg.edit(embed=page5)
            elif '6⃣' in str(res.emoji):
                print('<<6⃣>>')
                page6 = discord.Embed(title="Page 6/7", description="prefix:[y/]", color=0x5d00ff)
                page6.add_field(name="**timer <秒数>**", value="タイマー機能です")
                page6.add_field(name="**invite**", value="招待リンクを表示します")
                page6.add_field(name="**official**", value="サポート鯖のリンクを表示します")
                page6.add_field(name="**ping**", value="ネットの速さを知れます")
                page6.add_field(name="**say <内容>**", value="幽々子に言いたいことを言わせます")
                page6.set_thumbnail(
                    url="https://images-ext-2.discordapp.net/external/svQAPh7v9BBNiUgs3Fx4e27C1yhQ1KMp5h1KOhkKH3U/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/757807145264611378/f6e2d7ff1f8092409983a77952670eae.png")
                await msg.remove_reaction("6⃣", user)
                await msg.edit(embed=page6)
            elif '7⃣' in str(res.emoji):
                print('<<7⃣>>')
                page7 = discord.Embed(title="Page 7/7", description="prefix:[y/]", color=0x5d00ff)
                page7.add_field(name="**request <要望> <理由>**", value="リクエスト随時受付中です")
                page7.add_field(name="**feedback <内容>**",value="フィートバックを送ります")
                page7.add_field(name="**bug <不具合内容>**", value="不具合があれば教えてください")
                page7.set_thumbnail(
                    url="https://images-ext-2.discordapp.net/external/svQAPh7v9BBNiUgs3Fx4e27C1yhQ1KMp5h1KOhkKH3U/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/757807145264611378/f6e2d7ff1f8092409983a77952670eae.png")
                await msg.remove_reaction("7⃣", user)
                await msg.edit(embed=page7)


def setup(bot):
    bot.add_cog(help(bot))