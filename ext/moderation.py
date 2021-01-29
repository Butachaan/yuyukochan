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
import os
import functools
import inspect
from discord.ext.commands import clean_content
from discord import Embed
from discord.ext.commands import Cog
import sys
import json
import traceback
import asyncio


def to_emoji(c):
    base = 0x1f1e6
    return chr(base + c)


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def format_mod_embed(self, ctx, user, success, method, duration=None, location=None):
        '''Helper func to format an embed to prevent extra code'''
        emb = discord.Embed(timestamp=ctx.message.created_at)
        emb.set_author(name=method.title(), icon_url=user.avatar_url)
        emb.color = await ctx.get_dominant_color(user.avatar_url)
        emb.set_footer(text=f'User ID: {user.id}')
        if success:
            if method == 'ban' or method == 'hackban':
                emb.description = f'{user} was just {method}ned.'
            elif method == 'unmute':
                emb.description = f'{user} was just {method}d.'
            elif method == 'mute':
                emb.description = f'{user} was just {method}d for {duration}.'
            elif method == 'channel-lockdown' or method == 'server-lockdown':
                emb.description = f'`{location.name}` is now in lockdown mode!'
            else:
                emb.description = f'{user} was just {method}ed.'
        else:
            if method == 'lockdown' or 'channel-lockdown':
                emb.description = f"You do not have the permissions to {method} `{location.name}`."
            else:
                emb.description = f"You do not have the permissions to {method} {user.name}."

        with open('data/config.json') as f:
            config = json.load(f)
            modlog = os.environ.get('MODLOG') or config.get('MODLOG')
        if modlog is None:
            await ctx.send('You have not set `MODLOG` in your config vars.', delete_after=5)
        else:
            modlog = discord.utils.get(self.bot.get_all_channels(), id=int(modlog))
            if modlog is None:
                await ctx.send('Your `MODLOG` channel ID is invalid.', delete_after=5)
            else:
                await modlog.send(embed=emb)

        return emb

    @commands.command(name="kick")
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await ctx.guild.kick(user=member, reason=reason)

        # Using our past episodes knowledge can we make the log channel dynamic?
        embed = discord.Embed(
            title=f"{ctx.author.name} kicked: {member.name}", description=reason
        )
        await ctx.send(embed=embed)

    @commands.command(
        name="ban",
        description="A command which bans a given user",
        usage="<user> [reason]",
    )
    @commands.guild_only()
    @commands.has_guild_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await ctx.guild.ban(user=member, reason=reason)

        # Using our past episodes knowledge can we make the log channel dynamic?
        embed = discord.Embed(
            title=f"{ctx.author.name} banned: {member.name}", description=reason
        )
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.command(no_pm=True)
    async def banlist(self, ctx):
        """```banされた人が確認できます``` """
        try:
            bans = await ctx.guild.bans()
        except:
            return await ctx.send("You don't have the perms to see bans. (｡◝‿◜｡)")
        e = discord.Embed(color=0x5d00ff)
        e.set_author(name=f'List of Banned Members ({len(bans)}):', icon_url=ctx.guild.icon_url)
        result = ',\n'.join(["[" + (str(b.user.id) + "] " + str(b.user)) for b in bans])
        if len(result) < 1990:
            total = result
        else:
            total = result[:1990]
            e.set_footer(text=f'Too many bans to show here!')
        e.description = f'```bf\n{total}```'
        await ctx.send(embed=e)

    @commands.command(name="unban", description="```banを解除する```")
    @commands.bot_has_permissions(ban_members=True)
    async def unban(self, ctx, user: discord.User):
        """`BANの権限`"""
        if user.bot:
            return await ctx.say("owner.bot")
        if await self.bot.is_owner(user):
            return await ctx.say("owner.you")
        if not await self.bot.is_banned(user.id):
            return await ctx.say("owner.yet")
        self.bot.db.execute("UPDATE users SET banned = 0 WHERE user_id = ?", (user.id,))
        await ctx.say("owner.done")

    @commands.bot_has_permissions(ban_members=True)
    @commands.command(aliases=['hban'], pass_context=True)
    async def hackban(self, ctx, user_id: int):
        """`BANの権限`"""
        author = ctx.message.author
        guild = author.guild

        user = guild.get_member(user_id)
        if user is not None:
            await ctx.invoke(self.ban, user=user)
            return

        try:
            await self.bot.http.ban(user_id, guild.id, 0)
            await ctx.message.edit(content=self.bot.bot_prefix + 'Banned user: %s' % user_id)
        except discord.NotFound:
            await ctx.message.edit(content=self.bot.bot_prefix + 'Could not find user. '
                                                                 'Invalid user ID was provided.')
        except discord.errors.Forbidden:
            await ctx.message.edit(content=self.bot.bot_prefix + 'Could not ban user. Not enough permissions.')

    @commands.guild_only()
    @commands.command(name="baninfo")
    async def baninfo(self, ctx, *, name_or_id):
        """`BANの権限`"""
        ban = await ctx.get_ban(name_or_id)
        em = discord.Embed()
        em.color = await ctx.get_dominant_color(ban.user.avatar_url)
        em.set_author(name=str(ban.user), icon_url=ban.user.avatar_url)
        em.add_field(name='Reason', value=ban.reason or 'None')
        em.set_thumbnail(url=ban.user.avatar_url)
        em.set_footer(text=f'User ID: {ban.user.id}')

        await ctx.send(embed=em)

    @commands.command(name="poll", description="```アンケートを取れます```")
    async def poll(self, ctx, *, question):
        """`誰でも`"""

        # a list of messages to delete when we're all done
        messages = [ctx.message]
        answers = []

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel and len(m.content) <= 100

        for i in range(20):
            messages.append(await ctx.send(f'Say poll option or ```{ctx.prefix}cancel to publish poll.```'))

            try:
                entry = await self.bot.wait_for('message', check=check, timeout=60.0)
            except asyncio.TimeoutError:
                break

            messages.append(entry)

            if entry.clean_content.startswith(f'{ctx.prefix}cancel'):
                break

            answers.append((to_emoji(i), entry.clean_content))

        try:
            await ctx.channel.delete_messages(messages)
        except:
            pass  # oh well

        answer = '\n'.join(f'{keycap}: {content}' for keycap, content in answers)
        actual_poll = await ctx.send(f'{ctx.author} asks: {question}\n\n{answer}')
        for emoji, _ in answers:
            await actual_poll.add_reaction(emoji)

    @poll.error
    async def poll_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send('Missing the question.')

    @commands.command(name="poll2", aliases=["vote"], description="```投票を取ることができます```")
    async def quickpoll(self, ctx, *questions_and_choices: str):
        """`誰でも`"""

        if len(questions_and_choices) < 3:
            return await ctx.send('Need at least 1 question with 2 choices.')
        elif len(questions_and_choices) > 21:
            return await ctx.send('You can only have up to 20 choices.')

        perms = ctx.channel.permissions_for(ctx.me)
        if not (perms.read_message_history or perms.add_reactions):
            return await ctx.send('Need Read Message History and Add Reactions permissions.')

        question = questions_and_choices[0]
        choices = [(to_emoji(e), v) for e, v in enumerate(questions_and_choices[1:])]

        try:
            await ctx.message.delete()
        except:
            pass

        body = "\n".join(f"{key}: {c}" for key, c in choices)
        poll = await ctx.send(f'```{ctx.author} asks: {question}```\n\n{body}')
        for emoji, _ in choices:
            await poll.add_reaction(emoji)

    @commands.command(name="mute", aliases=["mt"], description="```ユーザーをmute```")
    @commands.guild_only()
    async def mute(self, ctx, user: discord.Member, time: int = 15):
        '''```役職の管理```'''
        secs = time * 60
        for channel in ctx.guild.channels:
            if isinstance(channel, discord.TextChannel):
                await ctx.channel.set_permissions(user, send_messages=False)
            elif isinstance(channel, discord.VoiceChannel):
                await channel.set_permissions(user, connect=False)
        await ctx.send(f"{user.mention} has been muted for {time} minutes.")
        await asyncio.sleep(secs)
        for channel in ctx.guild.channels:
            if isinstance(channel, discord.TextChannel):
                await ctx.channel.set_permissions(user, send_messages=None)
            elif isinstance(channel, discord.VoiceChannel):
                await channel.set_permissions(user, connect=None)
        await ctx.send(f'{user.mention} has been unmuted from the guild')

    @commands.command(name="unmute,unMute", description="```ミュートを解除```")
    @commands.guild_only()
    async def unmute(self, ctx, user: discord.Member):
        '''```役職の管理```'''
        for channel in ctx.guild.channels:
            if isinstance(channel, discord.TextChannel):
                await ctx.channel.set_permissions(user, send_messages=None)
            elif isinstance(channel, discord.VoiceChannel):
                await channel.set_permissions(user, connect=None)
        await ctx.send(f'{user.mention} has been unmuted from the guild.')

    @commands.command(name="purge", descriotion="```clearコマンドと同じです```")
    @commands.guild_only()
    async def purge(self, ctx, messages: int):
        '''`メッセージの管理`'''
        if messages > 99:
            messages = 99
        await ctx.channel.purge(limit=messages + 1)
        await ctx.send(f'{messages} messages deleted. 👌', delete_after=3)

    @commands.guild_only()
    @commands.command(name="addrole", aliases=["ar"], description="```ユーザーに役職を付与します```", pass_context=True)
    async def addrole(self, ctx, member: discord.Member, *, rolename: str):
        '''`役職の管理`'''
        role = discord.utils.find(lambda m: rolename.lower() in m.name.lower(), ctx.message.guild.roles)
        if not role:
            return await ctx.send('That role does not exist.')
        try:
            await member.add_roles(role)
            await ctx.send(f'Added: `{role.name}`')
        except:
            await ctx.send("I don't have the perms to add that role.")

    @commands.guild_only()
    @commands.command(name="removerole", aliases=["rr"], description="```ユーザーの役職を剥奪します```", pass_context=True)
    async def removerole(self, ctx, user: discord.Member, *, role: discord.Role):
        """`役職の管理`"""
        if ctx.author.top_role >= user.top_role or ctx.author == ctx.guild.owner:
            await user.remove_roles(role)
            msg = await ctx.send(f"Ok, `{role}` was add from {user.mention}")
            await msg.add_reaction("\N{THUMBS UP SIGN}")

    @commands.guild_only()
    @commands.command(name="slowmode", aliases=['slowmo'], description="```低速モードを設定します```")
    async def slowmode(self, ctx, seconds: int = 0):
        """```メッセージの管理```"""
        if seconds > 120:
            return await ctx.send(":no_entry: Amount can't be over 120 seconds")
        if seconds is 0:
            await ctx.channel.edit(slowmode_delay=seconds)
            a = await ctx.send("**Slowmode is off for this channel**")
            await a.add_reaction("a:SpectrumOkSpin:466480898049835011")
        else:
            if seconds is 1:
                numofsecs = "second"
            else:
                numofsecs = "seconds"
            await ctx.channel.edit(slowmode_delay=seconds)
            confirm = await ctx.send(
                f"**Set the channel slow mode delay to `{seconds}` {numofsecs}\nTo turn this off, do $slowmode**")
            await confirm.add_reaction("\N{THUMBS UP SIGN}")

    @commands.group(invoke_without_command=True)
    async def lockdown(self, ctx):
        """Server/Channel lockdown"""
        pass

    @lockdown.command(aliases=['channel'])
    async def chan(self, ctx, channel: discord.TextChannel = None, *, reason=None):
        if channel is None: channel = ctx.channel
        try:
            await channel.set_permissions(ctx.guild.default_role,
                                          overwrite=discord.PermissionOverwrite(send_messages=False), reason=reason)
        except:
            success = False
        else:
            success = True
        emb = await self.format_mod_embed(ctx, ctx.author, success, 'channel-lockdown', 0, channel)
        await ctx.send(embed=emb)

    @lockdown.command()
    async def server(self, ctx, server: discord.Guild = None, *, reason=None):
        if server is None: server = ctx.guild
        progress = await ctx.send(f'Locking down {server.name}')
        try:
            for channel in server.channels:
                await channel.set_permissions(ctx.guild.default_role,
                                              overwrite=discord.PermissionOverwrite(send_messages=False), reason=reason)
        except:
            success = False
        else:
            success = True
        emb = await self.format_mod_embed(ctx, ctx.author, success, 'server-lockdown', 0, server)
        progress.delete()
        await ctx.send(embed=emb)


def setup(bot):
    bot.add_cog(Moderation(bot))
