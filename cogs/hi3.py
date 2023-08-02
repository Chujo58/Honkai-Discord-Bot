import discord
from discord.ext import commands
from discord import option
import bs4
import datetime
import requests
import rich.progress

STIG_URL = 'https://honkaiimpact3.fandom.com/wiki/Stigmata'

stig_page = requests.get(url=STIG_URL)
stig_soup = bs4.BeautifulSoup(stig_page.content, 'html.parser')

Header_H1 = stig_soup.find(id='firstHeading')

Headers_H2_3 = Header_H1.find_all_next(class_='mw-headline')
Stig_List_Headers = {}
Stig_List = {}

# rarity = ['4★','3★','2★','1★']

# Type_Header = [True if '★' in h.text else False for h in Headers_H2_3]
Type_Header = []
for header in Headers_H2_3:
    if "Stigmata" in header.text:
        Type_Header.append(True)
    else:
        Type_Header.append(False)
# for header in Headers_H2_3:
#     for rar in rarity:
#         if header.text == f"{rar} Stigmata":
#             Type_Header.append(True)
#             break
#         else:
#             Type_Header.append(False)

rarity = [h.text for index, h in enumerate(Headers_H2_3) if Type_Header[index]]

rar_count = 0
for i in range(0, len(Headers_H2_3)):
    if Type_Header[i]:
        Stig_List_Headers[Headers_H2_3[i].text] = []
        Stig_List[Headers_H2_3[i].text] = {}
        if rar_count == 0 and i == 0: rar_count = 0
        else: rar_count += 1
        if "2★ Stigmata" == Headers_H2_3[i].text or "1★ Stigmata" == Headers_H2_3[i].text:
            Stig_List_Headers[rarity[rar_count]].append(Headers_H2_3[i].find_parent('h1'))
            Stig_List[rarity[rar_count]]['Sets'] = {}
    else:
        Stig_List_Headers[rarity[rar_count]].append(Headers_H2_3[i].find_parent('h2'))
        Stig_List[rarity[rar_count]][Headers_H2_3[i].text] = {}


def get_single_info(list_of_td):
    url_img_h = list(list_of_td[0])[0]
    stig_name_h = list(list_of_td[0])[0]
    url_img = url_img_h.find('img').get('data-src')
    stig_name = stig_name_h.get('title')

    stats_h = list_of_td[1:-1]

    stats = ""
    stats = f"**HP** {stats_h[0].text[:-1]} | **ATK** {stats_h[1].text[:-1]} | **DEF** {stats_h[2].text[:-1]} | **CRT** {stats_h[3].text[:-1]} | **SP** {stats_h[4].text[:-1]}"

    effect_h = [i for i in list_of_td[-1]]
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
    previous_is_tag = False
    for item in effect_text_h:
        if type(item) == bs4.element.Tag and not previous_is_tag:
            effect_text += f"**{item.text}**"
            previous_is_tag = True
        elif type(item) == bs4.element.Tag and previous_is_tag:
            effect_text = effect_text[:-2]
            effect_text += f"{item.text}**"
            previous_is_tag = True
        else:
            effect_text += item.text
            previous_is_tag = False

    return (stig_name, stats, effect_name, effect_text, url_img)


def filter_display(tag):
    return tag.has_attr("style") and tag["style"] == "display: flex;"

def has_children(tag):
    return len(list(tag.children)) >= 1

def get_event_stig_info(one_div: bs4.PageElement):
    url_stig = STIG_URL.split("/wiki")[0] + one_div.find("div").find("a").get("href")
    stig_img_url = one_div.find("div").find("a").find("img").get("data-src")

    event_stig_page = requests.get(url=url_stig)
    event_stig_soup = bs4.BeautifulSoup(event_stig_page.content, "html.parser")

    data = event_stig_soup.find("div", class_="mw-parser-output")
    divs = data.find_all(filter_display)[0]
    data = divs.find("div").find("div")
    
    divs = data.find_all(has_children, recursive=False)[0:3]
    
    stig_name = divs[0].find("b").text
    
    url_img_h, stats_h = divs[1].find_all("div", recursive=False)
    url_img = url_img_h.find("a").get("href")
    stat_values = stats_h.find_all("div",recursive=False)[1].find_all("b")
    stats = f"**HP** {stat_values[0].text} | **ATK** {stat_values[1].text} | **DEF** {stat_values[2].text} | **CRT** {stat_values[3].text}"

    effect_name_h, effect_text_h = divs[2].find_all("div",recursive=False)
    effect_name = effect_name_h.text
    effect_text = ""
    for item in effect_text_h:
        if type(item) == bs4.element.Tag:
            effect_text += f"**{item.text}**"
        else:
            effect_text += item.text

    return (stig_name, stats, effect_name, effect_text, url_img, stig_img_url)


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

