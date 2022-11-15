# --------------------------------------------------
# WikiBot (Version 2.1)
# by Sha-chan~
# last version released on the 23 of May 2021
#
# code provided with licence :
# GNU General Public Licence v3.0
# --------------------------------------------------

import discord
import os
import libs.wikibot_lib as wl

from random import randint

client = discord.Client()
__version__ = "1.2.1"


def make_embed(title, description, field, color, image, in_line = False, thumb = False):
    if not color: color = randint(0, 16777215)
    answer = discord.Embed(title=title, description=description, color=color)

    for i in field:
        answer.add_field(name=i[0], value=i[1], inline=in_line)
    
    if image:
        if thumb: answer.set_thumbnail(url=image)
        else: answer.set_image(url=image)
    return answer

@client.event
async def on_message(message):
    msg_content, rep = message.content, None

    if message.author == client.user: return None

    try:
        if msg_content[0] != "^": return None
    except:
        return None

    msg_content = list(msg_content[1:].partition("^"))

    msg_content[0] = msg_content[0].rstrip()

    language = msg_content[2].strip().rstrip()
    
    if not language:
        language = "he"
    wl.wikipedia.set_lang(language.split()[0])

    if not msg_content[0].find("r "):
        rep = make_embed(*wl.page_random(msg_content[0][2:]))
        
    elif not msg_content[0].find("w- "):
        rep = make_embed(*wl.page_read(msg_content[0][2:], True))

    elif not msg_content[0].find("w "):
        rep = make_embed(*wl.page_read(msg_content[0][2:]))

    elif not msg_content[0].find("w+ "):
        rep = make_embed(*wl.page_search(msg_content[0][2:]))

    elif not msg_content[0].find("c "):
        city_name = msg_content[0][2:]
        rep, img, day, timezone, datetime = wl.weather(city_name, language)
        
        if not rep:
            rep = make_embed("Weather", "Unknown city's name", [("Error", f"No city were found for the name : '{city_name}'. Please check the city's name.")], 16711680, None)
        else:
            if day == 0: day = f"today : {datetime}"
            elif day == 1: day = f"tomorrow : {datetime}"
            else: day = f"in {day} days : {datetime}"
            rep = make_embed("Weather", f"{city_name} {day} ({timezone})", rep, None, img, True, True)

            rep.set_footer(text = "Weather forecast provided by OpenWeather", icon_url = "https://openweathermap.org/themes/openweathermap/assets/img/logo_white_cropped.png")

    elif not msg_content[0].find("n "):
        name, news = wl.get_news(msg_content[0][2:], language)
        embed_title = f"**{name}**"
        if news[0]:
            news = news[0]
            rep = []
            for index, article in enumerate(news):
                rep.append(make_embed(f"{embed_title} (#{index + 1})", article[0], (("סיכום המאמר", article[1]), ("קישור למאמר המלא", article[2])), None, article[3]))
        else:
            rep = make_embed(embed_title, "אתר חדשות לא ידוע", (("שגיאה", "אתר החדשות המבוקש אינו במאגר"), ("אתרי חדשות זמינים", " - ".join(news[1]))), 16711680, None)
        
    elif msg_content[0] == "עזרה":
        rep = discord.Embed(title=f"לוח עזרה (ויקיבוט גרסה {__version__})", description="רשימה של  פקודות זמינות:", color=randint(0, 16777215))
        rep.add_field(name="חיפוש ערך בוויקיפדיה", value="`^w < ערך >`", inline=False)
        rep.add_field(name="חיפוש תוצאות מרובות למושג", value="`^w+ < מושג >`", inline=False)
        rep.add_field(name="ערך אקראי בוויקיפדיה (ייתכן וייקח לבוט זמן לטעון את הערכים).", value="`^r < מספר ערכים >`", inline=False)

    if not rep: return None
    
    if type(rep) == str:
        await message.channel.send(rep)
    elif type(rep) == list:
        for msg in rep: await message.channel.send(embed = msg)
    else:
        await message.channel.send(embed = rep)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="▶ ^עזרה ◀"))
    print("Online.")

client.run('')