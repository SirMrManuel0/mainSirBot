import discord
from discord import app_commands
from discord.ext import commands
import os
from credentials import keyMaker
import en_decrypt


class RememberCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.tree.sync()
        print(f"{__name__} loaded successfully!")

    @app_commands.command(name="remember", description="give the bot something to remember")
    async def remember(self, interaction: discord.Interaction, to_remember: str, name: str = None):
        guild_id = interaction.guild_id
        user_id = interaction.user.id

        key = keyMaker.keyMaking(user_id, guild_id)

        encrypted = en_decrypt.encrypt(to_remember, key)


        if not os.path.exists(f"discord_storage/{str(guild_id)}/{str(user_id)}.txt") and name is None:
            os.mkdir(f"discord_storage/{str(guild_id)}/")
            with open(f"discord_storage/{str(guild_id)}/{str(user_id)}.txt", "w", encoding="utf-8") as file:
                file.write(encrypted)
            await interaction.response.send_message(f"I have remembered: {to_remember}.")
            return
        elif not os.path.exists(f"discord_storage/{str(guild_id)}/{str(user_id)}.txt"):
            os.mkdir(f"discord_storage/{str(guild_id)}/")
            with open(f"discord_storage/{str(guild_id)}/{str(user_id)}.txt", "w", encoding="utf-8") as file:
                file.write(f"\n{name}:\n" + encrypted)
            await interaction.response.send_message(f"Under the name: {name}. I have remembered: {to_remember}.")
            return
        file = open(f"discord_storage/{str(guild_id)}/{str(user_id)}.txt", "r", encoding="utf-8")
        lines = file.readlines()
        file.close()
        if len(lines) > 0 and name is None:
            lines[0] = encrypted
            with open(f"discord_storage/{str(guild_id)}/{str(user_id)}.txt", "w", encoding="utf-8") as f:
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
                lines[1] = f"{name}:\n{encrypted}\n" + lines[1]
                with open(f"discord_storage/{str(guild_id)}/{str(user_id)}.txt", "w", encoding="utf-8") as file:
                    for line in lines:
                        file.write(line)
                await interaction.response.send_message(f"Under the name: {name}. I have remembered: {to_remember}.")
                return
            elif count == len(lines) and len(lines) == 1:
                with open(f"discord_storage/{str(guild_id)}/{str(user_id)}.txt", "a", encoding="utf-8") as file:
                    file.write(f"\n{name}:\n{encrypted}")
                await interaction.response.send_message(f"Under the name: {name}. I have remembered: {to_remember}.")
                return
            if count < len(lines):
                lines[count] = encrypted + "\n"
                with open(f"discord_storage/{str(guild_id)}/{str(user_id)}.txt", "w", encoding="utf-8") as file:
                    for line in lines:
                        file.write(line)
                await interaction.response.send_message(f"Under the name: {name}. I have remembered: {to_remember}.")
                return
        await interaction.response.send_message(f"I can not remember: {to_remember}")


    @app_commands.command(name="recall", description="remember what the bot saved")
    async def recall(self, interaction: discord.Interaction, name: str = None):
        guild_id = interaction.guild_id
        user_id = interaction.user.id

        rec_id = str(user_id) + str(guild_id)

        key = keyMaker.keyMaking(user_id, guild_id)

        if not os.path.exists("discord_storage/" + rec_id + ".txt"):
            await interaction.response.send_message(f"I can not remember anything.")
            return
        file = open("discord_storage/" + rec_id + ".txt", "r", encoding="utf-8")
        lines = file.readlines()
        file.close()
        if name is None and lines[0] == "":
            await interaction.response.send_message(f"I can not remember anything. Maybe try using a name.")
            return
        elif name is None:
            await interaction.response.send_message(f"I seem to remember: {en_decrypt.decrypt(lines[0], key)}.")
            return
        if name is not None:
            count = 0
            for line in lines:
                count += 1
                if line == f"{name}:\n" and count % 2 == 0:
                    break
            if count == len(lines):
                await interaction.response.send_message(f"I can not remember something under the name: {name}.")
                return
            await interaction.response.send_message(f"Under the name: {name}. I seem to remember: {en_decrypt.decrypt(lines[count], key)}.")


async def setup(client):
    await client.add_cog(RememberCommand(client))
