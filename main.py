import discord
import os 
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.default()
intents.members = True
bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Dancing on the Ceiling by Lionel Richie"))

@bot.slash_command(name = "ping", description = "Returns the bot's latency")
async def ping(ctx):
    await ctx.respond(f"Pong!  Latency: {round(bot.latency * 1000)}ms")

@bot.slash_command(name = "debate", description = "Starts a new debate")
async def debate(ctx, question: discord.Option(str)):
    debate_role = discord.utils.get(ctx.guild.roles, name="Debates")

    embed = discord.Embed(
        title=f"{question}",
        description=f"React with 👍 or 👎 to vote!  Share your insight by messaging in the thread attached to this message.  Please don't get too political about it.",
        color=discord.Colour.dark_purple()
    )

    message = await ctx.send(f"{debate_role.mention} A new debate has started!", embed=embed)
    await message.create_thread(name=f"{question}", auto_archive_duration=60)
    await message.add_reaction("👍")
    await message.add_reaction("👎") 

@bot.event
async def on_raw_reaction_add(payload):
    # Premium Ceiling Gang
    if payload.emoji.name == "⭐":
        channel = bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        
        if message.attachments:
            for reaction in message.reactions:
                if reaction.emoji == "⭐" and reaction.count == 10:
                    target_channel = bot.get_channel(1150273041406890065)
                    picture = await message.attachments[0].to_file()
                    await target_channel.send(f"PREMIUM CEILING ALERT\n\n Take a look at this fine ceiling provided by {message.author.mention}:", file=picture)
    
    #Debates Role
    role_message = await bot.get_channel(payload.channel_id).fetch_message(1165779240659198072)
    reaction = discord.utils.get(role_message.reactions, emoji="📣")
    user = payload.member
    if reaction and user != bot.user:
        await user.add_roles(discord.utils.get(user.guild.roles, name="Debates"))

@bot.event
async def on_raw_reaction_remove(payload):
    print("Reaction removed event triggered.") 

    if payload.message_id != 1165779240659198072:
        print("Reaction is not on the message we're interested in.")
        return

    if str(payload.emoji) != "📣":
        print("Emoji is not the one we're interested in.")
        return
    
    # Make sure that the reactor isn't the bot
    if payload.user_id == bot.user.id:
        print("Reaction was removed by the bot.")
        return

    guild = discord.utils.get(bot.guilds, id=payload.guild_id)    
    member = guild.get_member(payload.user_id)
    if not member:
        print("Couldn't find the member.")
        return  

    role = discord.utils.get(guild.roles, name="Debates")
    if not role:
        print("Couldn't find the role.")
        return

    await member.remove_roles(role)

bot.run(os.getenv('TOKEN'))
