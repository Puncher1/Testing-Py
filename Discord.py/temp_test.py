import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()


bot = commands.Bot(
    command_prefix="$",
    case_insensitive=True,
    intents=intents,
    status=discord.Status.dnd,
    activity=discord.Activity(name='TM!help',type=discord.ActivityType.watching))
bot.remove_command('help')


@bot.event
async def on_ready():
    print(f'{bot.user} is online!')

bot.run(os.getenv("TEST_TOKEN"))