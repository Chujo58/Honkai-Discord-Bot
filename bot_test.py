import discord
from discord.ext import commands
import os
import json

with open("key.txt", "r") as f:
    TOKEN = f.read()

intents = discord.Intents().all()

help_command = commands.MinimalHelpCommand()

bot = commands.Bot(command_prefix="$", help_command=help_command, intents=intents)

@bot.event
async def on_ready():
    print("Bot is ready")

@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    print(bot.get_message(payload.message_id))
    print(payload.emoji)

bot.run(TOKEN)