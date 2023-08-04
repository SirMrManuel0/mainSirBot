import discord
from discord import app_commands
from discord.ext import commands
from credentials import apiToken
import asyncio
import os


client = commands.Bot(command_prefix="$", intents=discord.Intents.all())

@client.event
async def on_ready():
    print(f"#" * 20)
    print("Success: Bot is connected to Discord!")
    print(f"#" * 20)

async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            print(filename)
            await client.load_extension(f"cogs.{filename[:-3]}")


async def main():
    async with client:
        await load()
        await client.start(apiToken.discord_token)

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("#" * 50 + "\nBot is offline!")