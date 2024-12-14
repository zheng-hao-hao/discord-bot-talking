import interactions
import google.generativeai as gemini
import json
import os

#=======================Gemini settings===========================
with open("D:\\vs_code\discord-bot-talking\setting.json","r",encoding='utf8') as jfile:
    jdata = json.load(jfile)

gemini.configure(api_key=jdata["GeminiAPI_key"])
model = gemini.GenerativeModel("gemini-1.5-flash")
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
   options=[
        interactions.SlashCommandOption(
            name="message",  
            description="Talk to Gemini",  
            type=interactions.OptionType.STRING,  
            required=True,  
        ),
    ],
   )
   async def aichat(self,ctx,message: str):
    response = chat.send_message(message)
    response_text = response.text
    await ctx.send(response_text)