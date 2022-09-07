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
    for i in [1,3,5,7]:
        infos = StigmataInformation[i].find_all('div')
        for info in infos:
            text.append(info.text)
    text.append(StigmataInformation[8].find('div').text)

    StigInfos['TEXT'] = text
    return StigInfos

def StackImage(first_image_url, second_image_url, stacked_image_name):
    urllib.request.urlretrieve(first_image_url, 'Front.png')
    urllib.request.urlretrieve(second_image_url, 'Back.png')
    front = Image.open('Front.png')
    back = Image.open('Back.png')
    back.paste(front, (0,0), front)
    back.save(stacked_image_name)

class HI3(commands.Cog, name='HI3'):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(guild_ids=[817117856147439646])
    async def stigmata(self, ctx, set_name):
        set_gen_info = AllStigmataSets[set_name]
        rarity = set_gen_info['RARITY']
        icons = set_gen_info['ICONS']
        set_stats = GetInfoFromURL(set_name)
        images = set_stats['IMAGE_URL']
        
        if len(images) == 6:
            index_front = []
            for value in range(0,6):
                if value % 2 == 0:
                    index_front.append(value)
            stig_pos = 0
            for index in index_front:
                if stig_pos == 0:
                    StackImage(images[index], images[index+1], 'T.png')
                if stig_pos == 1:
                    StackImage(images[index], images[index+1], 'M.png')
                if stig_pos == 2:
                    StackImage(images[index], images[index+1], 'B.png')
                stig_pos += 1

        