stigs_2_star_done = False
stigs_1_star_done = False

def get_table(rarity_, set_single):
    if rarity_ != '2★ Stigmata' and rarity_ != '1★ Stigmata':
            type_s = list(Stig_List[rarity_])[set_single]
            header = Stig_List_Headers[rarity_][set_single]
            has_effect = True
    else:
        header = Stig_List_Headers[rarity_][0]
        has_effect = False
        type_s = rarity_
        set_single = 0 #By default for 2★ and 1★ sets since they do not exist in singles.

    table = header.find_next('tbody')
    sets = table.find_all('tr')[1:]# [1:] since the first line is the header of the table.
    task_id = progress.add_task(f"{type_s}", total=len(sets))
    if set_single == 0:
        for index, stig_set in enumerate(sets):
            stigs = stig_set.find_all('td')
            info = get_set_info(stigs, has_effect)
            set_name = info[0]
            set_info = info[1:]
            if rarity_ == '2★ Stigmata' or rarity_ == '1★ Stigmata':
                Stig_List[rarity_]['Sets'][set_name] = set_info
            else:
                Stig_List[rarity_][type_s][set_name] = set_info

            progress.update(task_id, completed=index)
        progress.update(task_id, completed=len(sets))

    if (((set_single == 2 or set_single == 3 or set_single == 4) and rarity_ == "4★ Stigmata") or ((set_single == 1 or set_single == 2 or set_single == 3) and rarity_ != "4★ Stigmata")) :
        for index, stig_set in enumerate(sets):
            stig = stig_set.find_all('td')
            info = get_single_info(stig)
            stig_name = info[0]
            stig_info = info[1:]
            if rarity_ == "2★ Stigmata" or rarity_ == "1★ Stigmata":
                continue
            else:
                Stig_List[rarity_][type_s][stig_name] = stig_info

            progress.update(task_id, completed=index)
        progress.update(task_id, completed=len(sets))

    if set_single == 1 and rarity_ == "4★ Stigmata":
        table = header.find_next(id="mw-customcollapsible-4eventSets")
        sets_names = table.find_all("p")
        for stig_set in sets_names:
            stigs = stig_set.find_next("div").find_all(class_="infobox-border")
            for index, stig in enumerate(stigs):
                info = get_event_stig_info(stig)
                stig_name = info[0]
                stig_info = info[1:]
                if rarity_ == "2★ Stigmata" or rarity_ == "1★ Stigmata":
                    continue
                else:
                    Stig_List[rarity_][type_s][stig_name] = stig_info
                progress.update(task_id, completed=index)
            progress.update(task_id, completed=len(sets))

    # allan = sets[0].find_all('td')
    # print(get_set_info(allan)[3])

with rich.progress.Progress(
    rich.progress.TextColumn("{task.description}"),
    "•",
    "[progress.percentage]{task.percentage:>3.0f}%",
    rich.progress.BarColumn(),
    rich.progress.DownloadColumn(),
    "•",
    rich.progress.TimeRemainingColumn(
        compact=True,
        elapsed_when_finished=True),
    "•",
    rich.progress.TransferSpeedColumn(),
    "•",
    rich.progress.SpinnerColumn(finished_text="✔")
) as progress:
    for key in Stig_List.keys():
        get_table(key, 0)
        if key == "2★ Stigmata":
            stigs_2_star_done = True
        if key == "1★ Stigmata":
            stigs_1_star_done = True

        if key == "2★ Stigmata" and stigs_2_star_done:
            continue
        if key == "1★ Stigmata" and stigs_1_star_done:
            continue
        get_table(key, 2) if key == "4★ Stigmata" else get_table(key, 1)
        get_table(key, 3) if key == "4★ Stigmata" else get_table(key, 2)
        get_table(key, 4) if key == "4★ Stigmata" else get_table(key, 3)

    get_table("4★ Stigmata", 1)


WEAPON_URL = 'https://honkaiimpact3.fandom.com/wiki/Weapons'
weapon_page = requests.get(url=WEAPON_URL)
weapon_soup = bs4.BeautifulSoup(weapon_page.content, 'html.parser')

weapon_types = ['Pistols','Katanas','Cannons','Crosses','Greatswords','Gauntlets','Scythes','Lances','Bows','Chakrams',"Javelins"]
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
    weapon_name = weapon_gen_info.find('b').text
    weapon_rarity = weapon_gen_info.find('span')['title']

    print(main_div.find_all('div')[1].find_all('div')[0].find('div')) 
    

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

