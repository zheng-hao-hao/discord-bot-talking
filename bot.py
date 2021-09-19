import discord
from discord import channel
from discord.ext import commands
from discord.flags import Intents
import json
import os
import time

with open('setting.json','r',encoding='utf8') as jfile:
    jdata = json.load(jfile)

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='~',intents = intents)

@bot.event
async def on_ready():
    print("機器人已就緒")

@bot.event
async def on_member_join(user):
    channel = bot.get_channel(int(jdata['Msg_channel']))
    await channel.send(f"{user}加入了伺服器!")


@bot.event 
async def on_member_remove(user):
    channel = bot.get_channel(int(jdata['Msg_channel']))
    await channel.send(f"{user}離開了伺服器!")

@bot.command()
async def load(ctx,extension):
    bot.load_extension(f'cmds.{extension}')
    await ctx.send(f'安裝 {extension} 模組完成')

@bot.command()
async def unload(ctx,extension):
    bot.unload_extension(f'cmds.{extension}')
    await ctx.send(f'卸載 {extension} 模組完成')

@bot.command()
async def reload(ctx,extension):
    bot.reload_extension(f'cmds.{extension}')
    await ctx.send(f'重新載入 {extension} 模組完成')

for filename in os.listdir("./cmds"):
    if filename.endswith(".py"):
        bot.load_extension(f"cmds.{filename[:-3]}")

if __name__ =="__main__":
    bot.run(jdata['TOKEN'])
