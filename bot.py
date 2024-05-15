import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
import json
from app import keep_alive 

with open(file="city_data.json", mode='r') as file:
    data = json.load(file)
    CITIES_LIST = data["cities"]

class AstroBot(commands.Bot):
    def __init__(self):
        #super().__init__(command_prefix='$' ,intents = self.intents)

        # Pinging and city configuration
        self.curr_city = str()
        self.ping = False

        # Call the setup method
        self.setup()

    def setup(self):
        # Load environment variables from 'sec.env' file
        load_dotenv()

        # Get bot token from environment variable
        self.TOKEN = os.getenv("TOKEN")

        # Define intents
        self.intents = discord.Intents.default()
        self.intents.messages = True  # Enable message-related events
        self.intents.message_content = True  # enable message content reading 

        # Create a bot instance with intents
        self.client = discord.Client(intents=self.intents)
    @property
    def intents(self):
        return self._intents

    @intents.setter
    def intents(self, value):
        self._intents = value
    async def on_ready(self):
        print('Logged in as {0.user}'.format(self.client))

    async def on_message(self, message):
        if message.author == self.client.user:
            return

        print(f"Received message: '{message.content}'")

        if message.content.startswith('$hello'):
            await message.channel.send('Hello!')

        elif message.content.startswith('$bye'):
            await message.channel.send('Goodbye!')
        elif message.content.startswith('$home'):
            await self.home(message)
        elif message.content.lower().startswith("$curr_city"):
            await self.display_curr_city(message=message)
        elif message.content.lower().startswith("$avail_city"):
            await self.available_cities(message=message)
        elif message.content.lower().startswith("$set_city"):
            await self.set_city(message=message)
        elif message.content.lower().startswith("$project_info"):
            await self.project_info(message=message)
        elif message.content.startswith('$embed'):
            await self.send_embed(message)

    async def home(self, message):
        # Embedded message contents
        embed = discord.Embed(
            title="Astro Alert 🛰",
            description="Did someone call me ? 🧐",
            color=discord.Color.dark_magenta()
        )
        embed.add_field(
            name="About",
            value="Hi i am a Celestial Bot who will spam you when International Space Station (ISS) will be over your city.",
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

    async def display_curr_city(self, message):

        print(self.curr_city)

        if self.curr_city is None or self.curr_city == "":
            description = "**No configuration found**. Please configure the bot to start using it. Refer the below help doc to configure it."
        else:
            description = f"The current city is set to: **{self.curr_city}**"

        embed = discord.Embed(
            title="Current city",
            description=description,
            color=discord.Color.yellow()
        )

        await message.channel.send(embed=embed)

        if self.curr_city is None or self.curr_city == "":
            await self.home(message=message)

    async def set_city(self, message):
       #assuming there exists a space
        if message.content.split(" ")[1] in CITIES_LIST:
            self.curr_city = message.content.split(" ")[1]
            await self.curr_city_display(message=message)

        else:
            await self.show_error(message=message, text=f'No city named: **{message.content.split(" ")[1]}** in database.')
            await self.available_cities(message=message)

    async def stop_ping(self, message):
        pass

    @staticmethod
    async def available_cities(message):

        cities = ', '.join(CITIES_LIST)

        embed = discord.Embed(
            title="Available Cities",
            description=f"Names of cities available in the database are: {cities}.",
            color=discord.Color.blue()
        )

        await message.channel.send(embed=embed)

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
        embed = discord.Embed(
            title="Project Info",
            description=f"Find the project at: https://github.com/scienmanas",
            color=discord.Color.pink()
        )

        await message.channel.send(embed=embed)

    def run(self):
        @self.client.event
        async def on_ready():
            await self.on_ready()

        @self.client.event
        async def on_message(message):
            await self.on_message(message)

        # Run the bot with the token from the environment variable
        self.client.run(self.TOKEN)

# Example Usage:
if __name__ == "__main__":
    bot = AstroBot()
    keep_alive()
    bot.run()
