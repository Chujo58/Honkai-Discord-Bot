import requests
from bs4 import BeautifulSoup
import numpy as np

URL = 'https://honkaiimpact3.fandom.com/wiki/Stigmata'

page = requests.get(url=URL)
soup = BeautifulSoup(page.content, 'html.parser')
#-----
#We want to sort through all the stigmata sets.
#We will have a dictionary holding all the sets' name as keys and another dictionary holding the stigma piece as keys and url as value.
#-----
body = soup.find('body')

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
    stig_pos = ['(T)','(M)','(B)']
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

    #images = soup.find_all('a', {'class':'image'})[0:6]
    urls = []
    #for image in images:
        #urls.append(image.get('href'))


    print(soup.find('img', width=720, height=720, alt=StigmataSetName+' (B).png')['src'])
    for position in stig_pos:
        url = soup.find('img', width=720, height=720, alt=StigmataSetName+f' {position}.png')['src']
        urls.append(url)
    StigInfos['IMAGE_URL'] = urls
    
    text = []
    #print(StigmataInformation[0].find_all('div'))

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

Allan_poe = GetInfoFromURL('Allan Poe')
#print(list(filter(None, Allan_poe['TEXT'][10].split("\n"))))
print(Allan_poe['IMAGE_URL'])

