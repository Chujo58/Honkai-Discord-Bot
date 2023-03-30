import discord
from discord.ext import commands
from discord import option
import requests
from bs4 import BeautifulSoup
import bs4
from PIL import Image
import urllib.request

URL = 'https://honkaiimpact3.fandom.com/wiki/Stigmata'

page = requests.get(url=URL)
soup = BeautifulSoup(page.content, 'html.parser')

header_1 = soup.find(id="Stigmata_List")
title = soup.title.text

test = header_1.find_all_next(class_="mw-headline")
Stig_List_H = {}
Stig_List = {}

rarity = ['4★','3★','2★','1★']
current = 0
loop = 0
for h in test:
    if '★' in h.text:
        Stig_List_H[h.text] = []
        Stig_List[h.text] = {} 
        if loop == 0:
            current = 0
        else:
            current += 1
        if '2★' == h.text or '1★' == h.text:
            Stig_List_H[rarity[current]].append(h.find_parent('h2'))
    else:
        loop += 1
        Stig_List[rarity[current]][h.text] = []
        Stig_List_H[rarity[current]].append(h.find_parent('h3'))


# table = soup.find_all('tbody')[4]
SetsH_4 = Stig_List_H['4★'][0]
table = SetsH_4.find_next('tbody')
sets = table.find_all('tr')[1:]
allan = sets[1].find_all('td')
td = allan[3]
list_ = [i for i in td]

is_div = [True if item.name == 'div' or item.name == 'hr' else False for item in list_]
numb_divs = is_div.count(True)

counter = 0
set_2_name_h = []
effect_name_h = []
effect_text_h = []

for index, item in enumerate(is_div):
    if not item:
        if counter == 0:
            set_2_name_h.append(list_[index])
        if counter == 1:
            effect_name_h.append(list_[index])
        if counter == 2:
            effect_text_h.append(list_[index])
    else:
        counter = counter + 1 if counter <= numb_divs else numb_divs

set_2_name = set_2_name_h[0].text
effect_name = effect_name_h[0].text
effect_text = ""
for item in effect_text_h:
    if type(item) == bs4.element.Tag:
        effect_text += f"**{item.text}**"
    else:
        effect_text += item.text

print(set_2_name)
print(effect_name)
print(effect_text)

# counter = 0
# url_img_h = []
# stig_name_h = []
# stats_h = []
# effect_name_h = []
# effect_text_h = []
# for index, item in enumerate(is_div):
#     if index == len(is_div) - 1:
#         if item:
#             effect_h = list(list_[index])
#             effect_name_h.append(effect_h[0])
#             effect_text_h = [i for i in effect_h[2:]]
#     if not item:
#         if counter == 0:
#             url_img_h.append(list_[index])
#         if counter == 1:
#             stig_name_h.append(list_[index])
#         if counter == 2:
#             stats_h.append(list_[index])
#         if counter == 3:
#             effect_name_h.append(list_[index])
#         if counter == 4:
#             effect_text_h.append(list_[index])

#     else:
#         counter = counter + 1 if counter <= numb_divs else numb_divs

# url_img = url_img_h[0].find('img').get('data-src')
# stig_name = stig_name_h[0].text

# stats = ""
# for stat in stats_h:
#     if type(stat) == bs4.element.Tag:
#         stats += f"**{stat.text}**"
#     else:
#         stats += stat.text

# effect_name = effect_name_h[0].text
# effect_text = ""
# for item in effect_text_h:
#     if type(item) == bs4.element.Tag:
#         effect_text += f"**{item.text}**"
#     else:
#         effect_text += item.text


# print(stig_name)
# print(stats)
# print(effect_name)
# print(effect_text)


# emojis = None

# class HI3(commands.Cog, name='HI3'):
#     def __init__(self, bot):
#         self.bot = bot

#     @commands.slash_command(guild_ids=[817117856147439646])
#     async def test(self, ctx):
#         global emojis
#         if not emojis:
#             emojis = {e.name:str(e) for e in ctx.bot.emojis}

#         stig_embed = discord.Embed(title=" ", color=0xfc8e73)
#         T_png = discord.File('Icons/icon_t.png', filename='image.png')
#         stig_embed.set_author(name=stig_name, icon_url='attachment://image.png')
#         stig_embed.add_field(name='Max stats', value=stats, inline=False)
#         stig_embed.add_field(name=f':emote: Effect - {effect_name}'.replace(':emote:',emojis['stigmata']), value=effect_text, inline=False)
#         stig_embed.set_thumbnail(url=url)
#         await ctx.send(file=T_png,embed=stig_embed)

#     @commands.slash_command(guild_ids=[817117856147439646])
#     @option('set_rarity', description="Choose the rarity of the set you're looking for.", autocomplete=discord.utils.basic_autocomplete(['4★','3★','2★','1★']))
#     async def stigmata(self, ctx, set_rarity):
#         await ctx.respond(f"You chose {set_rarity}!")

#     @commands.slash_command(guild_ids=[817117856147439646])
#     async def test2(self, ctx):
#         global emojis
#         if not emojis:
#             emojis = {e.name:str(e) for e in ctx.bot.emojis}
#         await ctx.respond(f"Test :emote:".replace(':emote:', emojis['stigmata']))

# def setup(bot):
#     bot.add_cog(HI3(bot))