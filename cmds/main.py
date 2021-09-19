import discord
from discord.ext import commands
from core.classes import Cog_Extension
import time

class Main(Cog_Extension):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def test(self,ctx):
         await ctx.send(f"testing")
    @commands.command()
    async def clean(self,ctx,num:int):
        await ctx.channel.purge(limit=num+1)
    @commands.command()
    async def tclean(self,ctx,num:int):
        while 1==1:
            await ctx.channel.purge(limit=num+1)
            await ctx.send(f"@everyone 本頻道將在一小時後定時清除")
            time.sleep(3600)

        
        
    
def setup(bot):
    bot.add_cog(Main(bot))
