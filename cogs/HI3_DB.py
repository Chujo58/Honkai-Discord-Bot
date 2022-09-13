import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
from PIL import Image
import urllib.request

URL = 'https://honkaiimpact3.fandom.com/wiki/Stigmata'

page = requests.get(url=URL)
soup = BeautifulSoup(page.content, 'html.parser')

#4★
FourStarsStigmataSets = soup.find('div', {'id':'mw-customcollapsible-4sets'}).find_all('div', {'class':'infobox-border'})
FourStarsEventStigmata = soup.find('div', {'id':'mw-customcollapsible-4eventSets'}).find_all('div', {'class':'infobox-border'})
FourStarsSingle = soup.find('div', {'id':'mw-customcollapsible-4singles'}).find_all('div', {'class':'infobox-border'})

#3★
ThreeStarsStigmataSets = soup.find('div', {'id':'mw-customcollapsible-3sets'}).find_all('div', {'class':'infobox-border'})
ThreeStarsSingle = soup.find('div', {'id':'mw-customcollapsible-3singles'}).find_all('div', {'class':'infobox-border'})

#2★
TwoStarsStigmataSets = soup.find_all('div', {'class':'infobox-border'})[-7:-2]

#1★
OneStarsStigmataSets = soup.find_all('div', {'class':'infobox-border'})[-2:]


AllStigmataSets = {}

def GetGenInfo(stig_list, stig_dict, rarity):
    for set in stig_list:
        stig_icons = set.find_all('div', {'class':'infobox-solid border-top border-bottom border-right border-left'})[0].find_all('a', href=True)

        set_name = set.find_all('div', {'class':'infobox-solid border-top border-bottom border-right border-left'})[1].find('a', href=True).string
        
        set_url = URL[0:URL.find('/wiki')] + set.find_all('div', {'class':'infobox-solid border-top border-bottom border-right border-left'})[1].find('a', href=True)['href']#Returns the new website to find all the information regarding the stigmata set.

        icons = []
        for icon in stig_icons:
            try:
                icon_url = icon.find('img')['data-src']#.get('data-src')
                icons.append(icon_url)
            except:
                icon_url = None
        
        stig_dict[set_name] = {'URL': set_url, 'ICONS': icons, 'RARITY': f'{rarity}★'}

#4★
GetGenInfo(FourStarsStigmataSets, AllStigmataSets, 4)
GetGenInfo(FourStarsEventStigmata, AllStigmataSets, 4)
GetGenInfo(FourStarsSingle, AllStigmataSets, 4)

#3★
GetGenInfo(ThreeStarsStigmataSets, AllStigmataSets, 3)
GetGenInfo(ThreeStarsSingle, AllStigmataSets, 3)

#2★
GetGenInfo(TwoStarsStigmataSets, AllStigmataSets, 2)

#1★
GetGenInfo(OneStarsStigmataSets, AllStigmataSets, 1)

def GetInfoFromURL(StigmataSetName):
    URL = AllStigmataSets[StigmataSetName]['URL']
    page = requests.get(url=URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    StigmataInformation = soup.find_all('div', {'class':'infobox-base'})
    stigmata_stats = soup.find_all('div', {'class':'cflex-nowrap'})

    StigInfos = {}

    all_stats = []
    for stigma in stigmata_stats:
        values = stigma.find_all('span')
        stats = ""
        for stat in values:
            #print(stat.string)
            stats += stat.string + ' '
        all_stats.append(stats)
    StigInfos['STATS'] = all_stats

    images = soup.find_all('a', {'class':'image'})[0:6]
    urls = []
    for image in images:
        urls.append(image.get('href'))

    StigInfos['IMAGE_URL'] = urls

    text = []
    for i in [3,5,7]:
        infos = StigmataInformation[i].find_all('div')
        for info in infos:
            text.append(info.text)
    text.append(StigmataInformation[8].find('div').text)

    StigInfos['TEXT'] = text

    stig_names_info = StigmataInformation[0].find_all('span', {'class':'tabberex-tab-header'})
    stig_names = []
    for name in stig_names_info:
        stig_names.append(name.text)
    StigInfos['NAMES'] = stig_names

    return StigInfos

def StackImage(first_image_url, second_image_url, stacked_image_name):
    urllib.request.urlretrieve(first_image_url, 'Images/Front.png')
    urllib.request.urlretrieve(second_image_url, 'Images/Back.png')
    front = Image.open('Images/Front.png')
    back = Image.open('Images/Back.png')
    back.paste(front, (0,0), front)
    back.save(stacked_image_name)

class HI3(commands.Cog, name='HI3'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def stigmata(self, ctx, set_name):
        set_gen_info = AllStigmataSets[set_name]
        rarity = set_gen_info['RARITY']
        icons = set_gen_info['ICONS']
        set_stats = GetInfoFromURL(set_name)
        images = set_stats['IMAGE_URL']
        names = set_stats['NAMES']
        text = set_stats['TEXT']
        stats = set_stats['STATS']
        
        
        index_front = []
        for value in range(0,len(images)):
            if value % 2 == 0:
                index_front.append(value)
        stig_pos = 0
        for index in index_front:
            if stig_pos == 0:
                StackImage(images[index], images[index+1], 'Images/T.png')
            if stig_pos == 1:
                StackImage(images[index], images[index+1], 'Images/M.png')
            if stig_pos == 2:
                StackImage(images[index], images[index+1], 'Images/B.png')
            stig_pos += 1           


        top_stig_embed = discord.Embed(title=" ", color=0xfc8e73)
        top_stig_embed.set_author(name=names[0], icon_url=icons[0])
        top_stig_embed.add_field(name='Max stats', value=stats[0], inline=False)
        top_stig_embed.add_field(name=f"Effect - {text[0]}", value=text[1], inline=False)
        T_png = discord.File('Images/T.png', filename='image.png')
        top_stig_embed.set_thumbnail(url="attachment://image.png")
        await ctx.send(file=T_png, embed=top_stig_embed)
        
        mid_stig_embed = discord.Embed(title=" ", color=0xa3abf3)
        mid_stig_embed.set_author(name=names[1], icon_url=icons[1])
        mid_stig_embed.add_field(name='Max stats', value=stats[1], inline=False)
        mid_stig_embed.add_field(name=f"Effect - {text[2]}", value=text[3], inline=False)
        M_png = discord.File('Images/M.png', filename='image2.png')
        mid_stig_embed.set_thumbnail(url="attachment://image2.png")
        await ctx.send(file=M_png, embed=mid_stig_embed)

        bot_stig_embed = discord.Embed(title=" ", color=0xb3c965)
        bot_stig_embed.set_author(name=names[2], icon_url=icons[2])
        bot_stig_embed.add_field(name='Max stats', value=stats[2], inline=False)
        bot_stig_embed.add_field(name=f"Effect - {text[4]}", value=text[5], inline=False)
        B_png = discord.File('Images/B.png', filename='image3.png')
        bot_stig_embed.set_thumbnail(url="attachment://image3.png")
        await ctx.send(file=B_png, embed=bot_stig_embed)
        
        set_effect_embed = discord.Embed(title=" ", color=0x8b47bf)
        set_effect_embed.set_author(name=f"{set_name} - {rarity}")
        set_effect_text = list(filter(None, text[6].split("\n")))
        set_effect_embed.add_field(name=set_effect_text[0], value=set_effect_text[1], inline=False)
        set_effect_embed.add_field(name=set_effect_text[2], value=set_effect_text[3], inline=False)
        await ctx.send(embed=set_effect_embed)


def setup(bot):
    bot.add_cog(HI3(bot))