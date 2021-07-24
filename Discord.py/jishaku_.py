import discord
from discord.ext import commands

import os
import jishaku
# end imports


async def jishaku_func(client: commands.Bot):
    os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
    os.environ['JISHAKU_NO_DM_TRACEBACK'] = "True"
    os.environ['JISHAKU_RETAIN'] = 'True'
    client.load_extension("jishaku")
    client.reload_extension("jishaku")




