'''
Author:@Zon0607

ver.:alpha 0.2.0

date:2024.12.15

'''
#import random
import discord
from discord import channel
from discord.ext import commands
from discord.flags import Intents
import interactions
import json #JSON
import os #OS
#import time #TIME
import asyncio #ASYNCIO
from interactions.api.voice.audio import AudioVolume
from bs4 import BeautifulSoup as bs4
#import requests

with open('setting.json','r',encoding='utf8') as jfile:
    jdata = json.load(jfile)



#=======================interactions.py settings===========================
irtbot = interactions.Client(token=jdata['TOKEN'])

@interactions.listen()
async def Startup():
    print('main bot is ready')

#fixing cmds

@interactions.slash_command(
    name="loadets",
    description="load extension",
    options=[  
                interactions.SlashCommandOption(
                name="name",
                description="The extension name that you want to load.",
                type=interactions.OptionType.STRING,
                required=True
                )
    ],
    default_member_permissions=interactions.Permissions.ADMINISTRATOR #only ADMIN can use this cmd
)
async def loadets(ctx,name):
    try:
        irtbot.load_extension(f'cmds.{name}')
        await ctx.send(f'{name} extension has loaded.')
    except:
        print(f'Error:Faild to load extension:{name}.')
        await ctx.send(f'Error:Faild to load extension:{name}.')

#fixing
@interactions.slash_command(
    name="reloadets",
    description="reload extension",
    options=[interactions.SlashCommandOption(
                name="name",
                description="The extension name that you want to reload.",
                type=interactions.OptionType.STRING,
                required=True
            )
    ],
    default_member_permissions=interactions.Permissions.ADMINISTRATOR #only ADMIN can use this cmd
    )
async def reloadets(ctx,name):
    try:
        irtbot.reload_extension(f'cmds.{name}')
        await ctx.send(f'{name} extension has reloaded.')
    except:
        print(f'Error:Faild to reload extension:{name}.')
        await ctx.send(f'Error:Faild to reload extension:{name}.')

@interactions.slash_command(
    name="unloadets",
    description="unload extension",
    options=[interactions.SlashCommandOption(
                name="name",
                description="The extension name that you want to unload.",
                type=interactions.OptionType.STRING,
                required=True,
            )
    ],
    default_member_permissions=interactions.Permissions.ADMINISTRATOR #only ADMIN can use this cmd
)
async def unloadets(ctx,name):
    try:
        irtbot.unload_extension(f'cmds.{name}')
        await ctx.send(f'{name} extension has unloaded.')
    except:
        print(f'Error:Faild to unload extension:{name}.')
        await ctx.send(f'Error:Faild to unload extension:{name}.')



for filename in os.listdir("./cmds"):
    if filename.endswith(".py"):
        try:
            irtbot.load_extension(f'cmds.{filename[:-3]}')
        except Exception as e:
            print(f"Failed to load extension:{filename[:-3]}.", e)


#=======================discord.py settings===============================
intents = discord.Intents.default()
intents.members = True
dcbot = commands.Bot(command_prefix='',intents = intents)

@dcbot.event
async def on_ready():
    print("event modes is ready")

@dcbot.event
async def on_member_join(member):
    channel = dcbot.get_channel(int(jdata['Msg_channel']))
    await channel.send(f"{member.display_name}加入了伺服器!")


@dcbot.event 
async def on_member_remove(member):
    channel = dcbot.get_channel(int(jdata['Msg_channel']))
    await channel.send(f"{member.display_name}離開了伺服器!")

#start two bot at the same time(irtbot and dcbot)
async def main():
    await asyncio.gather(
        dcbot.start(jdata['TOKEN']),
        irtbot.astart()
    )

#run code
asyncio.run(main())
