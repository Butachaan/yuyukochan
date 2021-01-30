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


class infoCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def _getRoles(roles):
        string = ''
        for role in roles[::-1]:
            if not role.is_default():
                string += f'{role.mention}, '
        if string == '':
            return 'None'
        else:
            return string[:-2]

    @staticmethod
    def _getEmojis(emojis):
        string = ''
        for emoji in emojis:
            string += str(emoji)
        if string == '':
            return 'None'
        else:
            return string[:1000]  # The maximum allowed charcter amount for embed fields

    @commands.command(name="serverinfo", aliases=["si"], description="```サーバーの情報```")
    async def serverinfo(self, ctx, *, guild_id: int = None,arg):
        """カスさんサーバー情報"""

        if guild_id is not None and await self.bot.is_owner(ctx.author):
            guild = self.bot.get_guild(int(arg))
            if guild is None:
                return await ctx.send(f'Invalid Guild ID given.')
        else:
            guild = ctx.bot.get_guild(int(arg))
            statuses = [len(list(filter(lambda m: str(m.status) == "online", guild.members))),
                        len(list(filter(lambda m: str(m.status) == "idle", guild.members))),
                        len(list(filter(lambda m: str(m.status) == "dnd", guild.members))),
                        len(list(filter(lambda m: str(m.status) == "offline", guild.members)))]

            e = discord.Embed(title="サーバー検索", description=f"{guild.name}の情報を表示しています", color=0x05deff)
            e.add_field(name="サーバー名", value=f"{guild.name}({str(guild.id)})")

        if guild.icon_url is not None:
            e.set_thumbnail(url=guild.icon_url)

            e.add_field(name="絵文字", value=len(guild.emojis))
            e.add_field(name="地域", value=str(guild.region))
            e.add_field(name="認証度", value=str(guild.verification_level))

            e.add_field(name="Owner", value=ctx.guild.owner)
            e.add_field(name="created", value=guild.created_at.strftime("%d/%m/%Y %H:%M:%S"))
            e.add_field(name="Statuses", value=f"🟢 {statuses[0]} 🟠 {statuses[1]} 🔴 {statuses[2]} ⚪ {statuses[3]}")

            bm = 0
            ubm = 0
            for m in guild.members:
                if m.bot:
                    bm = bm + 1
                else:
                    ubm = ubm + 1
            e.add_field(name="メンバー数",
                        value=f"{len(ctx.guild.members)}(<:bot:798877222638845952>:{bm}/:busts_in_silhouette::{ubm})")
            e.add_field(name="チャンネル数",
                        value=f'{("<:categorie:798883839124308008>")}:{len(guild.categories)}\n{(":speech_balloon:")}:{len(guild.text_channels)}\n{(":mega:")}:{len(guild.voice_channels)}')

            if guild.system_channel:
                e.add_field(name="システムチャンネル", value=f"{guild.system_channel}\n({str(guild.system_channel.id)})")
            try:

                e.add_field(name="welcome", value=guild.system_channel_flags.join_notifications)
                e.add_field(name="boost", value=guild.system_channel_flags.premium_subscriptions)
            except:
                pass
            if guild.afk_channel:
                e.add_field(name="AFKチャンネル", value=f"{guild.afk_channel.name}({str(guild.afk_channel.id)})")
                e.add_field(name="AFKタイムアウト", value=str(guild.afk_timeout / 60))

            e.add_field(name="役職数", value=len(guild.roles))

            e.add_field(name='Guild Shard', value=ctx.guild.shard_id, inline=True)
            roles = self._getRoles(ctx.guild.roles)
            if len(roles) <= 1024:
                e.add_field(name="役職", value=roles, inline=False)
            else:
                e.add_field(name="役職", value="多いですよ")

            emojis = self._getEmojis(ctx.guild.emojis)

            e.add_field(name='カスタム絵文字', value=emojis, inline=False)

            await ctx.reply(embed=e)

    @commands.command(name="info", description="豆腐botの")
    async def info(self, ctx):

        """`誰でも`"""
        pythonVersion = platform.python_version()
        dpyVersion = discord.__version__
        channels = str(len(set(self.bot.get_all_channels())))
        total_members = [x.id for x in self.bot.get_all_members()]
        unique_members = set(total_members)
        if len(total_members) == len(unique_members):
            member_count = "{:,}".format(len(total_members))
        else:
            member_count = "{:,} ({:,} unique)".format(len(total_members), len(unique_members))

        guild_count = "{:,}".format(len(self.bot.guilds))
        mem = psutil.virtual_memory()

        allmem = str(mem.total / 1000000000)[0:3]
        used = str(mem.used / 1000000000)[0:3]
        ava = str(mem.available / 1000000000)[0:3]
        memparcent = mem.percent

        embed = discord.Embed(title="幽々子",
                              url="https://cdn.discordapp.com/avatars/757807145264611378/f6e2d7ff1f8092409983a77952670eae.png?size=1024",
                              color=0x5d00ff)
        embed.set_author(name="y/info")
        embed.add_field(name="サーバー数", value=guild_count)
        embed.add_field(name="ユーザー数", value=member_count)

        embed.set_thumbnail(
            url="https://cdn.discordapp.com/avatars/757807145264611378/f6e2d7ff1f8092409983a77952670eae.png?size=1024")
        embed.add_field(name="Channels bot can see:", value=channels)
        embed.add_field(name="discord.pyのバージョン", value=dpyVersion)
        embed.add_field(name="Pythonのバージョン", value=pythonVersion)
        embed.add_field(name="プロセッサ", value="Intel(R) Xeon(R) CPU E5-2660 v3 @ 2.60GHz")
        embed.add_field(name="OS", value=f"{platform.system()} {platform.release()}({platform.version()})")
        embed.add_field(
            name="メモリ", value=f"全てのメモリ容量:{allmem}GB\n使用量:{used}GB({memparcent}%)\n空き容量{ava}GB({100 - memparcent}%)")
        await ctx.reply(embed=embed)

    @commands.command(name="userinfo", aliases=["ui"], description="ユーザーの情報")
    async def userinfo(self, ctx, *, user: Union[discord.Member, discord.User] = None):
        """`誰でも`"""

        user = user or ctx.author
        e = discord.Embed(color=0xb300ff)
        roles = [r.mention for r in user.roles]
        e.set_author(name="ユーザー情報")
        perms = "`" + "`, `".join(perm for perm, value in user.guild_permissions if value) + "`"
        since_created = (ctx.message.created_at - user.created_at).days
        since_joined = (ctx.message.created_at - user.joined_at).days
        user_created = user.created_at.strftime("%d %b %Y %H:%M")
        user_joined = user.joined_at.strftime("%d %b %Y %H:%M")

        created_at = f"{user_created}\n({since_created} days ago)"
        joined_at = f"{user_joined}\n({since_joined} days ago)"

        e.add_field(name="ユーザー名", value=f"{user}({user.id})", inline=True)

        voice = getattr(user, 'voice', None)
        if voice is not None:
            vc = voice.channel
            other_people = len(vc.members) - 1
            voice = f'{vc.name} with {other_people} others' if other_people else f'{vc.name} by themselves'
            e.add_field(name='Voice', value=voice, inline=True)
        else:
            e.add_field(name="voice", value="入っていません")

        e.add_field(name="ニックネーム", value=user.display_name)
        e.add_field(name="bot?", value=user.bot)
        e.add_field(name="ブースト!", value=bool(user.premium_since), inline=True)

        e.add_field(name="Discord参加日:", value=created_at, inline=True)
        e.add_field(name="サーバー参加日", value=joined_at, inline=True)

        e.add_field(name="Highest Role:", value=user.top_role.mention)
        print(user.top_role.mention)

        if roles:
            e.add_field(name=f"Roles({len(roles)})",
                        value=', '.join(roles) if len(roles) < 40 else f'{len(roles)} roles', inline=False)

        e.add_field(name='Avatar Link', value=user.avatar_url, inline=False)

        if user.avatar:
            e.set_thumbnail(url=user.avatar_url)

        if isinstance(user, discord.User):
            e.set_footer(text='This member is not in this server.')

        await ctx.reply(embed=e)

        e = discord.Embed(color=0xb300ff)
        if isinstance(user, discord.Member):
            e.add_field(name='権限', value=perms)

        await ctx.send(embed=e)

    @commands.command()
    async def user(self, ctx, *, user: Union[discord.Member, discord.User] = None):
        """Shows info about a user."""

        user = user or ctx.author
        e = discord.Embed(title="外部ユーザー情報", color=0x0066ff)
        roles = [role.name.replace('@', '@\u200b') for role in getattr(user, 'roles', [])]
        e.set_author(name=str(user))
        since_created = (ctx.message.created_at - user.created_at).days
        user_created = user.created_at.strftime("%d %b %Y %H:%M")
        created_at = f"{user_created}\n({since_created} days ago)"
        e.add_field(name='ユーザー名', value=f"{user.name}({user.id})", inline=False)
        e.add_field(name="Discord参加日:", value=created_at, inline=True)

        voice = getattr(user, 'voice', None)
        if voice is not None:
            vc = voice.channel
            other_people = len(vc.members) - 1
            voice = f'{vc.name} with {other_people} others' if other_people else f'{vc.name} by themselves'
            e.add_field(name='Voice', value=voice, inline=False)

        if roles:
            e.add_field(name='Roles', value=', '.join(roles) if len(roles) < 10 else f'{len(roles)} roles',
                        inline=False)

        if user.avatar:
            e.set_thumbnail(url=user.avatar_url)

        if isinstance(user, discord.User):
            e.set_footer(text='This member is not in this server.')

        await ctx.reply(embed=e)

    @commands.command(name="roleinfo", aliases=["ri", "role"], description="```役職の情報```")
    async def roleinfo(self, ctx, *, role: commands.RoleConverter = None):
        """`誰でも`"""
        if role is None:
            await ctx.send(ctx._("roleinfo-howto"))
        elif role.guild == ctx.guild:
            embed = discord.Embed(title=role.name, description=f"id:{role.id}", color=role.colour)
            embed.add_field(name="別表示", value=role.hoist)
            embed.add_field(name="メンション", value=role.mentionable)

            embed.add_field(name='メンバー数', value=str(len(role.members)))
            embed.add_field(name='カラーコード', value=str(role.color))

            embed.add_field(name='作成日時', value=role.created_at.__format__('%x at %X'))
            embed.add_field(name='メンバー [%s]' % len(role.members),
                            value='%s Online' % sum(1 for m in role.members if m.status != discord.Status.offline),
                            inline=True)

            perms = ""
        if role.permissions.administrator:
            perms += "管理者権限, "
        if role.permissions.create_instant_invite:
            perms += "招待リンクの作成, "
        if role.permissions.kick_members:
            perms += "Kick権限, "
        if role.permissions.ban_members:
            perms += "Ban権限, "
        if role.permissions.manage_channels:
            perms += "チャンネルの管理, "
        if role.permissions.manage_guild:
            perms += "サーバーの管理, "
        if role.permissions.add_reactions:
            perms += "リアクションの追加, "
        if role.permissions.view_audit_log:
            perms += "サーバーの統計を表示, "
        if role.permissions.read_messages:
            perms += "メッセージの表示, "
        if role.permissions.send_messages:
            perms += "メッセージを送信, "
        if role.permissions.send_tts_messages:
            perms += "TTSメッセージの送信, "
        if role.permissions.manage_messages:
            perms += "メッセージを管理, "
        if role.permissions.embed_links:
            perms += "埋め込みリンクの送信, "
        if role.permissions.attach_files:
            perms += "ファイルの添付, "
        if role.permissions.read_message_history:
            perms += "メッセージの履歴の表示, "
        if role.permissions.mention_everyone:
            perms += "役職,全員宛メンション, "
        if role.permissions.external_emojis:
            perms += "外侮の絵文字を使用, "
        if role.permissions.connect:
            perms += "接続, "
        if role.permissions.speak:
            perms += "発言, "
        if role.permissions.mute_members:
            perms += "メンバーをミュート, "
        if role.permissions.deafen_members:
            perms += "スピーカーミュート, "
        if role.permissions.move_members:
            perms += "メンバーの移動, "
        if role.permissions.use_voice_activation:
            perms += "音声検出を使用, "
        if role.permissions.change_nickname:
            perms += "ニックネームを変える, "
        if role.permissions.manage_nicknames:
            perms += "ニックネームを管理, "
        if role.permissions.manage_roles:
            perms += "役職を管理, "
        if role.permissions.manage_webhooks:
            perms += "webhookを管理, "
        if role.permissions.manage_emojis:
            perms += "絵文字を管理, "

        if perms is None:
            perms = "None"
        else:
            perms = perms.strip(", ")

            embed.add_field(name='Permissions', value=f"`{perms}`")

            hasmember = ""
            for m in role.members:
                hasmember = hasmember + f"{m.mention},"
            if not hasmember == "":
                if len(hasmember) <= 1024:
                    embed.add_field(name="メンバー", value=hasmember)
                else:
                    embed.add_field(name="メンバー", value="ユーザーが多すぎます")
            else:
                embed.add_field(name="メンバー", value="None")

            await ctx.send(embed=embed)

    @commands.command(name="avatar", description="```ユーザーのアイコン```")
    async def avatar(self, ctx, *, user: Union[discord.Member, discord.User] = None):
        """`誰でも`"""
        embed = discord.Embed(color=0x5d00ff)
        user = user or ctx.author
        avatar = user.avatar_url_as(static_format='png')
        embed.set_author(name=str(user), url=avatar)
        embed.set_image(url=avatar)
        await ctx.reply(embed=embed)

    @commands.command(aliases=['e'])
    async def emoji(self, ctx, emojiname: str):
        """`誰でも`"""
        emoji = discord.utils.find(lambda e: e.name.lower() == emojiname.lower(), self.bot.emojis)
        if emoji:
            tempEmojiFile = 'tempEmoji.png'
            async with aiohttp.ClientSession() as cs:
                async with cs.get(str(emoji.url)) as img:
                    with open(tempEmojiFile, 'wb') as f:
                        f.write(await img.read())
                f = discord.File(tempEmojiFile)
                await ctx.send(file=f)
                os.remove(tempEmojiFile)
        else:
            await ctx.reply(':x: Konnte das angegebene Emoji leider nicht finden :(')

    @commands.command(aliases=['emotes'])
    async def emojis(self, ctx):
        """`誰でも`"""
        msg = ''
        for emoji in self.bot.emojis:
            if len(msg) + len(str(emoji)) > 1000:
                await ctx.send(msg)
                msg = ''
            msg += str(emoji)
        await ctx.reply(msg)

    @commands.command(name="messageinfo", aliases=["msg", "message"], description="```メッセージの情報```")
    async def messageinfo(self, ctx, target: Union[commands.MessageConverter, None]):
        """`誰でも`"""
        if target:
            fetch_from = "引数"
            msg = target
        else:
            if ctx.message.reference and ctx.message.type == discord.MessageType.default:
                if ctx.message.reference.cached_message:
                    fetch_from = "返信"
                    msg = ctx.message.reference.cached_message
                else:
                    try:
                        fetch_from = "返信"
                        msg = await self.bot.get_channel(ctx.message.reference.channel_id).fetch_message(
                            ctx.message.reference.message_id)
                    except:
                        fetch_from = "コマンド実行メッセージ"
                        msg = ctx.message

            else:
                fetch_from = "コマンド実行メッセージ"
                msg = ctx.message

        e = discord.Embed(title=f"メッセージ{fetch_from}", descriptio=msg.system_content, color=0x5d00ff)
        e.set_author(name=f"{msg.author.display_name}({msg.author.id}){'[bot]' if msg.author.bot else ''}のメッセージ",
                     icon_url=msg.author.avatar_url_as(static_format="png"))

        post_time = msg.created_at.strftime("%d/%m/%Y %H:%M:%S")

        if msg.edited_at:
            edit_time = msg.edited_at.strftime("%d/%m/%Y %H:%M:%S")

        else:
            edit_time = "なし"

        e.set_footer(text=f"メッセージ送信時間:{post_time}/最終編集時間:{edit_time}")

        e.add_field(name="メッセージ", value=str(msg.id))
        e.add_field(name="システムメッセージ？", value=msg.is_system())
        e.add_field(name="添付ファイル数", value=f"{len(msg.attachments)}個")
        e.add_field(name="埋め込み数", value=f"{len(msg.embeds)}個")

        if msg.guild.rules_channel and msg.channel_id == msg.guild.rules_channel.id:
            chtype = f"{msg.channel.name}({msg.channel.id}):ルールチャンネル"
        elif msg.channel.is_news():
            chtype = f"{msg.Channel.name}({msg.channel.id}):アナウンスチャンネル"
        else:
            chtype = f"{msg.channel.name}({msg.channel.id}):テキストチャンネル"
        e.add_field(name="メッセージの送信チャンネル", value=chtype)

        if msg.reference:
            e.add_field(name="メッセージの返信等", value=f"返信元確認用:`{msg.reference.channel_id}-{msg.reference.message_id}`")

        e.add_field(name="メンションの内訳",
                    value=f"全員宛メンション:{msg.mention_everyone}\nユーザーメンション:{len(msg.mentions)}個\n役職メンション:{len(msg.role_mentions)}個\nチャンネルメンション:{len(msg.channel_mentions)}個")
        if msg.webhook_id:
            e.add_field(name="webhook投稿", value=f"ID:{msg.webhook_id}")
        e.add_field(name="ピン留めされてるかどうか", value=str(msg.pinned))
        if len(msg.reactions) != 0:
            e.add_field(name="リアクション", value=",".join({f"{r.emoji}:{r.count}" for r in msg.reactions}))

        e.add_field(name="メッセージフラグ", value=[i[0] for i in iter(msg.flags) if i[1]])

        e.add_field(name="メッセージに飛ぶ", value=msg.jump_url)

        try:
            await ctx.replay(embed=e, mentions_author=False)
        except:
            await ctx.reply(embed=e)

    @commands.command(name="channelinfo", aliases=["chinfo", "channel"], description="```チャンネルの情報```")
    async def channelinfo(self, ctx, target=None):
        """`誰でも`"""
        if target is None:
            target = ctx.channel
        else:
            try:
                target = await commands.TextChannelConverter().convert(ctx, target)
            except:
                try:
                    target = await commands.VoiceChannelConverter().convert(ctx, target)
                except:
                    try:
                        target = await commands.CategoryChannelConverter().convert(ctx, target)
                    except:
                        try:
                            target = self.bot.get_channel(int(target))
                        except:
                            await ctx.send("引数をチャンネルに変換できませんでした。")
                            return

        if target is None:
            return await ctx.send("そのチャンネルが見つかりませんでした。")
        if not target.guild.id == ctx.guild.id:
            await ctx.send("別のサーバーのチャンネルです")
            return
        if isinstance(target, discord.TextChannel):
            if target.is_news():
                if "NEWS" in target.guild.features:
                    e = discord.Embed(name="チャンネル情報", description=f"{target.name}(タイプ:アナウンス)\nID:{target.id}",
                                      color=0x00ff00)
                else:
                    e = discord.Embed(name="チャンネル情報", description=f"{target.name}(タイプ:アナウンス(フォロー不可))\nID:{target.id}")
            else:
                e = discord.Embed(name="チャンネル情報", description=f"{target.name}(タイプ:テキスト)\nID:{target.id}")
            e.timestamp = target.created_at
            if target.category:
                e.add_field(name="所属するカテゴリ", value=f"{target.category.name}({target.category.id})")
            e.add_field(name="チャンネルトピック", value=target.topic or "なし")
            if not target.slowmode_delay == 0:
                e.add_field(name="スローモードの時間", value=f"{target.slowmode_delay}秒")
            e.add_field(name="NSFW指定有無", value=target.is_nsfw())
            mbs = ""
            for m in target.members:
                if len(mbs + f"`{m.name}`,") >= 1020:
                    mbs = mbs + f"他"
                    break
                else:
                    mbs = mbs + f"`{m.name}`,"
            if mbs != "":
                e.add_field(name=f"メンバー({len(target.members)}人)", value=mbs, inline=False)
            await ctx.send(embed=e)
        elif isinstance(target, discord.VoiceChannel):
            e = discord.Embed(name="チャンネル情報", description=f"{target.name}(タイプ:ボイス)\nID:{target.id}")
            e.timestamp = target.created_at
            if target.category:
                e.add_field(name="所属するカテゴリ", value=f"{target.category.name}({target.category.id})")
            e.add_field(name="チャンネルビットレート", value=f"{target.bitrate / 1000}Kbps")
            if not target.user_limit == 0:
                e.add_field(name="ユーザー数制限", value=f"{target.user_limit}人")
            mbs = ""
            for m in target.members:
                if len(mbs + f"`{m.name}`,") >= 1020:
                    mbs = mbs + f"他"
                    break
                else:
                    mbs = mbs + f"`{m.name}`,"
            if mbs != "":
                e.add_field(name=f"参加可能なメンバー({len(target.members)}人)", value=mbs, inline=False)
            await ctx.send(embed=e)
        elif isinstance(target, discord.CategoryChannel):
            e = discord.Embed(name="チャンネル情報", description=f"{target.name}(タイプ:カテゴリ)\nID:{target.id}")
            e.timestamp = target.created_at
            e.add_field(name="NSFW指定有無", value=target.is_nsfw())
            mbs = ""
            for c in target.channels:
                if c.type is discord.ChannelType.news:
                    if "NEWS" in target.guild.features:
                        chtype = "アナウンス"
                    else:
                        chtype = "アナウンス(フォロー不可)"
                elif c.type is discord.ChannelType.store:
                    chtype = "ストア"
                elif c.type is discord.ChannelType.voice:
                    chtype = "ボイス"
                elif c.type is discord.ChannelType.text:
                    chtype = "テキスト"
                else:
                    chtype = str(c.type)
                if len(mbs + f"`{c.name}({chtype})`,") >= 1020:
                    mbs = mbs + f"他"
                    break
                else:
                    mbs = mbs + f"`{c.name}({chtype})`,"
            if mbs != "":
                e.add_field(name=f"所属するチャンネル({len(target.channels)}チャンネル)", value=mbs, inline=False)
            await ctx.reply(embed=e)


def setup(bot):
    bot.add_cog(infoCog(bot))