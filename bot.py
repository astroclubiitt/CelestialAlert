import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

# Load the environment variables
load_dotenv()

# Get bot token from environment variable
DISCORD_BOT_TOKEN = os.getenv("TOKEN")

# Define intents
intents = discord.Intents.default()
intents.messages = True  # This is needed for the on_message event
intents.message_content = True   # Needed to get the messages

# Connection with the discord
client = commands.Bot(command_prefix='$', intents=intents)

# Register an event
@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    # Ignore if the message is from the bot itself
    if message.author == client.user:
        return

    if message.content.lower().startswith('$hello'):
        await message.channel.send('Hello!')



# Run the Bot
client.run(DISCORD_BOT_TOKEN)
