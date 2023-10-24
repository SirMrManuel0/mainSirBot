# Import required libraries and modules
import discord
from discord import app_commands
from discord.ext import commands
import os
from credentials import keyMaker
import en_decrypt

# Define a custom Cog class called RememberCommand
class RememberCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Event handler for when the Cog is loaded
    @commands.Cog.listener()
    async def on_ready(self):
        """
        Event handler for when the bot is ready.

        This method is called when the bot successfully connects to Discord.

        Args:
            self: The RememberCommand instance.

        Returns:
            None
        """
        await self.client.tree.sync()
        print(f"{__name__} loaded successfully!")

    # Define a command called "remember" to make the bot remember something
    @app_commands.command(name="remember", description="give the bot something to remember")
    async def remember(self, interaction: discord.Interaction, to_remember: str, name: str = None):
        """
        Command to remember a piece of information.

        This command allows the bot to store and remember a piece of information, optionally associated with a name.

        Args:
            self: The RememberCommand instance.
            interaction: The interaction object.
            to_remember (str): The information to remember.
            name (str, optional): The name under which to remember the information.

        Returns:
            None
        """
        # Check if the command is used in a DM channel
        if isinstance(interaction.channel, discord.DMChannel):
            await interaction.response.send_message(
                "Sorry, but this command is only supported in servers.", ephemeral=True)
            return

        # Get guild and user IDs
        guild_id = interaction.guild_id
        user_id = interaction.user.id

        # Generate a key for encryption
        key = keyMaker.keyMaking(user_id, guild_id)

        # Encrypt the data to remember
        encrypted = en_decrypt.encrypt(to_remember, key)

        # Handle different cases based on whether a file exists and if a name is provided
        if not os.path.exists(f"discord_storage/{str(guild_id)}/{str(user_id)}.txt") and name is None:
            # Case: something is to be remembered for the first time with no name
            # Create the file if it doesn't exist
            if not os.path.exists(f"discord_storage/{str(guild_id)}/"):
                os.mkdir(f"discord_storage/{str(guild_id)}/")

            with open(f"discord_storage/{str(guild_id)}/{str(user_id)}.txt", "w", encoding="utf-8") as file:
                file.write(encrypted + "\n")
            await interaction.response.send_message(f"I have remembered: {to_remember}.")
            return
        elif not os.path.exists(f"discord_storage/{str(guild_id)}/{str(user_id)}.txt"):
            # Case: something is to be remembered for the first time with name

            if not os.path.exists(f"discord_storage/{str(guild_id)}/"):
                os.mkdir(f"discord_storage/{str(guild_id)}/")

            with open(f"discord_storage/{str(guild_id)}/{str(user_id)}.txt", "w", encoding="utf-8") as file:
                file.write(f"\n{name}:\n" + encrypted + "\n")
            await interaction.response.send_message(f"Under the name: {name}. I have remembered: {to_remember}.")
            return
        file = open(f"discord_storage/{str(guild_id)}/{str(user_id)}.txt", "r", encoding="utf-8")
        lines = file.readlines()
        file.close()
        if len(lines) > 0 and name is None:
            # Case: something is to be remembered with no name

            lines[0] = encrypted + "\n"
            with open(f"discord_storage/{str(guild_id)}/{str(user_id)}.txt", "w", encoding="utf-8") as f:
                for line in lines:
                    f.write(line)
            await interaction.response.send_message(f"I have remembered: {to_remember}.")
            return
        elif len(lines) > 0:
            # Case: something is to be remembered with name

            count = 0
            for line in lines:
                if line == f"{name}:\n":
                    break
                count += 1

            if count == len(lines) and not len(lines) == 1:
                # Case: name is not used

                lines[1] = f"{name}:\n{encrypted}\n" + lines[1]
                with open(f"discord_storage/{str(guild_id)}/{str(user_id)}.txt", "w", encoding="utf-8") as file:
                    for line in lines:
                        file.write(line)
                await interaction.response.send_message(f"Under the name: {name}. I have remembered: {to_remember}.")
                return
            elif count == len(lines) and len(lines) == 1:
                # Case: nothing to remember has yet been set with name

                with open(f"discord_storage/{str(guild_id)}/{str(user_id)}.txt", "a", encoding="utf-8") as file:
                    file.write(f"{name}:\n{encrypted}\n")
                await interaction.response.send_message(f"Under the name: {name}. I have remembered: {to_remember}.")
                return
            if count < len(lines):
                # Case: name was already used

                lines[count + 1] = encrypted + "\n"
                with open(f"discord_storage/{str(guild_id)}/{str(user_id)}.txt", "w", encoding="utf-8") as file:
                    for line in lines:
                        file.write(line)
                await interaction.response.send_message(f"Under the name: {name}. I have remembered: {to_remember}.")
                return
        await interaction.response.send_message(f"I can not remember: {to_remember}")

    # Define a command called "recall" to retrieve what the bot saved
    @app_commands.command(name="recall", description="remember what the bot saved")
    async def recall(self, interaction: discord.Interaction, name: str = None):
        """
        Command to recall a previously stored piece of information.

        This command allows the bot to retrieve and recall information it has stored previously, optionally by name.

        Args:
            self: The RememberCommand instance.
            interaction: The interaction object.
            name (str, optional): The name of the information to recall.

        Returns:
            None
        """
        if isinstance(interaction.channel, discord.DMChannel):
            await interaction.response.send_message(
                "Sorry, but this command is only supported in servers.", ephemeral=True)
            return

        guild_id = interaction.guild_id
        user_id = interaction.user.id


        key = keyMaker.keyMaking(user_id, guild_id)

        if not os.path.exists(f"discord_storage/{str(guild_id)}/{str(user_id)}.txt"):
            # Case: nothing to remember

            await interaction.response.send_message(f"I can not remember anything.")
            return
        file = open(f"discord_storage/{str(guild_id)}/{str(user_id)}.txt", "r", encoding="utf-8")
        lines = file.readlines()
        file.close()
        if name is None and lines[0] == "":
            # Case: file exists yet there is nothing to remember

            await interaction.response.send_message(f"I can not remember anything. Maybe try using a name.")
            return
        elif name is None:
            # Case: standard thing to remember

            await interaction.response.send_message(f"I seem to remember: {en_decrypt.decrypt(lines[0], key)[:-1]}.")
            return
        if name is not None:
            # Case: something with a name will be recalled

            count = 0
            for line in lines:
                count += 1
                if line == f"{name}:\n" and count % 2 == 0:
                    break
            if count == len(lines):
                # Case: name does not exist

                await interaction.response.send_message(f"I can not remember something under the name: {name}.")
                return
            await interaction.response.send_message(f"Under the name: {name}. I seem to remember: {en_decrypt.decrypt(lines[count], key)[:-1]}.")

    # Define a command called "server_remember" to make the bot remember something for the server
    @app_commands.command(name="server_remember", description="give the bot something to remember and everyone to recall")
    async def server_remember(self, interaction: discord.Interaction, to_remember: str, name: str = None):
        """
        Command to remember information for the server.

        This command allows the bot to store and remember information for the entire server to recall, optionally with a name.

        Args:
            self: The RememberCommand instance.
            interaction: The interaction object.
            to_remember (str): The information to remember.
            name (str, optional): The name under which to remember the information.

        Returns:
            None
        """
        if isinstance(interaction.channel, discord.DMChannel):
            await interaction.response.send_message(
                "Sorry, but this command is only supported in servers.", ephemeral=True)
            return

        guild_id = interaction.guild_id

        key = keyMaker.keyMakingServer(guild_id)

        encrypted = en_decrypt.encrypt(to_remember, key)

        if not os.path.exists(f"discord_storage/{str(guild_id)}/{str(guild_id)}.txt") and name is None:
            # Case: something is to be remembered for the first time with no name

            if not os.path.exists(f"discord_storage/{str(guild_id)}/"):
                os.mkdir(f"discord_storage/{str(guild_id)}/")

            with open(f"discord_storage/{str(guild_id)}/{str(guild_id)}.txt", "w", encoding="utf-8") as file:
                file.write(encrypted + "\n")
            await interaction.response.send_message(f"I have remembered: {to_remember}.")
            return
        elif not os.path.exists(f"discord_storage/{str(guild_id)}/{str(guild_id)}.txt"):
            # Case: something is to be remembered for the first time with name

            if not os.path.exists(f"discord_storage/{str(guild_id)}/"):
                os.mkdir(f"discord_storage/{str(guild_id)}/")

            with open(f"discord_storage/{str(guild_id)}/{str(guild_id)}.txt", "w", encoding="utf-8") as file:
                file.write(f"\n{name}:\n" + encrypted + "\n")
            await interaction.response.send_message(f"Under the name: {name}. I have remembered: {to_remember}.")
            return
        file = open(f"discord_storage/{str(guild_id)}/{str(guild_id)}.txt", "r", encoding="utf-8")
        lines = file.readlines()
        file.close()
        if len(lines) > 0 and name is None:
            # Case: something is to be remembered with no name

            lines[0] = encrypted + "\n"
            with open(f"discord_storage/{str(guild_id)}/{str(guild_id)}.txt", "w", encoding="utf-8") as f:
                for line in lines:
                    f.write(line)
            await interaction.response.send_message(f"I have remembered: {to_remember}.")
            return
        elif len(lines) > 0:
            # Case: something is to be remembered with name

            count = 0
            for line in lines:
                if line == f"{name}:\n":
                    break
                count += 1

            if count == len(lines) and not len(lines) == 1:
                # Case: name is not used

                lines[1] = f"{name}:\n{encrypted}\n" + lines[1]
                with open(f"discord_storage/{str(guild_id)}/{str(guild_id)}.txt", "w", encoding="utf-8") as file:
                    for line in lines:
                        file.write(line)
                await interaction.response.send_message(f"Under the name: {name}. I have remembered: {to_remember}.")
                return
            elif count == len(lines) and len(lines) == 1:
                # Case: nothing to remember has yet been set with name

                with open(f"discord_storage/{str(guild_id)}/{str(guild_id)}.txt", "a", encoding="utf-8") as file:
                    file.write(f"{name}:\n{encrypted}\n")
                await interaction.response.send_message(f"Under the name: {name}. I have remembered: {to_remember}.")
                return
            if count < len(lines):
                # Case: name was already used

                lines[count + 1] = encrypted + "\n"
                with open(f"discord_storage/{str(guild_id)}/{str(guild_id)}.txt", "w", encoding="utf-8") as file:
                    for line in lines:
                        file.write(line)
                await interaction.response.send_message(f"Under the name: {name}. I have remembered: {to_remember}.")
                return
        await interaction.response.send_message(f"I can not remember: {to_remember}")

    # Define a command called "server_recall" to retrieve what the bot saved for the server
    @app_commands.command(name="server_recall", description="remember what the bot saved for the server")
    async def server_recall(self, interaction: discord.Interaction, name: str = None):
        """
       Command to recall information stored for the server.

       This command allows the bot to retrieve and recall information stored for the entire server, optionally by name.

       Args:
           self: The RememberCommand instance.
           interaction: The interaction object.
           name (str, optional): The name of the information to recall.

       Returns:
           None
       """
        if isinstance(interaction.channel, discord.DMChannel):
            await interaction.response.send_message(
                "Sorry, but this command is only supported in servers.", ephemeral=True)
            return

        guild_id = interaction.guild_id

        key = keyMaker.keyMakingServer(guild_id)

        if not os.path.exists(f"discord_storage/{str(guild_id)}/{str(guild_id)}.txt"):
            # Case: nothing to remember

            await interaction.response.send_message(f"I can not remember anything.")
            return
        file = open(f"discord_storage/{str(guild_id)}/{str(guild_id)}.txt", "r", encoding="utf-8")
        lines = file.readlines()
        file.close()
        if name is None and lines[0] == "":
            # Case: file exists yet there is nothing to remember

            await interaction.response.send_message(f"I can not remember anything. Maybe try using a name.")
            return
        elif name is None:
            # Case: standard thing to remember

            if len(lines) == 1:
                await interaction.response.send_message(f"I seem to remember: {en_decrypt.decrypt(lines[0], key)}.")
                return
            await interaction.response.send_message(f"I seem to remember: {en_decrypt.decrypt(lines[0], key)[:-1]}.")
            return
        if name is not None:
            # Case: something with a name will be recalled

            count = 0
            for line in lines:
                count += 1
                if line == f"{name}:\n" and count % 2 == 0:
                    break
            if count == len(lines):
                # Case: name does not exist

                await interaction.response.send_message(f"I can not remember something under the name: {name}.")
                return
            await interaction.response.send_message(
                f"Under the name: {name}. I seem to remember: {en_decrypt.decrypt(lines[count], key)[:-1]}.")

# Function to set up the RememberCommand Cog
async def setup(client):
    await client.add_cog(RememberCommand(client))
