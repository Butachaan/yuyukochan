import discord
import config as f
import json
from typing import Union
import logging
import textwrap

import asyncio

from discord.ext import commands

bot = commands.Bot(command_prefix=f.prefix)


class Help(commands.HelpCommand):
    def __init__(self):
        super().__init__()
        self.no_category = "カテゴリ未設定"
        self.command_attrs["description"] = "このメッセージを表示します。"
        self.command_attrs["help"] = "このBOTのヘルプコマンドです。"

    async def create_category_tree(self, category, enclosure):
        """
        コマンドの集まり（Group、Cog）から木の枝状のコマンドリスト文字列を生成する。
        生成した文字列は enlosure 引数に渡された文字列で囲われる。
        """
        content = ""
        command_list = category.walk_commands()
        for cmd in await self.filter_commands(command_list, sort=True):
            if cmd.root_parent:
                # cmd.root_parent は「根」なので、根からの距離に応じてインデントを増やす
                index = cmd.parents.index(cmd.root_parent)
                indent = "\t" * (index + 1)
                if indent:
                    content += f"{indent}- {cmd.name} / {cmd.description}\n"
                else:
                    # インデントが入らない、つまり木の中で最も浅く表示されるのでprefixを付加
                    content += f"{self.context.prefix}{cmd.name} / {cmd.description}\n"
            else:
                # 親を持たないコマンドなので、木の中で最も浅く表示する。prefixを付加
                content += f"{self.context.prefix}{cmd.name} / {cmd.description}\n"

        return enclosure + textwrap.dedent(content) + enclosure

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="helpコマンド", color=0x5d00ff)
        if self.context.bot.description:
            # もしBOTに description 属性が定義されているなら、それも埋め込みに追加する
            embed.description = self.context.bot.description
            embed.add_field(name="サポート", value="https://discord.gg/uPbXyFh6")
        for cog in mapping:
            if cog:
                cog_name = cog.qualified_name
            else:
                # mappingのキーはNoneになる可能性もある
                # もしキーがNoneなら、自身のno_category属性を参照する
                cog_name = self.no_category

            command_list = await self.filter_commands(mapping[cog], sort=True)
            content = ""
            for cmd in command_list:
                content += f"`{cmd.name}` "
            embed.add_field(name=cog_name, value=content, inline=False)

        await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog):
        embed = discord.Embed(title=cog.quaylified_name, description=cog.description, color=0x00ff00)
        embed.add_field(name="コマンドリスト：", value=await self.create_category_tree(cog, "```"))
        await self.get_destination().send(embed=embed)

    async def send_group_help(self, group):
        embed = discord.Embed(title=f"{self.context.prefix}{group.qualified_name}",
                              description=group.description, color=0x00ff00)
        if group.aliases:
            embed.add_field(name="有効なエイリアス：", value="`" + "`, `".join(group.aliases) + "`", inline=True)
        if group.help:
            embed.add_field(name="必要な権限：", value=group.help, inline=True)
        embed.add_field(name="サブコマンドリスト：", value=await self.create_category_tree(group, "```"), inline=True)
        await self.get_destination().send(embed=embed)

    async def send_command_help(self, command):
        params = " ".join(command.clean_params.keys())
        embed = discord.Embed(title=f"{self.context.prefix}{command.qualified_name} {params}",
                              description=command.description, color=0x00ff00)
        if command.aliases:
            embed.add_field(name="有効なエイリアス：", value="`" + "`, `".join(command.aliases) + "`", inline=True)
        if command.help:
            embed.add_field(name="必要な権限：", value=command.help, inline=True)
        if command.name:
            embed.add_field(name="name", value=command.name, inline=True)

        await self.get_destination().send(embed=embed)

    async def send_error_message(self, error):
        embed = discord.Embed(title="ヘルプ表示のエラー", description=error, color=0xff0000)
        await self.get_destination().send(embed=embed)

    def command_not_found(self, string):
        return f"{string} というコマンドは存在しません。"

    def subcommand_not_found(self, command, string):
        if isinstance(command, commands.Group) and len(command.all_commands) > 0:
            # もし、そのコマンドにサブコマンドが存在しているなら
            return f"{command.qualified_name} に {string} というサブコマンドは登録されていません。"
        return f"{command.qualified_name} にサブコマンドは登録されていません。"


bot = commands.Bot(command_prefix="y/", help_command=Help(), description="```y/helps で調べられます``` ")

developer = f.bot_developers

bot.load_extension('ext.info')
bot.load_extension('ext.admin')
bot.load_extension('ext.other')
bot.load_extension('ext.moderation')
bot.load_extension('ext.report')
bot.load_extension('ext.fun')
bot.load_extension('ext.help')
bot.load_extension('jishaku')

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
async def on_ready():
    activity = discord.Game(name="y/helps", type=3)
    await bot.change_presence(status=discord.Status.idle, activity=activity)
    print("Bot is ready!")


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