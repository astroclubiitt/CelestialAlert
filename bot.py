import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import os
import json
from app import keep_alive
import datetime

# Load the environment variables
load_dotenv()

# Get bot token from environment variable
DISCORD_BOT_TOKEN = os.getenv("TOKEN")

# Get all cities from the JSON file
with open(file="city_data.json", mode='r') as file:
    data = json.load(file)
    CITIES_AVAILABLE = data["cities"]

# Custom Bot class inheriting from commands.Bot
class CelestialAlert(commands.Bot):
    def __init__(self):
        # Initialize bot with custom intents
        intents = discord.Intents.default()
        intents.messages = True
        intents.message_content = True
        super().__init__(command_prefix='$', intents=intents)

        # Initialize variables
        self.curr_city = str()  # Current city the bot is configured for
        self.ping = False  # Flag to indicate whether the bot is currently pinging
        self.min_latitude = float()  # Minimum latitude for the current city
        self.max_latitude = float()  # Maximum latitude for the current city
        self.min_longitude = float()  # Minimum longitude for the current city
        self.max_longitude = float()  # Maximum longitude for the current city

        # Date, time logs object
        self.data_time_object = datetime.datetime

    async def on_ready(self):
        print("We have logged in as {0.user}".format(self))

    async def on_message(self, message):
        # Ignore if the message is from the bot itself
        if message.author == self.user:
            return

        # Handle different commands
        if message.content.lower().startswith('$home') or message.content.lower().startswith("$help"):
            await self.home(message=message)

        elif message.content.lower().startswith("$curr_city"):
            await self.curr_city_display(message=message)

        elif message.content.lower().startswith("$avail_city"):
            await self.available_cities(message=message)

        elif message.content.lower().startswith("$set_city"):
            await self.set_city(message=message)

        elif message.content.lower().startswith("$project_info"):
            await self.project_info(message=message)

        elif message.content.lower().startswith("$bot_config"):
            await self.display_bot_configuration(message=message)

        elif message.content.lower().startswith("$stop_ping"):
            await self.stop_ping(message=message)

        elif message.content.lower().startswith("$start_ping"):
            await self.start_ping(message=message)

        elif message.content.lower().startswith("$update_city"):
            await self.update_city(message=message)

    async def home(self, message):
        # Embedded message contents
        embed = discord.Embed(
            title="Celestial Alert 🛰",
            description="Did someone called me ? 🧐",
            color=discord.Color.dark_magenta()
        )
        embed.add_field(
            name="About",
            value="Hi! I am an Celestial Bot who informs you when the International Space Station (ISS) will be over your city.",
            inline=False
        )
        embed.add_field(
            name="Commands",
            value="To operate me, use **$<command>**\n"
                  "- **$home/help**: To go to home.\n"
                  "- **$curr_city**: gives current configured city.\n"
                  "- **$avail_city**: list all available cities.\n"
                  "- **$set_city <city>**: to set the city.\n"
                  "- **$project_info**: get project information.\n"
                  "- **$bot_config**: display bot configuration.\n"
                  "- **$stop_ping**: to pause the bot from pinging.\n"
                  "- **$update_city**: To update the city",
            inline=False
        )
        embed.set_footer(
            text="This bot was developed by Gagan Vedhi Team [Ikshitha (GV-23) coordinated by Manas]"
        )

        # Send the message
        await message.channel.send(embed=embed)

    async def curr_city_display(self, message):
        # Display the current configured city
        if self.curr_city is None or self.curr_city == "":
            description = "**No configuration found**. Please configure the bot to start using it. " \
                          "Refer the below help doc to configure it."
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

    @staticmethod
    async def available_cities(message):
        # Display the list of available cities
        cities = ', '.join(CITIES_AVAILABLE)

        embed = discord.Embed(
            title="Available Cities",
            description=f"Names of cities supported are: {cities}.",
            color=discord.Color.dark_green()
        )

        await message.channel.send(embed=embed)

    async def set_city(self, message):
        # Set the current city
        if self.curr_city is not None and self.curr_city != "":
            await self.show_error(message=message, text="City already configured, to update use **$update_city** command.")
            await self.display_bot_configuration(message=message)
            return

        if message.content.split(" ")[1] in CITIES_AVAILABLE:
            # Configure city
            self.curr_city = message.content.split(" ")[1]
            self.configure_latitude_and_longitude(city=self.curr_city)
            await self.curr_city_display(message=message)

            # Start Pinging the API
            await self.start_ping(message=message)

        else:
            await self.show_error(message=message, text=f'No city named: **{message.content.split(" ")[1]}** in database.')
            await self.available_cities(message=message)

    async def update_city(self, message):
        # Update the current city
        if self.curr_city is None or self.curr_city == "":
            await self.show_error(message=message, text="**No configuration found**. Please configure the bot by **$set_city <city>**.")
            await self.available_cities(message=message)
            return

        city = message.content.split(" ")[1]

        if city in CITIES_AVAILABLE:
            # Instantaneously stop current ping
            self.ping = False

            # Change the configuration
            self.curr_city = message.content.split(" ")[1]
            self.configure_latitude_and_longitude(self.curr_city)

            # Start pinging again after configuration is updated
            self.ping = True

            # Embedded message
            embed = discord.Embed(
                title="Settings Update.",
                description=f"City to be pinged changed to **{self.curr_city}**.",
                color=discord.Colour.magenta()
            )
            await message.channel.send(embed=embed)

        else:
            await self.show_error(message=message, text=f'No city named: **{city}** in database. Settings not updated.')
            await self.display_bot_configuration(message=message)
            await self.available_cities(message=message)

    async def display_bot_configuration(self, message):
        # Display the current bot configuration
        if self.curr_city is None or self.curr_city == "":
            city = "None"
        else:
            city = self.curr_city

        embed = discord.Embed(
            title="Bot Configuration",
            description=f"- **Current city**: {city}\n"
            f"- **Ping status**: {self.ping}",
            color=discord.Color.blurple()
        )

        await message.channel.send(embed=embed)

    async def start_ping(self, message):
        # Start pinging the API
        if self.curr_city is None or self.curr_city == "":
            await self.show_error(message=message, text=f'**No configuration found**, please set the city by using **$set_city <city>**. '
                                  f'To view list of cities: **$avail_city**, and for help: **$help**')
            return

        elif self.ping is True:
            await self.show_error(message=message, text="Bot is already **running**")
            await self.display_bot_configuration(message=message)
            return

        # Start the ping
        self.ping = True
        self.ping_api.start()
        print("Ping Started")
        await self.ping_message_template(message=message, text="**Ping started**. The bot is currently **active**.", color=discord.Color.brand_green())

    async def stop_ping(self, message):
        # Stop pinging the API
        if self.ping is False:
            await self.show_error(message=message, text="Bot is already **off**")
            await self.display_bot_configuration(message=message)
            return

        self.ping = False
        self.ping_api.stop()
        print("Ping stopped")
        await self.ping_message_template(message=message, text="**Ping Stopped**. The bot is currently **inactive**.", color=discord.Color.light_gray())

    @staticmethod
    async def ping_message_template(message, text, color):
        # Template for ping messages
        embed = discord.Embed(
            title="Update",
            description=text,
            color=color
        )
        await message.channel.send(embed=embed)

    @tasks.loop(seconds=2)
    async def ping_api(self):
        # Loop for pinging the API
        if self.ping is True :

            # Note time for ping - for logs
            now = self.data_time_object.now()
            date_str = now.strftime("%d-%m-%Y")
            time_str = now.strftime("%I:%M:%S %p")
            print(f"Pinged: {self.curr_city}, on: {date_str}, at time: {time_str}")

    @staticmethod
    async def send_alert(message):
        # Send alert message about ISS passing
        embed = discord.Embed(
            title="Look up at the sky 😲",
            description=f"@everyone The **International Space Station** (ISS) is passing above the city. Grab your equipment and take a look! 😅.",
            color=discord.Color.dark_gold()
        )
        await message.channel.send(embed=embed)

    @staticmethod
    async def show_error(message, text):
        # Display error message
        embed = discord.Embed(
            title="Error",
            description=text,
            color=discord.Color.brand_red()
        )
        await message.channel.send(embed=embed)

    @staticmethod
    async def project_info(message):
        # Display project information
        await message.channel.send(f"Find the project at: https://github.com/scienmanas")

    def configure_latitude_and_longitude(self, city):
        # Configure latitude and longitude for the given city
        with open(file="city_data.json", mode='r') as file:
            data = json.load(file)

            self.min_latitude = data[city]["latitude"]["min"]
            self.max_latitude = data[city]["latitude"]["max"]

            self.min_longitude = data[city]["longitude"]["min"]
            self.max_longitude = data[city]["longitude"]["max"]

# Entry point of the program
def main():
    celestial_alert = CelestialAlert()
    keep_alive()  # Keep the bot alive
    celestial_alert.run(DISCORD_BOT_TOKEN)

# Call the main function
main()
