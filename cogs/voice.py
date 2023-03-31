import os
import openai
import nextcord
from nextcord.ext import commands
from nextcord import FFmpegPCMAudio, AudioSource
import io
import sys
from pydub import AudioSegment



class VoiceTranscribeCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def transcribe(self, ctx: commands.Context):
        # Join the voice channel if the user is in one
        if ctx.author.voice and ctx.author.voice.channel:
            voice_channel = ctx.author.voice.channel
        else:
            await ctx.send("You need to be in a voice channel to use this command.")
            return

        voice_client = nextcord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if not voice_client:
            voice_client = await voice_channel.connect()

        # Voice recording logic
        audio_data = io.BytesIO()
        audio_source = FFmpegPCMAudio(executable='ffmpeg', pipe=True, stderr=sys.stderr)
        while not audio_source.is_opus():
            audio_data.write(await audio_source.read())

        audio_data.seek(0)
        audio = AudioSegment.from_file(audio_data, format='raw', sample_width=2, channels=1, frame_rate=48000)
        audio.export("audio.wav", format='wav')

        # Transcribe the audio using OpenAI API
        with open("audio.wav", "rb") as audio_file:
            transcript = openai.Audio.transcribe("whisper-1", audio_file)

        # Send the transcription as a message in the text channel
        await ctx.send(f"Transcription: {transcript}")

    @commands.command()
    async def leave(self, ctx: commands.Context):
        voice_client = nextcord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice_client and voice_client.channel:
            await voice_client.disconnect()
        else:
            await ctx.send("I'm not in a voice channel!")

def setup(bot: commands.Bot):
    bot.add_cog(VoiceTranscribeCog(bot))