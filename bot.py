import discord
import config as f
import json
from typing import Union
import logging

import asyncio

from discord.ext import commands

bot = commands.Bot(command_prefix=f.prefix)

developer = f.bot_developers
bot.load_extension('jishaku')
bot.load_extension('ext.info')
bot.load_extension('ext.admin')
bot.load_extension('ext.other')

@bot.event
async def on_command(ctx):
    e = discord.Embed(title="コマンド実行ログ", description=f"実行分:`{ctx.message.clean_content}`")
    e.set_author(name=f"{ctx.author}({ctx.author.id})", icon_url=ctx.author.avatar_url_as(static_format="png"))
    e.add_field(name="実行サーバー", value=f"{ctx.guild.name}({ctx.guild.id})")
    e.add_field(name="実行チャンネル", value=ctx.channel.name)

    e.timestamp = ctx.message.created_at
    ch = bot.get_channel(803558816834650152)

    await ch.send(embed=e)


@bot.event
async def on_command_error(ctx, error):
    ch = 799505924280156192
    embed = discord.Embed(title="エラー情報", description="", color=0xf00)
    embed.add_field(name="エラー発生サーバー名", value=ctx.guild.name, inline=False)
    embed.add_field(name="エラー発生サーバーID", value=ctx.guild.id, inline=False)
    embed.add_field(name="エラー発生ユーザー名", value=ctx.author.name, inline=False)
    embed.add_field(name="エラー発生ユーザーID", value=ctx.author.id, inline=False)
    embed.add_field(name="エラー発生コマンド", value=ctx.message.content, inline=False)
    embed.add_field(name="発生エラー", value=error, inline=False)
    m = await bot.get_channel(ch).send(embed=embed)
    await ctx.send("エラーが発生しました")


bot.run(f.TOKEN)