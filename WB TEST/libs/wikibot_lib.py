import wikipedia
import requests
from bs4 import BeautifulSoup

from libs.newspaper_lib import NewsPaper
from libs.weather_lib import get_weather

def math_formula_detection(summary, source_code):
    for math_element in BeautifulSoup(source_code, features="html5lib").find_all("span", {"class": "mwe-math-element"}):
        summary = summary.replace(math_element.text[:-3], "[ *formula* ]")

    return summary

def page_content(name, limit = 1000):
    
    def image_detect(source_code):
        start = source_code.find("//upload")
        end = [source_code.find(ext, start) for ext in (".PNG", ".png", ".JPG", ".jpg")]
        end = min([ext for ext in end if ext != -1]) + 4
         
        if not source_code[start:end]:
            return None
        else:
            url = "https:" + source_code[start:end]
            if not ".svg" in url: url = url.replace("/thumb", "")
            if url not in (
                "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Disambig_colour.svg/20px-Disambig_colour.svg.png",
                "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Arithmetic_symbols.svg/24px-Arithmetic_symbols.svg.png",
                "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Racine_carr%C3%A9e_bleue.svg/24px-Racine_carr%C3%A9e_bleue.svg.png"
                ) and not ("<" in url or ">" in url):
                return url
    
    try:
        
        search = wikipedia.WikipediaPage(name)
        source_code = requests.get(search.url).text
        
        summary = math_formula_detection(search.summary, source_code)    
        
        for i in ("()", "(audio)", "(listen)"):
            summary = summary.replace(i, "")

        if len(summary) > limit:
            summary = summary[:limit] + "…"

        img = image_detect(source_code)
                
        return search.title, summary.replace(" , ", ", "), search.url, img, True

    except:
        return name.capitalize(), "", "", "", False


def list_pages(l_page, title, description, limit = 1000):
    pages = [title, description, [], None, None]

    if type(l_page) == list:
        for page in [page_content(i, limit) for i in l_page]:
            if len(page[0]) and len(page[1]):
                pages[2].append([page[0], page[1]])

    else:
        page = page_content(l_page, limit)
        if len(page[0]) and len(page[1]):
            pages[2].append([page[0], page[1]])

    return pages


def page_random(nb):
    try:
        nb = int(nb)
        
        if nb < 1: nb = 1
        elif nb > 10: nb = 10
            
    except:
        nb = 1
        
    rand = wikipedia.random(nb)
    return list_pages(rand, "ערכים אקראיים", f"{nb} ערכים אקראיים בוויקיפדיה", 500)


def page_search(name):
    rslt = wikipedia.search(name, results=5)
    
    if len(rslt):
        return list_pages(rslt, name, f"תוצאות חיפוש מרובות בוויקיפדיה", 500)

    else:
        rep = ["מחפש בוויקיפדיה", f"תוצאות החיפוש עבור '{name}'", [], 0xff0000, None]
        rep[2].append(["שגיאה", "הערך המבוקש לא נמצא. אנא בדקו את תקינות השם ונסו שנית."])
        return rep


def page_read(name, automatic_correction = False):
    def auto_name(name):
        try:
            for i in wikipedia.search(name, results = 3):
                try:
                    wikipedia.WikipediaPage(i)
                    return i
                except:
                    pass
        except:
            return name

    if automatic_correction: name = auto_name(name)
    w_title, w_content, w_url, w_img, success = page_content(name)
        
    if success:
        page = [w_title, "ערך בוויקיפדיה", [], None, w_img]
        page[2].append(["תקציר הערך", w_content])
        page[2].append(["לקריאה מורחבת", w_url])


    else:
        page = [w_title, "ערך בוויקיפדיה", [], 0xff0000, None]
        page[2].append(["שגיאה", f"לא נמצאו ערכים בשם: '{name}'. אנא בדקו את תקינות שם הערך."])

    return page


def get_news(newspaper_name, number):
    newspaper = NewsPaper()
    plus = False
    if number.endswith("+"):
        plus = True
        try:
            number = int(number[:-1])
        except:
            number = 1
    else:
        try:
            number = int(number)
        except:
            number = 1
    
    return newspaper_name.title(), newspaper.get_rss(newspaper_name, number, plus)


def weather(city_name, nb_day):
    try:
        nb_day = int(nb_day)
        if nb_day < 0 or nb_day > 7: nb_day = 0
    except:
        nb_day = 0

    try:
        weather_data = get_weather(city_name, nb_day)
        return [(value.partition("#")[0], f'{weather_data[index]}{value.partition("#")[2]}') for index, value in enumerate(("תיאור", "טמפרטורה#°C", "מרגיש כמו#°C", "טל#°C", "לחץ# hPa", "לחות# %", "מהירות הרוח# km/h", "Wind direction#°", "Cloudiness# %", "הסתברות לגשם# %"))], weather_data[-2], nb_day, weather_data[-3], weather_data[-1]
    except:
        return None, 0, 0, 0, 0