# get_weapon(WEAPON_URL.split("/wiki")[0]+'/wiki/Domain_of_Genesis')
# # get_weapons("https://honkaiimpact3.fandom.com/wiki/Pistols", "5★")

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
        stigs_for_autocomp = []
        for stig in list(Stig_List[chosen_rarity][chosen_type]):
            if len(self.value) > 1:
                if stig.startswith(self.value[0].upper() + self.value[1:].lower()):
                    stigs_for_autocomp.append(stig)
            else:
                if stig.startswith(self.value.upper()):
                    stigs_for_autocomp.append(stig)

        
        return stigs_for_autocomp


    @commands.slash_command(guild_ids=[817117856147439646],description="Find a stigmata")
    @option('rarity', description="Choose the rarity of the stigmata you're looking for.", autocomplete=discord.utils.basic_autocomplete(rarity))
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

        if "Sets" in stig_type and "Event Sets" not in stig_type:
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
            now = datetime.datetime.now().strftime('%Y/%m/%d %I:%M %p')

            BotIcon_png = discord.File("icon.png", filename="icon.png")
            Set_embed.set_footer(text=str(now), icon_url='attachment://icon.png')


            await ctx.respond(file=T_png, embed=T_embed)
            await ctx.send(file=M_png, embed=M_embed)
            await ctx.send(file=B_png, embed=B_embed)
            await ctx.send(file=BotIcon_png,embed=Set_embed)
            
        if "Singles" in stig_type:
            if "T-slot" in stig_type:
                embed = discord.Embed(title=" ", color=0xfc8e73)
                png = discord.File("Icons/icon_t.png", filename="t.png")
                embed.set_author(name=f"{stig_name}", icon_url="attachment://t.png")
                embed.add_field(name="Max stats", value=set_info[0], inline=False)

                embed.add_field(name=f":emote: Effect - {set_info[1]}".replace(':emote:', emojis['stigmata']), value=set_info[2], inline=False)
                embed.set_thumbnail(url=set_info[3])

                now = datetime.datetime.now().strftime("%Y/%m/%d %I:%M %p")
                BotIcon_png = discord.File("icon.png", filename="icon.png")
                embed.set_footer(text=str(now), icon_url="attachment://icon.png")

                await ctx.respond(files=[png,BotIcon_png], embed=embed)

            if "M-slot" in stig_type:
                embed = discord.Embed(title=" ", color=0xa3abf3)
                png = discord.File("Icons/icon_m.png", filename="m.png")
                embed.set_author(name=f"{stig_name}", icon_url="attachment://m.png")
                embed.add_field(name="Max stats", value=set_info[0], inline=False)

                embed.add_field(name=f":emote: Effect - {set_info[1]}".replace(':emote:', emojis['stigmata']), value=set_info[2], inline=False)
                embed.set_thumbnail(url=set_info[3])

                now = datetime.datetime.now().strftime("%Y/%m/%d %I:%M %p")
                BotIcon_png = discord.File("icon.png", filename="icon.png")
                embed.set_footer(text=str(now), icon_url="attachment://icon.png")

                await ctx.respond(files=[png,BotIcon_png], embed=embed)

            if "B-slot" in stig_type:
                embed = discord.Embed(title=" ", color=0xb3c965)
                png = discord.File("Icons/icon_b.png", filename="b.png")
                embed.set_author(name=f"{stig_name}", icon_url="attachment://b.png")
                embed.add_field(name="Max stats", value=set_info[0], inline=False)

                embed.add_field(name=f":emote: Effect - {set_info[1]}".replace(':emote:', emojis['stigmata']), value=set_info[2], inline=False)
                embed.set_thumbnail(url=set_info[3])

                now = datetime.datetime.now().strftime("%Y/%m/%d %I:%M %p")
                BotIcon_png = discord.File("icon.png", filename="icon.png")
                embed.set_footer(text=str(now), icon_url="attachment://icon.png")

                await ctx.respond(files=[png,BotIcon_png], embed=embed)

        if "Event Sets" in stig_type:
            if "(T)" in stig_name:
                color = 0xfc8e73

            if "(M)" in stig_name:
                color = 0xa3abf3

            if "(B)" in stig_name:
                color = 0xb3c965

            embed = discord.Embed(title=" ", color=color)
            embed.set_author(name=f"{stig_name}", icon_url=set_info[-1])
            embed.add_field(name="Max stats", value=set_info[0], inline=False)

            embed.add_field(name=f":emote: Effect - {set_info[1]}".replace(':emote:', emojis["stigmata"]), value=set_info[2], inline=False)
            embed.set_thumbnail(url=set_info[3])

            now = datetime.datetime.now().strftime("%Y/%m/%d %I:%M %p")
            BotIcon_png = discord.File("icon.png", filename="icon.png")
            embed.set_footer(text=str(now), icon_url="attachment://icon.png")

            await ctx.respond(files=[BotIcon_png] ,embed=embed)
            

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