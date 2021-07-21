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
    await asyncio.create_task(jishaku_.jishaku_func(client))

await invoking_func()
# end invoking external functions


await client.run(os.getenv("TOKEN"))
# end main file
