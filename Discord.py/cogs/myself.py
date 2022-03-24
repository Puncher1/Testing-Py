from discord.ext import commands

import os
from pathlib import Path

from cogs import global_ as g
from cogs import error_handler, embeds
# end imports

class Myself(commands.Cog):
    """Commands for Puncher"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Command: Shutdown
    @commands.command(aliases=["s"], description="Shuts down the bot")
    @commands.is_owner()
    async def shutdown(self, ctx: commands.Context):
        """
        Shuts down the bot. Only usable by the owner of the bot.
        """

        await ctx.message.add_reaction(g.e_white_checkmark)
        await self.bot.close()


    # Command: Cog reload
    @commands.command(aliases=["cr", "r"], description="Cogs reloading")
    @commands.is_owner()
    async def reload(self, ctx: commands.Context, *, path=None):

        """
        Reloads cogs, loads cogs that aren't loaded and unloads cogs whose file doesn't exist anymore.
        """

        # All cogs reload
        async def all_cogs_reloading():
            """Reloads every extension in './cogs'. Loads extensions that aren't loaded. Unloads extensions whose file doesn't exist anymore."""

            # Get extensions
            files = []
            ignored_extensions = ["!", "DEV", "embeds", "global_"]

            for file in Path("cogs").glob("**/*.py"):
                if any(ignored_extension in file.name for ignored_extension in ignored_extensions):
                    continue
                files.append(str(file).replace("\\", ".").replace(".py", ""))

            error = None
            full_trace = None

            # Unload deleted extension files
            unloaded_list, unloaded_count = [], 0

            for extension in list(self.bot.extensions):
                if extension not in files:
                    try:
                        self.bot.unload_extension(extension)
                    except:
                        short_trace = error_handler.short_traceback()
                        error = f"```py\n{short_trace}\n```"
                        break
                    else:
                        unloaded_list.append(f"`{extension}`")
                        unloaded_count += 1

            # Reload/Load extensions
            reloaded_list, reloaded_count = [], 0
            loaded_list, loaded_count = [], 0

            for ext in files:
                if ext in self.bot.extensions:
                    # Reload

                    try:
                        self.bot.reload_extension(ext)
                    except:
                        short_trace = error_handler.short_traceback()
                        full_trace = error_handler.full_traceback()
                        error = f"```py\n{short_trace}\n```"
                        break
                    else:
                        reloaded_list.append(f"`{ext}`")
                        reloaded_count += 1
                else:
                    # Load

                    try:
                        self.bot.load_extension(ext)
                    except:
                        short_trace = error_handler.short_traceback()
                        full_trace = error_handler.full_traceback()
                        error = f"```py\n{short_trace}\n```"
                        break

                    else:
                        loaded_list.append(f"`{ext}`")
                        loaded_count += 1


            if loaded_count > 0:
                loaded_list_join = "\n".join(loaded_list)
                loaded_str = f"\n\n{g.e_arrow_up_right} **Loaded - [{loaded_count}]**" \
                             f"\n{loaded_list_join}"
            else:
                loaded_str = ""

            if reloaded_count > 0:
                reloaded_list_join = "\n".join(reloaded_list)
                reloaded_str = f"{g.e_reload} **Reloaded - [{reloaded_count}]**" \
                               f"\n{reloaded_list_join}"
            else:
                reloaded_str = ""

            if unloaded_count > 0:
                unloaded_list_join = "\n".join(unloaded_list)
                unloaded_str = f"\n\n{g.e_arrow_down_right} **Unloaded - [{unloaded_count}]**" \
                               f"\n{unloaded_list_join}"
            else:
                unloaded_str = ""

            error = f"{error}" if error else "No error while reloading."

            await embeds.embed_gen(
                channel=ctx.channel,
                color=None,
                title="Cogs",
                description=f"{reloaded_str}"
                            f"{loaded_str}"
                            f"{unloaded_str}"
                            f"\n\n\n**Error**"
                            f"\n{error}",
                footer_text=None,
                thumbnail_url=None,
                image_url=None,
                return_embed=False
            )

            if full_trace:
                error_logs = self.bot.get_channel(g.error_channel)
                await embeds.embed_gen(
                    error_logs,
                    f"An error accured. Command: {ctx.command}",
                    f"```py\n{full_trace}\n```",
                    None,
                    None,
                    None,
                    g.error_red,
                    False
                )

        # Cog reload by path
        async def path_cog_reload():

            if path in self.bot.extensions:
                try:
                    self.bot.reload_extension(f"{path}")
                except:
                    short_trace = error_handler.short_traceback()
                    error = f"```py\n{short_trace}\n```"

                    await embeds.embed_gen(
                        channel=ctx.channel,
                        title="Cogs",
                        description=f"**An error occurred.**"
                                    f"\n{error}",
                        footer_text=None,
                        color=None,
                        thumbnail_url=None,
                        image_url=None,
                        return_embed=False
                    )
                    return

            else:
                try:
                    self.bot.load_extension(f"{path}")
                except:
                    short_trace = error_handler.short_traceback()
                    error = f"```py\n{short_trace}\n```"

                    await embeds.embed_gen(
                        channel=ctx.channel,
                        title="Cogs",
                        description=f"**An error occurred.**"
                                    f"\n{error}",
                        footer_text=None,
                        color=None,
                        thumbnail_url=None,
                        image_url=None,
                        return_embed=False
                    )
                    return

            reloaded_str = f"{g.e_reload} **Reloaded**" \
                           f"\n`{path}`"

            await embeds.embed_gen(
                channel=ctx.channel,
                color=None,
                title="Cogs",
                description=f"{reloaded_str}",
                footer_text=None,
                thumbnail_url=None,
                image_url=None,
                return_embed=False
            )

        # Invoking coroutines
        if not path:
            await all_cogs_reloading()
        else:
            await path_cog_reload()


async def setup(bot: commands.Bot):
    await bot.add_cog(Myself(bot))