from contextlib import redirect_stdout
import re
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="y/")


class report(commands.Cog, name="report"):
    """```
    report関係
    ```"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="request", description="```リクエスト募集してます```")
    async def request(self, ctx, arg, *, arg2):
        """`誰でも`"""
        async with ctx.typing():
            channel = bot.get_channel(777133930532306984)
            server = ctx.guild
            embed = discord.Embed(title="要望", description=f"```\n提案:\n{arg}```\n```理由:\n{arg2}\n```", color=0x0066ff)

            embed.set_author(name=ctx.message.author.name,
                             icon_url=ctx.message.author.avatar_url_as(format="png"))
            embed.add_field(name="**id**", value=ctx.message.author.id)
            embed.add_field(name="**server**", value=server.name)
            await channel.send(embed=embed)
        await ctx.send("ご協力ありがとうございます。")

    @commands.command(name="bug", description="```バグがあれば報告お願いします```")
    async def bug(self, ctx, arg):
        """`誰でも`"""
        async with ctx.typing():
            channel = bot.get_channel(777133930532306984)
            server = ctx.guild
            embed = discord.Embed(title="バグ", description=f"```\n不具合:\n{arg}\n```", color=0x0066ff)

            embed.set_author(name=ctx.message.author.name,
                             icon_url=ctx.message.author.avatar_url_as(format="png"))
            embed.add_field(name="**id**", value=ctx.message.author.id)
            embed.add_field(name="**server**", value=server.name)
            await channel.send(embed=embed)
        await ctx.send("ご協力ありがとうございます。")

    @commands.command()
    async def feedback(self, ctx, *, content: str):
        e = discord.Embed(title='Feedback', colour=0x738bd7)
        channel = self.bot.get_channel(759386170689585216)
        if channel is None:
            return

        e.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
        e.description = content
        e.timestamp = ctx.message.created_at

        if ctx.guild is not None:
            e.add_field(name='Server', value=f'{ctx.guild.name} (ID: {ctx.guild.id})', inline=False)

        e.add_field(name='Channel', value=f'{ctx.channel} (ID: {ctx.channel.id})', inline=False)
        e.set_footer(text=f'Author ID: {ctx.author.id}')

        await channel.send(embed=e)
        await ctx.send(f'{ctx.tick(True)} Successfully sent feedback')


def setup(bot):
    bot.add_cog(report(bot))