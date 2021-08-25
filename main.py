import discord
from discord import channel
from discord.ext import commands
from discord.flags import Intents


intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='~',intents = intents)

@bot.event
async def on_ready():
    print("機器人已就緒")

@bot.event 
async def on_member_join(user):
    channel = bot.get_channel(875400740015849533)
    await channel.send(f"{user}加入了伺服器!")

@bot.event 
async def on_member_remove(user):
    channel = bot.get_channel(875400740015849533)
    await channel.send(f"{user}離開了伺服器!")

@bot.command()
async def ping(ctx):
    await ctx.send(f"目前延遲為{round(bot.latency*1000)} ms")


bot.run("ODc5OTIwMzAwMTI3NTU1NTg0.YSWvow.9krQ3kWzpsqgFeGfh7YrOaCKxI8")