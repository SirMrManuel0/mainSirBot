# Import required libraries and modules
import discord
from discord import app_commands
from discord.ext import commands
import random

# Define a custom Cog class called AppCommands
class AppCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Event handler for when the Cog is loaded
    @commands.Cog.listener()
    async def on_ready(self):
        """
        Called when the Cog is loaded. Synchronizes the tree and prints a success message.
        """
        await self.client.tree.sync()
        print(f"{__name__} loaded successfully!")

    # Define a command called "avatar" to send a user's avatar in an embed
    @app_commands.command(name="avatar", description="Sends user's avatar in a embed (sends own avatar if user is left none)")
    async def avatar(self, interaction: discord.Interaction, member: discord.Member = None):
        """
        Sends a user's avatar in an embed. Defaults to the interaction user if no member is specified.

        Args:
            interaction (discord.Interaction): The interaction with the bot.
            member (discord.Member, optional): The member whose avatar to display. Defaults to None (interaction user).

        Returns:
            None
        """
        # Check if a member is specified, default to the interaction user if not
        if member is None:
            member = interaction.user
        elif member is not None:
            member = member

        user = interaction.user

        # Create an embed to display the user's avatar
        avatar_embed = discord.Embed(title=f"{member.name}'s Avatar", color=discord.Color.random())
        avatar_embed.set_image(url=member.avatar)
        avatar_embed.set_footer(text=f"Requested by {user.name}", icon_url=user.avatar)

        # Send the embed as a response
        await interaction.response.send_message(embed=avatar_embed)

    # Define a command called "ping" to send the bot's latency in milliseconds
    @app_commands.command(name="ping", description="Sends the bot's latency in ms")
    async def ping(self, interaction: discord.Interaction):
        """
        Sends the bot's latency in milliseconds.

        Args:
            interaction (discord.Interaction): The interaction with the bot.

        Returns:
            None
        """
        # Calculate the bot's latency in milliseconds
        bot_latency = round(self.client.latency * 1000)

        # Send the latency as a response
        await interaction.response.send_message(f"Pong! {bot_latency}ms.")

    # Define a command called "wwur" to send "Would You Rather" questions
    @app_commands.command(name="wwur", description="Sends you what would you rather Questions.")
    async def wwur(self, interaction: discord.Interaction):
        """
        Sends a "Would You Rather" question to the user.

        Args:
            interaction (discord.Interaction): The interaction with the bot.

        Returns:
            None
        """
        # Read "Would You Rather" questions from a file
        file = open("discord_storage/wwur.txt")
        lines = file.readlines()
        file.close()

        # Select a random question from the file
        max_line = len(lines) - 1
        line = random.randint(0, max_line)

        # Send the selected question as a response
        await interaction.response.send_message(lines[line])
        return

    # Define a command called "invite" to create an invite link
    @app_commands.command(name="invite", description="creates invite link")
    async def invite_user(self, interaction: discord.Interaction, uses: int = 0, length_in_seconds: int = 0,
                          temporary: bool = False):
        """
        Creates an invite link with specified settings and sends it as a response.

        Args:
            interaction (discord.Interaction): The interaction with the bot.
            uses (int, optional): Maximum number of uses for the invite. Defaults to 0 (unlimited).
            length_in_seconds (int, optional): Maximum duration (in seconds) for the invite. Defaults to 0 (never expires).
            temporary (bool, optional): Whether the invite is temporary. Defaults to False.

        Returns:
            None
        """
        # Check if the command is used in a DM channel
        if isinstance(interaction.channel, discord.DMChannel):
            await interaction.response.send_message(
                "Sorry, but this command is only supported in servers.", ephemeral=True)
            return

        message = ""

        # Check and limit the input values
        if length_in_seconds > 2592000:
            message = "length in seconds can not exceed 2592000 seconds (30 days)," \
                      " thus it was automatically set to 2592000 seconds (30 days)\n"
            length_in_seconds = 2592000
        if uses > 100:
            message += "uses can not exceed 100, thus it was automatically set to 100\n"
            uses = 100

        # Create an invite with the specified settings
        invite = await interaction.guild.text_channels[0].create_invite(max_uses=uses, max_age=length_in_seconds,
                                                                        temporary=temporary)

        message += str(invite)

        # Send the invite link as a response
        await interaction.response.send_message(message)

# Function to set up the AppCommands Cog
async def setup(client):
    """
    Sets up the AppCommands Cog and adds it to the client.

    Args:
        client (discord.Client): The Discord bot client.

    Returns:
        None
    """
    await client.add_cog(AppCommands(client))