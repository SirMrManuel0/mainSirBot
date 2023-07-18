import discord
from discord import app_commands
from discord.ext import commands

class RememberCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.tree.sync()
        print(f"{__name__} loaded successfully!")

    @app_commands.command(name="remember", description="give the bot something to remember | name for the thing to remember can be added")
    async def remember(self, interaction: discord.Interaction, to_remember: str):
        user_id = interaction.user.id

        remember = open('discord_storage_not_encrypted/remember.txt', 'r')
        lines = remember.readlines()

        line_count = 1
        for line in lines:
            if line == "#"*10 + str(user_id) + ":\n":
                break
            line_count += 1
        if line_count >= len(lines) or len(lines) == 0:
            with open('discord_storage_not_encrypted/remember.txt', 'a') as file:
                file.write("\n" + "#" * 10 + str(interaction.user.id) + ":\n" + to_remember)
                await interaction.response.send_message(f"I have remembered: {to_remember}")
                return
        elif line_count < len(lines):
            lines[line_count] = to_remember + "\n"
            with open('discord_storage_not_encrypted/remember.txt', 'w') as file:
                file.writelines(lines)
            await interaction.response.send_message(f"I have remembered: {to_remember}")
            return

        await interaction.response.send_message(f"I have not remembered: {to_remember}")






async def setup(client):
    await client.add_cog(RememberCommand(client))