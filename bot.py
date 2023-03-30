import discord
from discord.ext import commands
import os
import json

TOKEN = "MTAxNjgyNjI3MDcwNjgzMTM5MA.GgQzJh.xb_kFHNE6k6Lyb3pmJdsr-dmV0C6uVSEXPxf9I"
intents = discord.Intents().all()

"""class MyHelp(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Help")
        for cog, commands in mapping.items():
           command_signatures = [self.get_command_signature(c) for c in commands]
           if command_signatures:
                cog_name = getattr(cog, "qualified_name", "No Category")
                embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)"""

help_command = commands.DefaultHelpCommand(
    no_category = 'Commands'
)

def get_prefix(bot, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

bot = commands.Bot(command_prefix=get_prefix, help_command=help_command, intents=intents)

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

@bot.slash_command(guild_ids=[817117856147439646])
async def hello(ctx):
    await ctx.respond("Hello!")

@bot.command()
@commands.has_permissions(administrator=True)
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')

@bot.command()
@commands.has_permissions(administrator=True)
async def reload(ctx, extension):
    bot.load_extension(f'cogs.{extension}')

@bot.command()
@commands.has_permissions(administrator=True)
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        if filename == "HI3_DB.py":
            continue
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(TOKEN)