'''
Author:@Zon0607

ver.:alpha 0.2.0

date:2024.03.20
'''
import discord
from discord import channel
from discord.ext import commands
from discord.flags import Intents
import interactions
import json 
import os
import asyncio 
import traceback

with open('setting.json','r',encoding='utf8') as jfile:
    jdata = json.load(jfile)



#=======================interactions.py settings===========================
irtbot = interactions.Client(token=jdata['TOKEN'])

#load all extension
for filename in os.listdir("./cmds"):
    if filename.endswith(".py"):
        try:
            irtbot.load_extension(f'cmds.{filename[:-3]}')
        except Exception as e:
            print(f"Failed to load extension:{filename[:-3]}.", e)
            print(" Traceback:")
            traceback.print_exc()

#cmds-load extension
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

#cmds-unload extension
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

#cmds-reload extension
@interactions.slash_command(
    name="reloadets",
    description="reload extension",
    options=[
        interactions.SlashCommandOption(
            name="name",
            description="The extension name that you want to reload.",
            type=interactions.OptionType.STRING,
            required=True)
    ],
    default_member_permissions=interactions.Permissions.
    ADMINISTRATOR  #only ADMIN can use this cmd
)
async def reloadets(ctx, name):
    try:
        irtbot.reload_extension(f'cmds.{name}')
        await ctx.send(f'{name} extension has reloaded.')
    except:
        print(f'Error:Faild to reload extension:{name}.')
        await ctx.send(f'Error:Faild to reload extension:{name}.')

#cmds-help
@interactions.slash_command(
    name="help",
    description="Show all available commands."
)
async def help(ctx):
            cmds = irtbot.application_commands
            a = ''
            for ab in cmds:
                a = a + f'/{ab.name}\n'
            await ctx.send(f'指令名稱:\n{a}')

#event-startup
@interactions.listen()
async def Startup():
    print('main bot is ready')

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
    await channel.send(f"{member.mention}加入了伺服器! ")


@dcbot.event 
async def on_member_remove(member):
    channel = dcbot.get_channel(int(jdata['Msg_channel']))
    await channel.send(f"{member.mention}離開了伺服器!")


async def main():
    await asyncio.gather(
        dcbot.start(jdata['TOKEN']),
        irtbot.astart()
    )

asyncio.run(main())