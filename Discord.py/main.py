import discord
from discord.ext import commands

import os
from dotenv import load_dotenv
import asyncio

import jishaku_
# end imports


load_dotenv()
intents = discord.Intents.all()
client = commands.Bot(command_prefix="$", intents=intents)
# end setup


async def invoking_func():
    asyncio.create_task(jishaku_.jishaku_func(client))


@client.event
async def on_ready():
    await invoking_func()
# end invoking functions


@client.command(aliases=["s"])
@commands.is_owner()
async def shutdown(ctx):
    await client.logout()
# end shutdown

client.run(os.getenv("TEST_TOKEN"))
# end main file
