import discord
from discord.ext import commands

class General(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name = "ping", description = "Returns the bot's latency")
    async def ping(self, ctx):
        await ctx.respond(f"Pong!  {round(self.bot.latency * 1000)}ms")

    @discord.slash_command(name = "version", description = "Returns the bot's version and change log.")
    async def version(self, ctx):
        embed = discord.Embed(
            title="Version 1.1.1",
            description="Changes in this version:\n- Increased the number of 🔥 reactions needed to get a premium ceiling from 10 -> 12.\n- Created a new way to get info about premium ceilings from users.\n- Added new premium ceiling phrases.\n- Fixed a bug where the bot would post the same ceiling multiple times.\nNew in 1.1.1:\n- Removed ping in premium-ceiling announcement.",
            color=discord.Colour.dark_purple()
        )

        await ctx.respond(embed=embed)

    @discord.slash_command(name = "help", description = "Returns a list of commands")
    async def help(self, ctx):
        embed = discord.Embed(
            title="Commands",
            description="Here is a list of commands:",
            color=discord.Colour.dark_purple()
        )

        embed.add_field(name="/ping", value="Returns the bot's latency", inline=False)
        embed.add_field(name="/version", value="Returns the bot's version and change log", inline=False)
        embed.add_field(name="/debate", value="(admin) Starts a new debate", inline=False)
        embed.add_field(name="/debate_no_vote", value="(admin) Starts a new debate, but without the voting.  This encourages discussion.", inline=False)
        embed.add_field(name="/help", value="Returns a list of commands", inline=False)

        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(General(bot))
