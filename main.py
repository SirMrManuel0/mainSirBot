# Import required libraries and modules
import discord
from discord import app_commands
from discord.ext import commands
from credentials import apiToken  # Import your API token from credentials.py
import asyncio
import os

# Create a Discord bot instance with a custom command prefix and all intents enabled
client = commands.Bot(command_prefix="$", intents=discord.Intents.all())


# Define an event handler for when the bot is ready
@client.event
async def on_ready():
    print(f"#" * 20)
    print("Success: Bot is connected to Discord!")
    print(f"#" * 20)

# Function to load bot extensions (cogs)
async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            print(filename)
            await client.load_extension(f"cogs.{filename[:-3]}")


# Main asynchronous function to run the bot
async def main():
    async with client:
        await load()  # Load bot extensions
        await client.start(apiToken.discord_token)  # Start the bot using the provided token

# Start the bot and handle KeyboardInterrupt to gracefully shut down
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("#" * 50 + "\nBot is offline!")