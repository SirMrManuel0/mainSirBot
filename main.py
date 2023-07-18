import discord
from discord import app_commands
from discord.ext import commands
from credentials import apiToken
import asyncio
import os


client = commands.Bot(command_prefix="$", intents=discord.Intents.all())

@client.event
async def on_ready():
    print("Success: Bot is connected to Discord!")

async  def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with client:
        await load()
        await client.start(apiToken.discord_token)

asyncio.run(main())