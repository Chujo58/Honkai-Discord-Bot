import discord
from discord.ext import commands
import os
import json
import time
from discord import option

with open("key.txt", "r") as f:
    TOKEN = f.read()

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

help_command = commands.MinimalHelpCommand()

def get_prefix(bot, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

bot = commands.Bot(command_prefix=get_prefix, help_command=help_command, intents=intents)

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")

async def get_cogs(ctx):
    cogs = []
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            cogs.append(file[:-3])

    return cogs
    

@bot.slash_command(guild_ids=[817117856147439646],description="Loads an extension.")
@commands.has_permissions(administrator=True)
@option('extension',str,description="Extension chosen",autocomplete=get_cogs)
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    await ctx.respond(f"Loaded extension!")

@bot.slash_command(guild_ids=[817117856147439646],description="Reloads an extension.")
@commands.has_permissions(administrator=True)
@option('extension',str,description="Extension chosen",autocomplete=get_cogs)
async def reload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    time.sleep(0.01)
    bot.load_extension(f'cogs.{extension}')
    await ctx.respond(f"Reloaded extension!")

@bot.slash_command(guild_ids=[817117856147439646],description="Unloads an extension.")
@commands.has_permissions(administrator=True)
@option('extension',str,description="Extension chosen",autocomplete=get_cogs)
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    await ctx.respond(f"Unloaded extension!")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        if filename == "HI3_DB.py":
            continue
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(TOKEN)