import discord
import os
from dotenv import load_dotenv

# Load environment variables from 'sec.env' file
load_dotenv('sec.env')

# Get bot token from environment variable
TOKEN = os.getenv("TOKEN")

# Define intents
intents = discord.Intents.default()
intents.messages = True  # Enable message-related events
intents.message_content = True   # enable message content reading 

# Create a bot instance with intents
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    print(f"Received message: '{message.content}'")

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$bye'):
        await message.channel.send('Goodbye!')

# Run the bot with the token from the environment variable
client.run(TOKEN)