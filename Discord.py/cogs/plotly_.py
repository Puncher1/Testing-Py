import discord
from discord.ext import commands
import plotly.graph_objects as go
from plotly import io
import kaleido
import os

class Plotly(commands.Cog):

    def __init__(self, client):
        self.bot = client


    @commands.command()
    async def p(self, ctx, *, args: str):
        yRawValues = args.split(",")
        yValues = []
        for y in yRawValues:
            y.strip()
            yValues.append(int(y))

        fig = go.Figure(data=go.Bar(y=yValues, x=[0, 10]))

        if not os.path.exists("./cogs/images"):
            os.mkdir("./cogs/images")
        print(1)
        fig.write_image("./cogs/images/fig1.png")
        print(2)


def setup(client):
    client.add_cog(Plotly(client))