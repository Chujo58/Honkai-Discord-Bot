import discord
from discord.ext import commands
import json


class on_join(commands.Cog, name='OnJoin'):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open('prefixes.json', 'r') as file:
            prefixes = json.load(file)
        
        prefixes[str(guild.id)] = '.' #Default prefix for every server.

        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, file, indent=4)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        with open('prefixes.json', 'r') as file:
            prefixes = json.load(file)

        prefixes.pop(str(guild.id))

        with open('prefixes.json', 'w') as file:
            json.dump(prefixes, file, indent=4)

    @commands.command(aliases=['prefix'])
    @commands.has_permissions(administrator=True)
    async def changeprefix(self, ctx, prefix=None):
        with open('prefixes.json', 'r') as file:
            prefixes = json.load(file)

        if prefix is None:
            await ctx.send(f"Your guild's prefix is `{prefixes[str(ctx.guild.id)]}`.")

        if prefix is not None:
            prefixes[str(ctx.guild.id)] = prefix
        
            with open('prefixes.json', 'w') as file:
                json.dump(prefixes, file, indent=4)
            
            await ctx.send(f"The guild's prefix has been changed to `{prefix}`.")

    @commands.slash_command(guild_ids=[817117856147439646], description='Changes the prefix for your guild.')
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, prefix=None):
        with open('prefixes.json', 'r') as file:
            prefixes = json.load(file)

        if prefix is None:
            await ctx.send(f"Your guild's prefix is `{prefixes[str(ctx.guild.id)]}`.")

        if prefix is not None:
            prefixes[str(ctx.guild.id)] = prefix
        
            with open('prefixes.json', 'w') as file:
                json.dump(prefixes, file, indent=4)
            
            await ctx.send(f"The guild's prefix has been changed to `{prefix}`.")
        
    


def setup(bot):
    bot.add_cog(on_join(bot))