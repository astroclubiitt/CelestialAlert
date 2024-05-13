import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from app import keep_alive
import json

# Load the environment variables
load_dotenv()

# Get bot token from environment variable
DISCORD_BOT_TOKEN = os.getenv("TOKEN")
# Get all cities
with open(file="city_data.json", mode='r') as file:
    data = json.load(file)
    CITIES_AVAILABLE = data["cities"]


class CeletialALert(commands.Bot):
    def __init__(self):
        # Define intents
        intents = discord.Intents.default()
        intents.messages = True  # This is needed for the on_message event
        intents.message_content = True   # Needed to get the messages
        super().__init__(command_prefix='$', intents=intents)

        # Pinging and city configuration
        self.curr_city = str()
        self.ping = False

    async def on_ready(self):
        print("We have logged in as {0.user}".format(self))

    async def on_message(self, message):
        # Ignore if the message is from the bot itself
        if message.author == self.user:
            return

        # Handle different cases
        if message.content.lower().startswith('$home'):
            await self.home(message=message)

        elif message.content.lower().startswith("$curr_city"):
            await self.curr_city_display(message=message)

        elif message.content.lower().startswith("$avail_city"):
            await self.available_cities(message=message)

        elif message.content.lower().startswith("$set_city"):
            await self.set_city(message=message)

        elif message.content.lower().startswith("$project_info"):
            await self.project_info(message=message)

    async def home(self, message):

        # Embedded message contents
        embed = discord.Embed(
            title="Celestial Alert 🛰",
            description="Did someone called me ? 🧐",
            color=discord.Color.dark_magenta()
        )
        embed.add_field(
            name="About",
            value="Hi i am an Celetial Bot who spam you when International Space Station (ISS) will be over your city.",
            inline=False
        )
        embed.add_field(
            name="Command",
            value="To operate me, use **$<command>**\n- **$home**: To go to home\n- **$curr_city**: gives current configured city\n- **$avail_city**: list all available cities\n- **$set_city <city>**: to set the city\n- **$project_info**: get project information",
            inline=False
        )
        embed.set_footer(
            text="This fellow(bot) was developed by Gagan Vedhi Team [Ikshitha (GV-23) coordinated by Manas]"
        )

        # Send the message
        await message.channel.send(embed=embed)

    async def curr_city_display(self, message):

        print(self.curr_city)

        if self.curr_city is None or self.curr_city == "":
            description = "**No configuration found**. Please configure the bot to start using it. Refer the below help doc to configure it."
        else:
            description = f"The current city is set to: **{self.curr_city}**"

        embed = discord.Embed(
            title="Currect city",
            description=description,
            color=discord.Color.yellow()
        )

        await message.channel.send(embed=embed)

        if self.curr_city is None or self.curr_city == "":
            await self.home(message=message)

    @staticmethod
    async def available_cities(message):

        cities = ', '.join(CITIES_AVAILABLE)

        embed = discord.Embed(
            title="Available Cities",
            description=f"Names of cities supported are: {cities}.",
            color=discord.Color.dark_green()
        )

        await message.channel.send(embed=embed)

    async def set_city(self, message):

        if message.content.split(" ")[1] in CITIES_AVAILABLE:
            self.curr_city = message.content.split(" ")[1]
            await self.curr_city_display(message=message)

        else:
            await self.show_error(message=message, text=f'No city named: **{message.content.split(" ")[1]}** in database.')
            await self.available_cities(message=message)

    async def stop_ping(self, message):
        pass

    @staticmethod
    async def show_error(message, text):

        embed = discord.Embed(
            title="Error",
            description=text,
            color=discord.Color.brand_red()
        )

        await message.channel.send(embed=embed)

    @staticmethod
    async def project_info(message):

        # To be update
        await message.channel.send(f"Find the project at: https://github.com/scienmanas")


def main():
    celetial_alert = CeletialALert()
    keep_alive()
    celetial_alert.run(DISCORD_BOT_TOKEN)


main()
