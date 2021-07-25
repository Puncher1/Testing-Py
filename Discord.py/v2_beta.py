import discord
from discord.ext import commands

import os
# end imports


async def v2_beta(client):
    class Confirm(discord.ui.View):
        def __init__(self):
            super().__init__()
            self.value = None

        # When the confirm button is pressed, set the inner value to `True` and
        # stop the View from listening to more input.
        # We also send the user an ephemeral message that we're confirming their choice.
        @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
        async def confirm(self, button: discord.ui.Button, interaction: discord.Interaction):
            await interaction.response.send_message('Confirming', ephemeral=True)
            self.value = True
            self.stop()

        # This one is similar to the confirmation button except sets the inner value to `False`
        @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
        async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
            await interaction.response.send_message('Cancelling', ephemeral=True)
            self.value = False
            self.stop()

    @client.command()
    async def ask(ctx: commands.Context):
        """Asks the user a question to confirm something."""
        # We create the view and assign it to a variable so we can wait for it later.
        view = Confirm()
        await ctx.send('Do you want to continue?', view=view)
        # Wait for the View to stop listening for input...
        await view.wait()
        if view.value is None:
            print('Timed out...')
        elif view.value:
            print('Confirmed...')
        else:
            print('Cancelled...')


    class Counter(discord.ui.View):

        # Define the actual button
        # When pressed, this increments the number displayed until it hits 5.
        # When it hits 5, the counter button is disabled and it turns green.
        # note: The name of the function does not matter to the library
        @discord.ui.button(label='0', style=discord.ButtonStyle.red)
        async def count(self, button: discord.ui.Button, interaction: discord.Interaction):
            number = int(button.label) if button.label else 0
            if number + 1 >= 5:
                button.style = discord.ButtonStyle.green
                button.disabled = True
            button.label = str(number + 1)

            # Make sure to update the message with our updated selves
            await interaction.response.edit_message(view=self)

    @client.command()
    async def counter(ctx: commands.Context):
        """Starts a counter for pressing."""
        await ctx.send('Press!', view=Counter())


    class Choose(discord.ui.View):

        cake = discord.SelectOption(label="🍰 Cake", description="Get a cake.")
        gift = discord.SelectOption(label="🎁 Gift", description="Get a gift.")

        @discord.ui.select(options=[cake, gift], placeholder="Choose something")
        async def selection(self, button: discord.ui.Select, interaction: discord.Interaction):
            await interaction.response.send_message(f"You choosed {button.values[0]}!", ephemeral=True)

    @client.command()
    async def choose(ctx):
        await ctx.send("Choose!", view=Choose())


    class Button(discord.ui.View):
        def __init__(self):
            super().__init__()
            self.count = 0
            self.label_dict = {
                1: ["Hit!", discord.ButtonStyle.green],
                2: ["Double Hit!", discord.ButtonStyle.green],
                3: ["Triple Hit!", discord.ButtonStyle.green],
                4: ["Dominating!", discord.ButtonStyle.green],
                5: ["Rampage!!", discord.ButtonStyle.green],
                6: ["Mega Hit!!", discord.ButtonStyle.green],
                7: ["Unstoppable!!", discord.ButtonStyle.green],
                8: ["Wicked Sick!!", discord.ButtonStyle.green],
                9: ["Monster Hit!!!", discord.ButtonStyle.green],
                10: ["GODLIKE!!!!", discord.ButtonStyle.red],
                11: ["BEYOND GODLIKE!!!!!!", discord.ButtonStyle.red]
            }

        @discord.ui.button(label=f"Click!", style=discord.ButtonStyle.grey)
        async def button_func(self, button_obj: discord.ui.Button, interaction: discord.Interaction):
            self.count += 1

            edit_bool = True
            if self.count > 11:
                button_obj.disabled = True
                edit_bool = False

            if edit_bool:
                button_obj.label = self.label_dict[self.count][0]
                button_obj.style = self.label_dict[self.count][1]
            await interaction.response.edit_message(view=self)

    @client.command()
    async def button(ctx):
        await ctx.send("Click!", view=Button())

    # end shutdown command


