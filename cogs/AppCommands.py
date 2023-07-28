import discord
from discord import app_commands
from discord.ext import commands
import random

class AppCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.tree.sync()
        print(f"{__name__} loaded successfully!")

    @app_commands.command(name="avatar", description="Sends user's avatar in a embed (sends own avatar if user is left none)")
    async def avatar(self, interaction: discord.Interaction, member: discord.Member = None):
        if member is None:
            member = interaction.user
        elif member is not None:
            member = member

        user = interaction.user

        avatar_embed = discord.Embed(title=f"{member.name}'s Avatar", color=discord.Color.random())
        avatar_embed.set_image(url=member.avatar)
        avatar_embed.set_footer(text=f"Requested by {user.name}", icon_url=user.avatar)

        await interaction.response.send_message(embed=avatar_embed)

    @app_commands.command(name="ping", description="Sends the bot's latency in ms")
    async def ping(self, interaction: discord.Interaction):
        bot_latency = round(self.client.latency * 1000)

        await interaction.response.send_message(f"Pong! {bot_latency}ms.")

    @app_commands.command(name="wwur", description="Sends you what would you rather Questions.")
    async def ping(self, interaction: discord.Interaction):
        file = open("discord_storage/wwur.txt")
        lines = file.readlines()
        file.close()
        max_line = len(lines) - 1
        line = random.randint(0, max_line)
        await interaction.response.send_message(lines[line])
        return

    @app_commands.command(name="invite", description="creates invite link")
    async def invite_user(self, interaction: discord.Interaction, uses: int = 0, length_in_seconds: int = 0,
                          temporary: bool = False):
        if isinstance(interaction.channel, discord.DMChannel):
            await interaction.response.send_message(
                "Sorry, but this command is only supported in servers.", ephemeral=True)
            return

        message = ""

        if length_in_seconds > 2592000:
            message = "length in seconds can not exceed 2592000 seconds (30 days)," \
                      " thus it was automatically set to 2592000 seconds (30 days)\n"
            length_in_seconds = 2592000
        if uses > 100:
            message += "uses can not exceed 100, thus it was automatically set to 100\n"
            uses = 100
        invite = await interaction.guild.text_channels[0].create_invite(max_uses=uses, max_age=length_in_seconds,
                                                                        temporary=temporary)

        message += str(invite)

        await interaction.response.send_message(message)

async def setup(client):
    await client.add_cog(AppCommands(client))