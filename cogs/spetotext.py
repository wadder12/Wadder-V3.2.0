import nextcord
from nextcord.ext import commands
import asyncio
from gtts import gTTS
from io import BytesIO
import os
import tempfile

class TextToSpeech(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def tts(self, ctx, *, text: str):
        if ctx.author.voice:
            # Convert text to speech using gTTS
            tts = gTTS(text, lang="en")
            with tempfile.NamedTemporaryFile(delete=True) as fp:
                tts.save(fp.name)
                fp.seek(0)

            # Connect to the voice channel and start playing the audio
            voice_channel = ctx.author.voice.channel
            voice_client = await voice_channel.connect()

            audio_source = nextcord.FFmpegPCMAudio(fp.name)
            if not voice_client.is_playing():
                voice_client.play(audio_source, after=lambda e: print("Audio finished playing", e))

            # Wait for the audio to finish playing
            while voice_client.is_playing():
                await asyncio.sleep(1)

            # Disconnect from the voice channel
            await voice_client.disconnect()
        else:
            await ctx.send("Please join a voice channel to use this command.")


def setup(bot):
    bot.add_cog(TextToSpeech(bot))