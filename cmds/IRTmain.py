import interactions

class IRTmain(interactions.Extension):
   def __init__(self,client: interactions.Client):
      self.client = client
      
   @interactions.slash_command(
   name="test",
   description="Test bot"
   )
   async def test(self, ctx):
       await ctx.send("bot is online")