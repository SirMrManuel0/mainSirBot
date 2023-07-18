import discord
from discord import app_commands
from discord.ext import commands
from credentials import apiToken


bot = commands.Bot(command_prefix="$", intents=discord.Intents.all())

@bot.event
async def on_ready():
    await bot.tree.sync()

@bot.tree.command(name="ping", description="Sends the bot's latency in ms.")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! {round(bot.latency) * 1000}ms.")



bot.run(apiToken.discord_token)
