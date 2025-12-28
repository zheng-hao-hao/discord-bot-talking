import interactions
import google.generativeai as gemini
import json
import traceback

#=======================Gemini settings===========================
with open(".\setting.json","r",encoding='utf8') as jfile:
    jdata = json.load(jfile)

gemini.configure(api_key=jdata["GeminiAPI_key"])
model = gemini.GenerativeModel("gemini-3-flash-preview")
chat = model.start_chat(
    history=[
        {"role": "user", "parts": "Hello"},
        {"role": "model", "parts": "Great to meet you. What would you like to know?"},
    ]
)


class aichat(interactions.Extension):
   def __init__(self,client: interactions.Client):
      self.client = client
      
   @interactions.slash_command(
   name="aichat",
   description="Talk to Gemini",
   )
   @interactions.slash_option(
      name="message",  
            description="Talk to Gemini",  
            opt_type=interactions.OptionType.STRING,  
            required=True,
   )
   async def aichat(self,ctx,message: str):
    try:
        await ctx.defer()
        response = chat.send_message(message)
        response_text = response.text
        print(response_text)
        await ctx.send(response_text)

    except:
        await ctx.send("此內容不適用於此指令")
        traceback.print_exc()