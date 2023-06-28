import discord
from discord.ext import commands
from discord import option
import bs4
import datetime
import requests

STIG_URL = 'https://honkaiimpact3.fandom.com/wiki/Stigmata'

stig_page = requests.get(url=STIG_URL)
stig_soup = bs4.BeautifulSoup(stig_page.content, 'html.parser')

Header_H1 = stig_soup.find(id='firstHeading')

Headers_H2_3 = Header_H1.find_all_next(class_='mw-headline')
Stig_List_Headers = {}
Stig_List = {}

rarity = ['4★','3★','2★','1★']

Type_Header = [True if '★' in h.text else False for h in Headers_H2_3]

rar_count = 0
for i in range(0, len(Headers_H2_3)):
    if Type_Header[i]:
        Stig_List_Headers[Headers_H2_3[i].text] = []
        Stig_List[Headers_H2_3[i].text] = {}
        if rar_count == 0 and i == 0: rar_count = 0
        else: rar_count += 1
        if "2★" == Headers_H2_3[i].text or "1★" == Headers_H2_3[i].text:
            Stig_List_Headers[rarity[rar_count]].append(Headers_H2_3[i].find_parent('h2'))
            Stig_List[rarity[rar_count]]['Sets'] = {}
    else:
        Stig_List_Headers[rarity[rar_count]].append(Headers_H2_3[i].find_parent('h3'))
        Stig_List[rarity[rar_count]][Headers_H2_3[i].text] = {}

print(Stig_List)

def get_single_info(list_of_td):
    url_img_h = list(list_of_td[0])[0]
    stig_name_h = list(list_of_td[0])[2]

    stats_h = list_of_td[1:5]
    stats = f"**HP** {stats_h[0].text} | **ATK** {stats_h[1].text} | **DEF** {stats_h[2].text} | **CRT** {stats_h[3].text}"

    effect_h = [i for i in list_of_td[5]]
    effect_name_h = []
    effect_text_h = []
    is_div = [True if item.name == 'div' else False for item in effect_h]
    
    counter = 0
    for index, item in enumerate(is_div):
        if not item:
            if counter == 0:
                effect_name_h.append(effect_h[index])
            if counter == 1:
                effect_text_h.append(effect_h[index])
        else:
            counter += 1

    effect_name = effect_name_h[0].text
    effect_text = ""
    for item in effect_text_h:
        if type(item) == bs4.element.Tag:
            effect_text += f"**{item.text}**"
        else:
            effect_text += item.text


def get_stig_info(one_td, has_effect):
    # print(list(one_td))
    list_ = [i for i in one_td]
    is_div = [True if item.name == 'div' or item.name == 'hr' else False for item in list_]
    numb_divs = is_div.count(True)

    counter = 0
    url_img_h = []
    stig_name_h = []
    stats_h = []
    effect_name_h = []
    effect_text_h = []
    for index, item in enumerate(is_div):
        if index == len(is_div) - 1:
            if item:
                effect_h = list(list_[index])
                effect_name_h.append(effect_h[0])
                effect_text_h = [i for i in effect_h[2:]]
        if not item:
            if counter == 0:
                url_img_h.append(list_[index])
            if counter == 1:
                stig_name_h.append(list_[index])
            if counter == 2:
                stats_h.append(list_[index])
            if counter == 3:
                effect_name_h.append(list_[index])
            if counter == 4:
                effect_text_h.append(list_[index])
        else:
            counter = counter + 1 if counter <= numb_divs else numb_divs

    url_img = url_img_h[0].find('img').get('data-src')
    stig_name = stig_name_h[0].text + stig_name_h[1].text if len(stig_name_h) > 1 else stig_name_h[0].text

    stats = ""
    for stat in stats_h:
        if type(stat) == bs4.element.Tag:
            stats += f"**{stat.text}**"
        else:
            stats += stat.text

    if has_effect:
        effect_name = effect_name_h[0].text
        effect_text = ""
        for item in effect_text_h:
            if type(item) == bs4.element.Tag:
                effect_text += f"**{item.text}**"
            else:
                effect_text += item.text

        return (stig_name, stats, effect_name, effect_text, url_img)

    else:
        return (stig_name, stats, url_img)


def get_set_effect(one_td):
    list_ = [i for i in one_td]
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

    effect_name = effect_name.strip('\n')
    effect_text = effect_text.strip('\n')
    return set_2_name, effect_name, effect_text


def get_set_info(list_of_td, has_effect):
    top_stig, mid_stig, bot_stig, set_2, set_3 = list_of_td
    
    top_stig_info = get_stig_info(top_stig, has_effect)
    mid_stig_info = get_stig_info(mid_stig, has_effect)
    bot_stig_info = get_stig_info(bot_stig, has_effect)

    set_2_effect = get_set_effect(set_2)
    set_3_effect = get_set_effect(set_3)

    set_name = top_stig_info[0][:-4]

    return set_name, top_stig_info, mid_stig_info, bot_stig_info, set_2_effect, set_3_effect


