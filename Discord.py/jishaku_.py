import discord

import os
import jishaku
# end imports


async def jishaku_func(client):
    os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
    client.load_extension("jishaku")




