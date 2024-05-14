# Task - 3

#TODO-1: Change the whole thing to a class for better management if variables (check T-3 for it)
#TODO-2: Push the code, and then I will tell you which function you need to make, so this is partial T-3 completion task. 


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