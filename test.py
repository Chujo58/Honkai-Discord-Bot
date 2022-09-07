import discord
from discord.ext import commands

help_command = commands.DefaultHelpCommand(
    no_category = 'Commands'
)
intents = discord.Intents().all()

bot = commands.Bot(command_prefix="$", help_command=help_command, intents=intents)
TOKEN = "MTAxNjgyNjI3MDcwNjgzMTM5MA.GgQzJh.xb_kFHNE6k6Lyb3pmJdsr-dmV0C6uVSEXPxf9I"


@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')


@bot.command(command_prefix='$')
async def dosomething(ctx):
    await ctx.send("I did something")

bot.run(TOKEN)