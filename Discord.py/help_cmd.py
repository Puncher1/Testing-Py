import discord
from discord.ext import commands

async def help_func(client: commands.Bot):

    class EmbedMinimalHelp(commands.MinimalHelpCommand):
        async def send_pages(self):                   # override 'send_pages' function
            destination = self.get_destination()      # get context channel
            for page in self.paginator.pages:         # iterate through every page that discord.ext.commands.Paginator creates
                embed = discord.Embed(
                    color=discord.Colour.blurple(),
                    description=page,
                    title="Help"
                )
                await destination.send(embed=embed)


    class OverrideMethod(EmbedMinimalHelp):
        async def send_command_help(self, command):                         # override 'send_command_help' function
            channel = self.get_destination()
            if command.name == "about":                                     # checking if it's the command 'about'
                await channel.send("About Me :)")
            else:
                await EmbedMinimalHelp.send_command_help(self, command)     # send default command help


    class MyFirstHelp(commands.HelpCommand):
        async def send_bot_help(self, mapping):
            embed = discord.Embed(title="Help", color=discord.Colour.blurple())

            print(mapping)
            print(mapping.items())
            for cog, commands in mapping.items():                                         # iterate through every cog
                command_signatures = [self.get_command_signature(c) for c in commands]    # get signature (<prefix><command|aliases> <arguments>) of every command in cog
                print(command_signatures)
                if command_signatures:                                                    # check if commands in cog exist
                    cog_name = getattr(cog, "qualified_name", "No Category")              # get cog's name, default: 'No Category'
                    embed.add_field(
                        name=cog_name,
                        value="\n".join(command_signatures),
                        inline=False)

            channel = self.get_destination()
            await channel.send(embed=embed)


    class MySecondHelp(commands.HelpCommand):
        def get_command_signature(self, command):
            return f"{self.context.clean_prefix}{command.qualified_name} {command.signature}"       # creating own signature (<prefix><command> <arguments>)

        async def send_bot_help(self, mapping):
            embed = discord.Embed(title="Help", color=discord.Colour.blurple())
            for cog, commands in mapping.items():
                filtered = await self.filter_commands(commands, sort=True)                          # filtering out commands which the user can't use
                command_signatures = [self.get_command_signature(c) for c in filtered]
                if command_signatures:
                    cog_name = getattr(cog, "qualified_name", "No Category")
                    embed.add_field(
                        name=cog_name,
                        value="\n".join(command_signatures),
                        inline=False
                    )
            channel = self.get_destination()
            await channel.send(embed=embed)


    class MyThirdHelp(commands.MinimalHelpCommand):
        async def send_command_help(self, command):
            embed = discord.Embed(color=discord.Colour.blurple(), title=command.name)
            alias = command.aliases
            if command.help is not None:
                embed.add_field(name="Description", value=command.help)

            if alias:
                embed.add_field(name="Aliases", value=", ".join(alias), inline=False)

            channel = self.get_destination()
            await channel.send(embed=embed)

    class OverrideError(MyThirdHelp):
        async def send_error_message(self, error):
            embed = discord.Embed(color=discord.Colour.red(), title="Error", description=error)
            channel = self.get_destination()
            await channel.send(embed=embed)


    attributes = {
        'name': "hel",
        'aliases': ["help", "helps", "commands"],
        'cooldown': commands.CooldownMapping.from_cooldown(1, 5.0, commands.BucketType.user)
    }

    client.help_command = OverrideError(command_attrs=attributes)
