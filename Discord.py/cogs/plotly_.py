import discord
import imgkit
from discord.ext import commands
import plotly.graph_objects as go
from plotly import io
import kaleido
import os
import asyncio

class Plotly(commands.Cog):

    def __init__(self, client):
        self.bot = client


    @commands.command()
    async def p(self, ctx, *, args: str):
        path_wkthmltoimage = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltoimage.exe'
        config = imgkit.config(wkhtmltoimage=path_wkthmltoimage)

        yRawValues = args.split(",")
        yValues = []
        for y in yRawValues:
            y.strip()
            yValues.append(int(y))

        fig = go.Figure(data=go.Bar(y=yValues, x=[0, 10]))

        if not os.path.exists("./images"):
            os.mkdir("./images")

        fig.write_html('./images/fig.html', auto_open=False)
        imgkit.from_url("https://cdn.discordapp.com/attachments/722467477031878716/901882306082533416/fig.png", "./images/fig.png", config=config)

        file = discord.File("./images/fig.png", filename="fig.png")
        await ctx.send(file=file)

async def setup(client):
    await client.add_cog(Plotly(client))