def get_table(rarity_, set_single):
    if rarity_ != '2★' and rarity_ != '1★':
            type_s = list(Stig_List[rarity_])[set_single]
            header = Stig_List_Headers[rarity_][set_single]
            has_effect = True
    else:
        header = Stig_List_Headers[rarity_][0]
        has_effect = False
    table = header.find_next('tbody')
    sets = table.find_all('tr')[1:]# [1:] since the first line is the header of the table.
    for stig_set in sets:
        stigs = stig_set.find_all('td')
        info = get_set_info(stigs, has_effect)
        set_name = info[0]
        set_info = info[1:]
        if rarity_ == '2★' or rarity_ == '1★':
            Stig_List[rarity_]['Sets'][set_name] = set_info
        else:
            Stig_List[rarity_][type_s][set_name] = set_info
    # allan = sets[0].find_all('td')
    # print(get_set_info(allan)[3])

for key in Stig_List.keys():
    print(key)
    get_table(key, 0)
# get_table(rarity[0], 0)
# get_table(rarity[1], 0)
# get_table(rarity[2], 0)
# get_table(rarity[3], 0)


WEAPON_URL = 'https://honkaiimpact3.fandom.com/wiki/Weapons'
weapon_page = requests.get(url=WEAPON_URL)
weapon_soup = bs4.BeautifulSoup(weapon_page.content, 'html.parser')

weapon_types = ['Pistols','Katanas','Cannons','Crosses','Greatswords','Gauntlets','Scythes','Lances','Bows','Chakrams']
weapon_urls = []
weapon_rarity = ['5★','4★','3★','2★','1★']

def is_weapon(tag):
    if tag.has_attr('title'):
        if tag['title'] in weapon_types:
            return True
    
def get_urls(list_):
    items = weapon_soup.find_all(is_weapon)
    previous_href = ""
    for item in items:
        href = item['href']
        if href == previous_href:
            continue
        else:
            list_.append(WEAPON_URL[:-13]+href)
            previous_href = href

get_urls(weapon_urls)

def get_weapon(url):
    url_page = requests.get(url=url)
    url_soup = bs4.BeautifulSoup(url_page.content, 'html.parser')
    main_div = url_soup.find(class_='mw-parser-output').find_next('div')
    weapon_gen_info = main_div.find_all('div')[0]
    print(weapon_gen_info.find('b').text, weapon_gen_info.find('span')['title'])
    

def get_weapons(url, rarity):
    url_page = requests.get(url=url)
    url_soup = bs4.BeautifulSoup(url_page.content, 'html.parser')
    headers_h2 = url_soup.find_all('h2')
    header_to_use = None
    for header in headers_h2:
        if rarity in header.text:
            header_to_use = header
            break
    
    for s in header_to_use.find_next_siblings():
        if s.name == 'div':
            divs = s.find_all('div')
            weapon_url = divs[0].find('a')['href']
            print(weapon_url)
            # print(weapon_name, weapon_stats)
            
        else:
            break

get_weapon(WEAPON_URL[:-13]+'/wiki/Domain_of_Genesis')

emojis = None

