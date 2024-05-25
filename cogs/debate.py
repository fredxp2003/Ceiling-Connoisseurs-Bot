import discord
from discord.ext import commands

DEBATES_ROLE_NAME = "Debates"

class Debate(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name = "debate", description = "Starts a new debate")
    async def debate(self, ctx, question: discord.Option(str)):
        debate_role = discord.utils.get(ctx.guild.roles, name=DEBATES_ROLE_NAME)

        embed = discord.Embed(
            title=f"{question}",
            description=f"React with 👍 or 👎 to vote!  Share your insight by messaging in the thread attached to this message.",
            color=discord.Colour.dark_purple()
        )

        message = await ctx.send(f"{debate_role.mention} A new debate has started!", embed=embed)
        await message.create_thread(name=f"{question}", auto_archive_duration=60)
        await message.add_reaction("👍")
        await message.add_reaction("👎")

    @discord.slash_command(name = "debate_no_vote", description = "Starts a new debate, but without the voting.  This encourages discussion.")
    async def debate_no_vote(self, ctx, question: discord.Option(str)):
        debate_role = discord.utils.get(ctx.guild.roles, name=DEBATES_ROLE_NAME)

        embed = discord.Embed(
            title=f"{question}",
            description=f"No vote here.  This is more of a discussion question.  Share your insight by messaging in the thread attached to this message.",
            color=discord.Colour.dark_purple()
        )

        message = await ctx.send(f"{debate_role.mention} A new debate has started!", embed=embed)
        await message.create_thread(name=f"{question}", auto_archive_duration=60)

def setup(bot):
    bot.add_cog(Debate(bot))