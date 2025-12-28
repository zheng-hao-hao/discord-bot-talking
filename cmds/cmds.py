from discord import integrations
import interactions
import random as rd

class cmds(interactions.Extension):
   def __init__(self,client: interactions.Client):
      self.client = client

   @interactions.slash_command(
    name="roll",
    description="luck :)",
   )
   @interactions.slash_option(
      name="start",
          description="starting value",
          opt_type=interactions.OptionType.INTEGER,
          required=True,
)
   @interactions.slash_option(
      name="end",
          description="end value",
          opt_type=interactions.OptionType.INTEGER,
          required=True,
   )
   async def roll(self, ctx,start,end):
        num = rd.randint(start,end)
        await ctx.send(f"You rolled {num}!!!")