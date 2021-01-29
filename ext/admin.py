import textwrap
import discord
from discord import Intents
import typing
import aiohttp
from datetime import datetime, timedelta
from typing import Optional
from typing import Union
import time
import platform
from discord.ext import commands
import io
from discord.ext.commands import clean_content
from discord import Embed
from discord.ext.commands import Cog
import os
import random
import traceback
from contextlib import redirect_stdout
import asyncio


class AdminCog(commands.Cog, name="Admin"):
    """
    管理者用の機能です。
    管理者権限が無ければ使えません。
    """

    def __init__(self, bot):
        self.bot = bot
        self._last_result = None
        self.stream = io.StringIO()
        self.channel = None
        self._last_result = None

    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')

    @commands.command(name="load", description="```loadします```")
    @commands.is_owner()
    async def load(self, ctx, *, module):
        """`admin`"""
        try:
            self.bot.load_extension(module)
        except Exception:
            await ctx.send(f'```py\n{traceback.format_exc()}\n```')
        else:
            await ctx.send(f'`{module}をloadしました` ')

    @commands.is_owner()
    @commands.command(name="reload", description="```reloadします```")
    async def reload(self, ctx, *, module):
        """`admin`"""
        try:
            self.bot.unload_extension(module)
            self.bot.load_extension(module)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send(f"`{module}をreloadしました`")

    @commands.command(name="unload", description="```unloadします```")
    @commands.is_owner()
    async def unload(self, ctx, *, module):
        """`admin`"""
        try:
            self.bot.unload_extension(module)
        except Exception:
            await ctx.send(f'```py\n{traceback.format_exc()}\n```')
        else:
            await ctx.send(f'`{module}をunloadしました`')

    @commands.is_owner()
    @commands.command(name='listextensions', aliases=['le'])
    async def list_extensions(self, ctx):
        extensions_dict = self.bot.extensions
        msg = '```css\n'

        extensions = []

        for b in extensions_dict:
            # print(b)
            extensions.append(b)

        for a in range(len(extensions)):
            msg += f'{a}: {extensions[a]}\n'

        msg += '```'
        await ctx.send(msg)

    @commands.is_owner()
    @commands.command(pass_context=True, name='eval')
    async def _eval(self, ctx, *, body: str):
        """Evaluates a code"""

        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')

    @commands.is_owner()
    @commands.command(hidden=True)
    async def changestatus(self, ctx, status: str):
        '''Ändert den Online Status vom Bot (BOT OWNER ONLY)'''
        status = status.lower()
        if status == 'offline' or status == 'off' or status == 'invisible':
            discordStatus = discord.Status.invisible
        elif status == 'idle':
            discordStatus = discord.Status.idle
        elif status == 'dnd' or status == 'disturb':
            discordStatus = discord.Status.dnd
        else:
            discordStatus = discord.Status.online
        await self.bot.change_presence(status=discordStatus)
        await ctx.send(f'**:ok:** Ändere Status zu: **{discordStatus}**')

    @commands.command()
    @commands.is_owner()
    async def set_playing(self, ctx, *, game: str = None):
        """Set the playing status."""
        if game:
            await self.bot.change_presence(activity=discord.Game(game))
        ctx.delete()
        em = discord.Embed(color=0x00ff00)
        em.add_field(name="結果", value=f"{discord.Game(game)}に変わりました")
        await ctx.send(embed=em)

    @commands.is_owner()
    @commands.command(name="announce", aliases=["ann"], description="アナウンス用")
    async def announce(self, ctx, *, message):
        """```admin```"""
        await ctx.message.delete()
        em = discord.Embed(title="お知らせ", color=0x5d00ff)
        em.set_author(name="[y/]幽々子",
                      url="https://cdn.discordapp.com/avatars/757807145264611378/f6e2d7ff1f8092409983a77952670eae.png?size=512",
                      icon_url="https://cdn.discordapp.com/avatars/757807145264611378/f6e2d7ff1f8092409983a77952670eae.png?size=512")

        em.description = message
        await ctx.send(embed=em)

    @commands.command()
    @commands.is_owner()
    async def changenick(self, ctx, name=None):
        """`ニックネームの管理`"""
        print(f'{ctx.message.author.name}({ctx.message.guild.name})_' +
              ctx.message.content)
        await ctx.message.guild.me.edit(nick=name)
        if name is None:
            await ctx.send("私のニックネームをデフォルトの名前に変更したよ。")
        else:
            await ctx.reply("私のニックネームを" + name + "に変更したよ。")

    @commands.command(name="dm", aliases=["d", "send"], description="```dmを送る```")
    @commands.is_owner()
    async def dm(self, ctx, user_id: int, *, message: str):
        """`admin`"""
        user = self.bot.get_user(user_id)
        if not user:
            return await ctx.send(f"Could not find any UserID matching **{user_id}**")

        try:
            await user.send(message)
            await ctx.send(f"✉️ Sent a DM to **{user_id}**")
        except discord.Forbidden:
            await ctx.reply("This user might be having DMs blocked or it's a bot account...")

    @commands.is_owner()
    @commands.command(hidden=True, aliases=['guilds'])
    async def servers(self, ctx):
        '''Listet die aktuellen verbundenen Guilds auf (BOT OWNER ONLY)'''
        msg = '```js\n'
        msg += '{!s:19s} | {!s:>5s} | {} | {}\n'.format('ID', 'Member', 'Name', 'Owner')
        for guild in self.bot.guilds:
            msg += '{!s:19s} | {!s:>5s}| {} | {}\n'.format(guild.id, guild.member_count, guild.name, guild.owner)
        msg += '```'
        await ctx.reply(msg)

    @commands.is_owner()
    @commands.command(name="system_shutdown", aliases=["shutdown", "sh"], description="```botを停止します```")
    async def system_shutdown(self, ctx):
        """`admin`"""
        e = discord.Embed(title="System - shutdown", description="処理中...", color=0x5d00ff)
        msg = await ctx.send(embed=e)

        try:
            e.description = None
            e.add_field(name="成功", value="Botを停止するよ！")

            await msg.edit(embed=e)
            await self.bot.change_presence(activity=discord.Game(name=f'Disabling YuyukoBot {self} Please Wait...'))
            await asyncio.sleep(5)

            await self.bot.close()
            return
        except Exception as er:
            e.description = None
            e.add_field(name="エラー", value=f"py\n{er}\n")
            print(f"[Error] {traceback.format_exc(3)}")
            await msg.edit(embed=e)

    @commands.command(aliases=['archive'])
    @commands.cooldown(1, 60, commands.cooldowns.BucketType.channel)
    async def log(self, ctx, *limit: int):
        '''Archiviert den Log des derzeitigen Channels und läd diesen als Attachment hoch
        Beispiel:
        -----------
        :log 100
        '''
        if not limit:
            limit = 10
        else:
            limit = limit[0]
        logFile = f'{ctx.channel}.log'
        counter = 0
        with open(logFile, 'w', encoding='UTF-8') as f:
            f.write(
                f'Archivierte Nachrichten vom Channel: {ctx.channel} am {ctx.message.created_at.strftime("%d.%m.%Y %H:%M:%S")}\n')
            async for message in ctx.channel.history(limit=limit, before=ctx.message):
                try:
                    attachment = '[Angehängte Datei: {}]'.format(message.attachments[0].url)
                except IndexError:
                    attachment = ''
                f.write(
                    '{} {!s:20s}: {} {}\r\n'.format(message.created_at.strftime('%d.%m.%Y %H:%M:%S'), message.author,
                                                    message.clean_content, attachment))
                counter += 1
        msg = f':ok: {counter} Nachrichten wurden archiviert!'
        f = discord.File(logFile)
        await ctx.send(file=f, content=msg)
        os.remove(logFile)


def setup(bot):
    bot.add_cog(AdminCog(bot))