import discord
from discord import app_commands
from discord.ext import commands
import os

class RememberCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.tree.sync()
        print(f"{__name__} loaded successfully!")

    @app_commands.command(name="remember", description="give the bot something to remember")
    async def remember(self, interaction: discord.Interaction, to_remember: str):
        user_id = str(interaction.user.id)

        if not os.path.exists("discord_storage_not_encrypted/" + user_id + ".txt"):
            with open("discord_storage_not_encrypted/" + user_id + ".txt", "w") as file:
                file.write("")
        file = open("discord_storage_not_encrypted/" + user_id + ".txt", "r")
        lines = file.readlines()
        file.close()
        if len(lines) == 0:
            with open("discord_storage_not_encrypted/" + user_id + ".txt", "a") as f:
                f.write(to_remember)
            await interaction.response.send_message(f"I have remembered: {to_remember}")
            return
        if len(lines) > 0:
            lines[0] = to_remember
            with open("discord_storage_not_encrypted/" + user_id + ".txt", "w") as f:
                for line in lines:
                    f.write(line)
            await interaction.response.send_message(f"I have remembered: {to_remember}")
            return






async def setup(client):
    await client.add_cog(RememberCommand(client))