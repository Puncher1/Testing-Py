import discord
from discord import app_commands
from discord.ext import commands

class SlashCommands(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="hello", description="Hello World!")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message("HELLO WORLD!")


async def setup(client):
    await client.add_cog(SlashCommands(client))