import discord
from discord import app_commands
from discord.ext import commands
import os
import sys
from dotenv import load_dotenv
from pathlib import Path
import asyncio
import jishaku

from cogs import DEV_github_api


# end imports


load_dotenv()
intents = discord.Intents.all()
client = commands.Bot(command_prefix="$", intents=intents)
# end setup

BOT_TOKEN = os.getenv("TEST_TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
PUNCHER_ID = 305354423801217025
# end global constants

# TESTING
@client.command()
async def test(ctx, voiceChannel: discord.VoiceChannel):

    print(voiceChannel.members)


# Event: OnReady
@client.event
async def on_ready():
    print(f"[MAIN] Ready!")
    await get_extensions()


# Event: OnConnect
@client.event
async def on_connect():
    print(f"[MAIN] Connected to Discord.")


async def get_extensions():
    extensions = []
    ignored_extensions = ["!", "DEV", "embeds", "global_"]

    for file in Path("cogs").glob("**/*.py"):
        if any(ignored_extension in file.name for ignored_extension in ignored_extensions):
            continue
        extensions.append(str(file).replace("\\", ".").replace(".py", ""))

    for ext in extensions:
        await client.load_extension(ext)

    await client.tree.sync()

# LOAD EXTENSIONS

@client.command()
async def about(ctx: commands.Context):
    async with ctx.typing():
        github_desc = await DEV_github_api.github_api(GITHUB_TOKEN)
        owner = client.get_user(PUNCHER_ID)

    embed = discord.Embed()
    embed.title = f"About {client.user.name}"
    embed.description = f"{client.user.name} is a bot for development test purposes for {owner}." \
                        f"\nPython `{sys.version[0:3]}`, Discord.py `{discord.__version__}`, " \
                        f"Jishaku `{jishaku.__version__}`, PyGithub `1.55`"
    embed.add_field(name="Developer", value=f"```{owner}```", inline=False)
    embed.add_field(name="GitHub", value=f"{github_desc}", inline=False)
    await ctx.send(embed=embed)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"{error}", reference=ctx.message)


print("[MAIN] Boot up...")
print("[MAIN] Connecting to Discord...")
client.run(os.getenv("TEST_TOKEN"))
# end main file
