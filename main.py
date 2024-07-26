import os
import base64

import discord
from discord import FFmpegPCMAudio, app_commands
from dotenv import load_dotenv
from openAIRequests import get_response_tutor, get_response_trump, get_god_response, \
    describe_image  # Correct import statement
from TTS import generateTTS  # Correct import statement

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_API = os.getenv('OPENAI_API')
intents = discord.Intents.all()


client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    print(f'Guilds: {client.guilds}')
    await tree.sync(guild=discord.Object(id=879917305298030642))


@client.slash_command(name='hello', help='Responds with a greeting')
async def hello(ctx: discord.ApplicationContext):
    response = "Hello! How are you today?"
    await ctx.respond(response)


@client.command(name="Donald", help="Talk to Donald Trump")
async def donald(ctx: discord.ApplicationContext, *, message: str):
    response = get_response_trump(message, ctx.author.name)
    await ctx.send(ctx.author.mention + " " + response)


@client.slash_command(name="help", description="Get a list of available commands")
async def help(ctx):
    help_message = "Available commands:\n"
    for command in bot.commands:
        help_message += f"/{command.name}: {command.description}\n"
    await ctx.respond(help_message)


@client.slash_command(name="generate_tts", description="Generate a TTS audio file")
async def generate_tts(ctx: discord.ApplicationContext, *, message: str):
    await ctx.defer()
    response = get_response_trump(message, ctx.author.name)
    generateTTS(response)

    # Send the audio file
    with open('./resources/TTS/audio_file.wav', 'rb') as f:
        await ctx.respond(file=discord.File(f, 'audio_file.wav'))


@client.command(name="tutor", description="Ask a tutor for help in Political Science")
async def tutor(ctx: discord.ApplicationContext, *, message: str):
    response = get_response_tutor(message, ctx.author.name)
    await ctx.send(ctx.author.mention + " " + response)


@client.command(name="God", help="Talk to God")
async def god(ctx: discord.ApplicationContext, *, message: str):
    response = get_god_response(message, ctx.author.name)
    await ctx.send(ctx.author.mention + " " + response)


@client.command(name="join", help="Join a voice channel")
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.message.author.voice.channel
        if ctx.voice_client is not None:
            await ctx.voice_client.move_to(channel)
        else:
            voice = await channel.connect()
            print(voice)
        source = FFmpegPCMAudio('./resources/TTS/audio_file.wav', **FFMPEG_OPTIONS)
        print(source)
        def after_playing(error):
            if error:
                print(f'Error after playing audio: {error}')
        voice.play(source, after=after_playing)
    else:
        await ctx.send("You are not in a voice channel.")

@client.command(name="leave", help="Leave a voice channel")
async def leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
    else:
        await ctx.send("I am not in a voice channel.")

# @bot.command(name="trump_speak", help="Have Donald Trump speak")
# async def trump_speak(ctx: discord.ApplicationContext, *, message: str):
#     if ctx.voice_client is None:
#         await ctx.send("I am not in a voice channel, please use the !vc command to join a voice channel.")
#         return
#
#     response = get_response_trump(message, ctx.author.name)
#     generateTTS(response)
#     audio_file = './resources/TTS/audio_file.wav'
#
#     if not ctx.voice_client.is_playing():
#         ctx.voice_client.play(audio_file, after=lambda e: print(f'Finished playing: {e}'))
#         await ctx.send("Playing the voice line!")
#     else:
#         await ctx.send("Already playing audio, please wait.")


@client.command(name="show_trump", help="Show a picture of Donald Trump")
async def show_trump_a_picture(ctx: discord.ApplicationContext, message=None):
    image = ctx.message.attachments[0].url

    response = describe_image(image)
    await ctx.send(response)


# bot.loop.create_task(trump_initiate_random_argument())
client.run(TOKEN)