class HI3(commands.Cog, name='HI3'):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def stig_type_autocomp(self):
        chosen_rarity = self.options['rarity']
        return list(Stig_List[chosen_rarity])

    @staticmethod
    def stig_list_autocomp(self):
        chosen_rarity = self.options['rarity']
        chosen_type = self.options['stig_type']
        return [stig for stig in list(Stig_List[chosen_rarity][chosen_type]) if stig.startswith(self.value.upper())]


    @commands.slash_command(guild_ids=[817117856147439646],description="Find a stigmata")
    @option('rarity', description="Choose the rarity of the stigmata you're looking for.", autocomplete=discord.utils.basic_autocomplete(['4★','3★','2★','1★']))
    @option('stig_type', description="The type of stigmata you're looking for.", autocomplete=stig_type_autocomp)
    @option('stig_name', description="The stigmata's name.", autocomplete=stig_list_autocomp)
    async def stigmata(self, ctx, rarity, stig_type, stig_name):
        set_info = Stig_List[rarity][stig_type][stig_name]

        has_effect = True if len(set_info[0]) != 3 else False

        global emojis
        if not emojis:
            emojis = {e.name:str(e) for e in ctx.bot.emojis}

        glowstar = discord.utils.get(ctx.bot.emojis, name='glowstar')

        rar_set = int(rarity[0])
        if rar_set == 4:
            rar_string = ":emote1::emote1::emote1::emote1::emote2:"
        if rar_set == 3:
            rar_string = ":emote1::emote1::emote1::emote2::emote2:"
        if rar_set == 2:
            rar_string = ":emote1::emote1::emote2::emote2::emote2:"
        if rar_set == 1:
            rar_string = ":emote1::emote2::emote2::emote2::emote2:"

        T_embed = discord.Embed(title=" ", color=0xfc8e73)
        T_png = discord.File('Icons/icon_t.png', filename='t.png')
        T_embed.set_author(name=f"{set_info[0][0]}", icon_url='attachment://t.png')
        T_embed.add_field(name="Max stats", value=set_info[0][1], inline=False)
        if has_effect:
            T_embed.add_field(name=f":emote: Effect - {set_info[0][2]}".replace(':emote:', emojis['stigmata']), value=set_info[0][3], inline=False)
            T_embed.set_thumbnail(url=set_info[0][4])
        else:
            T_embed.set_thumbnail(url=set_info[0][2])

        M_embed = discord.Embed(title=" ", color=0xa3abf3)
        M_png = discord.File('Icons/icon_m.png', filename='m.png')
        M_embed.set_author(name=f"{set_info[1][0]}", icon_url='attachment://m.png')
        M_embed.add_field(name="Max stats", value=set_info[1][1], inline=False)
        if has_effect:
            M_embed.add_field(name=f":emote: Effect - {set_info[1][2]}".replace(':emote:', emojis['stigmata']), value=set_info[1][3], inline=False)
            M_embed.set_thumbnail(url=set_info[1][4])
        else:
            M_embed.set_thumbnail(url=set_info[1][2])

        B_embed = discord.Embed(title=" ", color=0xb3c965)
        B_png = discord.File('Icons/icon_b.png', filename='b.png')
        B_embed.set_author(name=f"{set_info[2][0]}", icon_url='attachment://b.png')
        B_embed.add_field(name="Max stats", value=set_info[2][1], inline=False)
        if has_effect:
            B_embed.add_field(name=f":emote: Effect - {set_info[2][2]}".replace(':emote:', emojis['stigmata']), value=set_info[2][3], inline=False)
            B_embed.set_thumbnail(url=set_info[2][4])
        else:
            B_embed.set_thumbnail(url=set_info[2][2])

        Set_embed = discord.Embed(title=f"{stig_name} - {rar_string.replace(':emote1:', emojis['glowstar']).replace(':emote2:',emojis['emptystar'])}", color=0x8b47bf)
        # Set_embed.set_author(name=f"{stig_name} - ")
        Set_embed.add_field(name=f"{set_info[3][0]} - {set_info[3][1]}", value=set_info[3][2], inline=False)
        Set_embed.add_field(name=f"{set_info[4][0]} - {set_info[4][1]}", value=set_info[4][2], inline=False)
        now = datetime.datetime.now().strftime('%m/%d/%Y %I:%M %p')
        Set_embed.set_footer(text=str(now))


        await ctx.respond(file=T_png, embed=T_embed)
        await ctx.send(file=M_png, embed=M_embed)
        await ctx.send(file=B_png, embed=B_embed)
        await ctx.send(embed=Set_embed)
        
    # @commands.slash_command(guild_ids=[817117856147439646],description="Find a weapon.")  
    # # @option('weapon_type', description="Type of weapon looked for.", autocomplete=discord.utils.basic_autocomplete(['Cannons','Crosses','Greatswords','Gauntlets','Scythes','Lances','Bows','Chakrams']))
    # async def weapon(self, ctx, type_):
    #     await ctx.respond(f"You choose {type_}.")

    @commands.slash_command(guild_ids=[817117856147439646],description="Find a weapon")
    @option('weapon_type',str,description="Type of weapon looked for.", autocomplete=discord.utils.basic_autocomplete(weapon_types))
    async def weapon(self, ctx, weapon_type):
        index = weapon_types.index(weapon_type)
        await ctx.respond(weapon_urls[index])


    @commands.slash_command(guild_ids=[817117856147439646])
    async def test5(self, ctx):
        global emojis
        if not emojis:
            emojis = {e.name:str(e) for e in ctx.bot.emojis}
        rar_string = ":emote1::emote1::emote1::emote1::emote2:"
        await ctx.respond(rar_string.replace(':emote1:', emojis['glowstar']).replace(":emote2:", emojis['emptystar']))
        
    @commands.command()
    async def debug(self, ctx, emoji):
        embed = discord.Embed(description=f"emoji: {emoji}", title=f"emoji: {emoji}")
        embed.add_field(name="id", value='lol')
        # embed.add_field(name="name", value=repr(emoji.name))
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(HI3(bot))