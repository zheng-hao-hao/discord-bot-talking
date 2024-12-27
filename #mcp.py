import interactions
import requests
from bs4 import BeautifulSoup as bs4
from interactions.api.voice.audio import AudioVolume

class Play(interactions.Extension):
    def __init__(self, client: interactions.Client):
        self.client = client

    @interactions.listen()
    async def on_startup(self):
        print("Music Player is ready")

    @interactions.slash_command(
        name="play",
        description="Play music in a voice channel",
        options=[
            interactions.SlashCommandOption(
                name="URL or keyword",
                description="Input URL or keyword to play music",
                type=interactions.OptionType.STRING,
                required=True,
            )
        ],
    )
    async def play_music(self, ctx: interactions.CommandContext, input: str):
        if not ctx.author.voice:
            await ctx.send("你不在語音頻道中!")
            return

        if not ctx.voice_state:
            await ctx.author.voice.channel.connect()  # Join the user's voice channel

        try:
            # In a real implementation, you'd process `input` for URL or keywords
            audio = AudioVolume(input)  # Replace with actual audio processing
            await ctx.send(f"Now Playing: **{audio}**")
        except Exception as e:
            await ctx.send(f"Error playing music: {str(e)}")
