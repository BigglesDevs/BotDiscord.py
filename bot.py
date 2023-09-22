# Import necessary libraries and modules
import discord
from discord.ext import commands, tasks
from itertools import cycle
import os
import asyncio
from dotenv import load_dotenv
import json

# Load environment variables from .env
load_dotenv()

# Get the bot token from the environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_OWNER_ID = int(os.getenv("BOT_OWNER_ID"))

# Define the bot prefix
bot_prefix = "~"

# Create an instance of the bot
client = commands.Bot(command_prefix=bot_prefix, intents=discord.Intents.all())

# Define the bot's activity status using an iterator cycling through different statuses
bot_status = cycle(["type ~help", "code by BigglesDevs", "With a Magic 8-Ball", "https://bigglesdevelopment.com", "coded with python"])

# Task: Status - loop to update the bot's activity status
@tasks.loop(seconds=15)
async def change_status():
    try:
        await client.change_presence(activity=discord.Game(next(bot_status)))
    except Exception as e:
        print(f"Error changing status: {e}")

# Event: Bot is ready - this event is triggered when the bot successfully connects to Discord
@client.event
async def on_ready():
    try:
        await client.tree.sync()
        print(f'Success: {client.user.name} is connected to Discord! 😁👍')
        # Start the change_status loop to update the bot's activity status
        change_status.start()
    except Exception as e:
        print(f"Error in on_ready: {e}")

# Function to load cogs (extensions)
async def load():
    try:
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                # Load each cog by adding it to the bot
                await client.load_extension(f"cogs.{filename[:-3]}")
    except Exception as e:
        print(f"Error loading cogs: {e}")

@client.event
async def on_guild_join(guild):
    try:
        with open("cogs/json/autorole.json","r") as f:
            auto_role = json.load(f)

        auto_role[str(guild.id)] = None

        with open("cogs/json/autorole.json","w") as f:
            json.dump(auto_role, f, indent=4)
    except Exception as e:
        print(f"Error in on_guild_join: {e}")

@client.event
async def on_guild_remoive(guild):
    try:
        with open("cogs/json/autorole.json","r") as f:
            auto_role = json.load(f)

        auto_role.pop(str(guild.id)) 

        with open("cogs/json/autorole.json","w") as f:
            json.dump(auto_role, f, indent=4)
    except Exception as e:
        print(f"Error in on_guild_remove: {e}")

# Main function
async def main():
    try:
        # Create an async context for the client
        async with client:
            # Load cogs (extensions)
            await load()
            # Start the bot with the provided BOT_TOKEN from environment variables
            await client.start(BOT_TOKEN)
    except Exception as e:
        print(f"Error in main: {e}")

# Run the main function when this script is executed
if __name__ == "__main__":
    asyncio.run(main())
