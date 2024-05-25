import discord
from discord.ext import commands
from database import *
import asyncio

class Leaderboard(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def get_usernames(self, bot, user_ids):
        return await asyncio.gather(*[bot.fetch_user(user_id) for user_id in user_ids])

    @discord.slash_command(name = "leaderboard", description = "Returns the top 5 users with the most premium ceilings.")
    async def leaderboard(self, ctx):
        top_users = get_top_users()
        if isinstance(top_users, str):
            await ctx.respond(f"An error occurred while getting the top users. {top_users}")
        else:
            if top_users:
                user_ids = [user[0] for user in top_users]
                users = await self.get_usernames(self.bot, user_ids)
                leaderboard_text = "\n".join([f"{i+1}. {user.name if user else 'Unknown User'} - {count} premium ceiling(s)" for i, (user, count) in enumerate(zip(users, [user[1] for user in top_users]))])  # I straight up do not know how or why this works.  ChatGPT is a gift.
                await ctx.respond(f"# Premium Ceiling Leaderboard\n\n{leaderboard_text}")
            else:
                await ctx.respond("No users have posted any premium ceilings yet.")

    @discord.slash_command(name = "status", description = "Returns how many premium ceilings have been posted by the user.")
    # This command needs to be passed with a user mentioned
    async def status(self, ctx, user: discord.Member):
        user_id = user.id

        count = get_premium_ceiling_count(user_id)
        await ctx.respond(f"{user.name} has posted {count} premium ceiling(s).")


def setup(bot):
    bot.add_cog(Leaderboard(bot))