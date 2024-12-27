from discord import integrations
import interactions
import random as rd

class cmds(interactions.Extension):
   def __init__(self,client: interactions.Client):
      self.client = client

   @interactions.slash_command(
    name="roll",
    description="luck :)",
    options=
      [
      interactions.SlashCommandOption
      (
          name="start",
          description="starting value",
          type=interactions.OptionType.INTEGER,
          required=True,
      ),
      interactions.SlashCommandOption
      (
          name="end",
          description="end value",
          type=interactions.OptionType.INTEGER,
          required=True,
      )
      ]
   )
   async def roll(self, ctx,start,end):
        num = rd.randint(start,end)
        await ctx.send(f"You rolled {num}!!!")