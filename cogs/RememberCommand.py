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
    async def remember(self, interaction: discord.Interaction, to_remember: str, name: str=None):
        user_id = str(interaction.user.id)

        if not os.path.exists("discord_storage_not_encrypted/" + user_id + ".txt") and name is None:
            with open(f"discord_storage_not_encrypted/{user_id}.txt", "w") as file:
                file.write(to_remember)
            await interaction.response.send_message(f"I have remembered: {to_remember}.")
            return
        elif not os.path.exists(f"discord_storage_not_encrypted/{user_id}.txt"):
            with open(f"discord_storage_not_encrypted/{user_id}.txt", "w") as file:
                file.write(f"\n{name}:\n" + to_remember)
            await interaction.response.send_message(f"Under the name: {name}. I have remembered: {to_remember}.")
            return
        file = open(f"discord_storage_not_encrypted/{user_id}.txt", "r")
        lines = file.readlines()
        file.close()
        if len(lines) > 0 and name is None:
            lines[0] = to_remember
            with open(f"discord_storage_not_encrypted/{user_id}.txt", "w") as f:
                for line in lines:
                    f.write(line)
            await interaction.response.send_message(f"I have remembered: {to_remember}.")
            return
        elif len(lines) > 0:
            count = 0
            for line in lines:
                count += 1
                if line == f"{name}:\n":
                    break
            if count % 2 != 0:
                count = len(lines)
            if count == len(lines) and not len(lines) == 1:
                lines[1] = f"{name}:\n{to_remember}\n" + lines[1]
                with open(f"discord_storage_not_encrypted/{user_id}.txt", "w") as file:
                    for line in lines:
                        file.write(line)
                await interaction.response.send_message(f"Under the name: {name}. I have remembered: {to_remember}.")
                return
            elif count == len(lines) and len(lines) == 1:
                with open(f"discord_storage_not_encrypted/{user_id}.txt", "a") as file:
                    file.write(f"\n{name}:\n{to_remember}")
                await interaction.response.send_message(f"Under the name: {name}. I have remembered: {to_remember}.")
                return
            if count < len(lines):
                lines[count] = to_remember + "\n"
                with open(f"discord_storage_not_encrypted/{user_id}.txt", "w") as file:
                    for line in lines:
                        file.write(line)
                await interaction.response.send_message(f"Under the name: {name}. I have remembered: {to_remember}.")
                return





async def setup(client):
    await client.add_cog(RememberCommand(client))