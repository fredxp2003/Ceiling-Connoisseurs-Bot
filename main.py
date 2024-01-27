import discord
import os 
from dotenv import load_dotenv
import random

# Local imports
from database import *

load_dotenv()
intents = discord.Intents.default()
intents.members = True
bot = discord.Bot(intents=intents)

DB_NAME = 'premium_ceiling.db'
PREMIUM_CEILING_CHANNEL_ID = 1150273041406890065
BAD_CEILING_CHANNEL_ID = 1149113000465285231
ROLE_MESSAGE_ID = 1165779240659198072
DEBATES_ROLE_NAME = "Debates"


good_ceiling_phrases = [
    "PREMIUM CEILING ALERT!!", "Wow, what a ceiling!",
    "Now *that's* what I call a ceiling!","*chef's kiss*",
    "This ceiling is so good, it's making me cry!",
    "Such beauty!  Such grace!  Such a ceiling!",
    "I'm not crying, you're crying!  It's just such a good ceiling!",
    "If I had a dollar for every time a ceiling made me think of the beauty of life, I would have lots of dollars.  But I would have one more right now!"
]

setup_database(DB_NAME)

# Load all the cogs
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        print(f'Loaded {filename[:-3]}')

### Bot Events and Commands ###
@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Dancing on the Ceiling by Lionel Richie"))

@bot.event
async def on_raw_reaction_add(payload):
    if payload.emoji.name == "🔥" or payload.emoji.name == "😔":
        channel = bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        pictures = []
        guild_id = message.guild.id
        channel_id = message.channel.id
        message_id = message.id
        link = f"https://discord.com/channels/{guild_id}/{channel_id}/{message_id}"
        
        # Get all the images in the message and save them to a list
        for attachment in message.attachments:
            pictures.append(await attachment.to_file())
        
        if message.attachments and not is_posted(message_id):
            for reaction in message.reactions:
                
                # Premium Ceiling Gang
                if reaction.emoji == "🔥" and reaction.count == 12:
                    premium_channel = bot.get_channel(PREMIUM_CEILING_CHANNEL_ID)
                    
                    await premium_channel.send(f"{random.choice(good_ceiling_phrases)}\n\n{link}\n\nTake a look at this fine ceiling provided by {message.author}:", files=pictures)
                    insert_message_id(message_id) # add the message id to the database so we don't post it again
                    
                    # Send a dm to the user who posted the ceiling
                    await message.author.send(f"Congratulations, your ceiling made premium status! If you would like us to share a short ~30 second story about this ceiling at the next meeting, please share the story! You will also have the opportunity to share it yourself if you come to the next meeting :-)\n\nJust fill out the [Google Form](https://forms.gle/hv5CD9bWpYq71EDB7)!  [Ceiling we are talking about]({link})]")
                
                # Bad Ceilings
                if reaction.emoji == "😔" and reaction.count == 12:
                    bad_channel = bot.get_channel(BAD_CEILING_CHANNEL_ID)
                    await bad_channel.send(f"TRIGGER WARNING: BAD CEILING ALERT\n\n{link}\n\nHelp shame this bad ceiling provided by {message.author}:", files=pictures)
                    insert_message_id(message_id) # add the message id to the database so we don't post it again
     
    #Debates Role
    role_message = await bot.get_channel(payload.channel_id).fetch_message(ROLE_MESSAGE_ID)
    reaction = discord.utils.get(role_message.reactions, emoji="📣")
    user = payload.member
    if reaction and user != bot.user:
        await user.add_roles(discord.utils.get(user.guild.roles, name="Debates"))

@bot.event
async def on_raw_reaction_remove(payload):
    print("Reaction removed event triggered.") 

    # Check if the message is the one we're interested in
    if payload.message_id != ROLE_MESSAGE_ID:
        print("Removed reaction is not on the message we're interested in.")
        return

    # Check if the emoji is 📣
    if str(payload.emoji) != "📣":
        print("Emoji is not the one we're interested in.")
        return
    
    # Make sure that the reactor isn't the bot
    if payload.user_id == bot.user.id:
        print("Reaction was removed by the bot.")
        return

    # Get the Discord server (guild) and member member info
    guild = discord.utils.get(bot.guilds, id=payload.guild_id)    
    member = guild.get_member(payload.user_id)
    if not member:
        print("Couldn't find the member.")
        return  

    # Get the Debates role
    role = discord.utils.get(guild.roles, name=DEBATES_ROLE_NAME)
    if not role:
        print("Couldn't find the role.")
        return

    await member.remove_roles(role)

# Run the bot B)
bot.run(os.getenv('TOKEN'))