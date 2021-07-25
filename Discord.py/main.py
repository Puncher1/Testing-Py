import discord
from discord.ext import commands
import os
import sys
from dotenv import load_dotenv
import asyncio

import jishaku_
import help_cmd
import github_api
# end imports


load_dotenv()
intents = discord.Intents.all()
client = commands.Bot(command_prefix="$", intents=intents)
# end setup

BOT_TOKEN = os.getenv("TEST_TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

PUNCHER_ID = 305354423801217025
# end global constants


async def invoking_funcs():
    asyncio.create_task(jishaku_.jishaku_func(client))


@client.event
async def on_ready():
    print("Ready!")
    await invoking_funcs()
# end invoking functions


@client.command(aliases=["s"])
@commands.is_owner()
async def shutdown(ctx):
    await client.close()
# end shutdown

@client.command()
async def about(ctx):
    github_desc = await github_api.github_api(GITHUB_TOKEN)

    owner = client.get_user(PUNCHER_ID)

    embed = discord.Embed()
    embed.title = f"About {client.user.name}"
    embed.description = f"{client.user.name} is a bot for development test purposes for {owner}." \
                        f"\nPython {sys.version[0:3]}, Discord.py {discord.__version__}"
    embed.add_field(name="Developer", value=f"```{owner}```", inline=False)
    embed.add_field(name="GitHub", value=f"{github_desc}", inline=False)
    await ctx.send(embed=embed)


client.run(os.getenv("TEST_TOKEN"))
# end main file
