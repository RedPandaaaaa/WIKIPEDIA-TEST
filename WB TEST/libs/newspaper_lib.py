import requests
import xmltodict
import html


def special_char(text):
    text = html.unescape(text)

    text = text.replace("><", "> <")
    start = text.find("<")
    stop = text.find(">", start)
    while start != -1:
        text = text[:start] + text[stop + 1:]
        start = text.find("<")
        stop = text.find(">", start)

    if len(text) > 1000: return text[:1000] + "…"
    return text


class NewsPaper:
    def __init__(self):
        self.name = None
        self.data = None
        self.url = None

    def __get_url(self):
        rss = (
            "http://www.thelancet.com/rssfeed/lancet_current.xml",
            "https://www.lemonde.fr/rss/une.xml",
            "https://www.lexpress.fr/rss/alaune.xml",
            "https://www.lefigaro.fr/rss/figaro_actualites.xml",
            "https://www.nouvelobs.com/a-la-une/rss.xml",
            "https://time.com/rss",
            "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
            "https://www.courrierinternational.com/feed/all/rss.xml",
            "http://rss.liberation.fr/rss/9/",
            "https://www.monde-diplomatique.fr/rss",
            "https://www.theguardian.com/international/rss",
            "https://www.sciencesetavenir.fr/rss.xml",
            "https://rcs.mako.co.il/rss/31750a2610f26110VgnVCM1000005201000aRCRD.xml")

        if self.index < len(rss):
            return rss[self.index]
        return None

    def __name_detect(self):
        newspapers_name = (
            "the lancet#lancet",
            "le monde#monde",
            "l'express#express",
            "le figaro#figaro",
            "l'obs#obs#l'observateur#observateur",
            "the time#time",
            "the news york times#new york times#ny times",
            "courrier international",
            "libération#liberation#libe#libé",
            "le monde diplomatique#monde diplomatique",
            "the guardian#guardian",
            "sciences et avenir",
            "mako#מאקו")
        
        for index, name in enumerate(newspapers_name):
            if self.name in name.split("#"):
                self.index = index
                return None

        return [name.split("#")[0].title() for name in newspapers_name]
        
    def __get_data(self):
        return xmltodict.parse(requests.get(self.url).content)

    def get_rss(self, name, nb, plus):
        
        self.name = name.lower()
        
        test_available = self.__name_detect()
        if test_available: return None, test_available
        
        self.url = self.__get_url()
        self.data = self.__get_data()

        if self.index == 0: self.data = self.__the_lancet(nb)
        elif self.index == 1: self.data = self.__le_monde(nb)
        elif self.index == 2: self.data = self.__l_express(nb)
        elif self.index == 3: self.data = self.__le_figaro(nb)
        elif self.index == 4: self.data = self.__l_obs(nb)
        elif self.index == 5: self.data = self.__time(nb)
        elif self.index == 6: self.data = self.__the_new_york_times(nb)
        elif self.index == 7: self.data = self.__courrier_international(nb)   
        elif self.index == 8: self.data = self.__liberation(nb)
        elif self.index == 9: self.data = self.__le_monde_diplomatique(nb)
        elif self.index == 10: self.data = self.__the_guardian(nb)
        elif self.index == 11: self.data = self.__sciences_et_avenir(nb)
        elif self.index == 12: self.data = self.__mako(nb)

        if plus: return [self.data[-1]], None
        else: return self.data, None

# --- self.data
# 0 : Titre
# 1 : Description
# 2 : Lien
# 3 : Image
# ---

# --- Newspapers functions --- #

    def __the_lancet(self, nb):
        information = []
        for news in self.data["rdf:RDF"]["item"][0:nb]:
            information.append([special_char(news["title"]),
                                                    special_char(news["description"]),
                                                    news["link"],
                                                    None])
        return information

    def __le_monde(self, nb):
        information = []
        for news in self.data["rss"]["channel"]["item"][0:nb]:
            information.append([special_char(news["title"]),
                                                    special_char(news["description"]),
                                                    news["link"],
                                                    news["media:content"]["@url"]])
        return information

    def __l_express(self, nb):
        information = []
        for news in self.data["rss"]["channel"]["item"][0:nb]:
            information.append([f"[{news['subhead']}] {special_char(news['title'])}",
                                                    special_char(news["description"]),
                                                    news["link"],
                                                    news["enclosure"]["@url"]])
        return information

    def __le_figaro(self, nb):
        information = []
        for news in self.data["rss"]["channel"]["item"][0:nb]:
            summary = news["description"]
            if not summary: summary = "*Unavailable*"
            information.append([f"[{news['category']}] {special_char(news['title'])}",
                                                    special_char(summary),
                                                    news["link"],
                                                    None])
        return information

    def __l_obs(self, nb):
        information = []
        for news in self.data["rss"]["channel"]["item"][0:nb]:
            information.append([f"[{news['category']}] {special_char(news['title'])}",
                                                    special_char(news["description"]),
                                                    news["link"],
                                                    news["enclosure"]["@url"]])
        return information

    def __time(self, nb):
        information = []
        for news in self.data["rss"]["channel"]["item"][0:nb]:
            information.append([special_char(news["title"]),
                                                    special_char(news["description"]),
                                                    news["link"],
                                                    None])
        return information

    def __the_new_york_times(self, nb):
        information = []
        for news in self.data["rss"]["channel"]["item"][0:nb]:
            information.append([special_char(news["title"]),
                                                    special_char(news["description"]),
                                                    news["link"],
                                                    news["media:content"]["@url"]])
        return information

    def __courrier_international(self, nb):
        information = []
        for news in self.data["rss"]["channel"]["item"][0:nb]:
            information.append([special_char(news["title"]),
                                                    special_char(news["description"]),
                                                    news["link"],
                                                    None])
        return information

    def __liberation(self, nb):
        information = []
        for news in self.data["feed"]["entry"][0:nb]:
            try:
                information.append([f"[{news['category']['@term']}] {special_char(news['title'])}",
                                                     special_char(news["summary"]["#text"]),
                                                     news["link"][0]["@href"],
                                                     news["link"][1]["@href"]])
            except:
                information.append([f"[{news['category']['@term']}] {special_char(news['title'])}",
                                                     "*Unavailable*",
                                                     news["link"][0]["@href"],
                                                     news["link"][1]["@href"]])
        return information

    def __le_monde_diplomatique(self, nb):
        information = []
        for news in self.data["rss"]["channel"]["item"][0:nb]:
            summary = special_char(news["description"])
            summary = summary[:min(summary.find("/"), summary.find("(...)") + 5)]
            if not summary: summary = "*Unavailable*"

            information.append([special_char(news["title"]),
                                                 summary,
                                                 news["link"],
                                                 None])
        return information

    def __the_guardian(self, nb):
        information = []
        for news in self.data["rss"]["channel"]["item"][0:nb]:
            information.append([special_char(news["title"]),
                                                    special_char(news["description"]),
                                                    news["link"],
                                                    news["media:content"][0]["@url"]])
        return information

    def __sciences_et_avenir(self, nb):
        information = []
        for news in self.data["rss"]["channel"]["item"][0:nb]:
            image = None
            if "enclosure" in news.keys(): image = news["enclosure"]["@url"]
            information.append([f"[{news['category']}] {special_char(news['title'])}",
                                                    special_char(news["description"]),
                                                    news["link"],
                                                    image])
        return information

    def __mako(self, nb):
        information = []
        for news in self.data["rss"]["channel"]["item"][0:nb]:
            image = None
            if "enclosure" in news.keys(): image = news["enclosure"]["@url"]
            information.append([f"[{news['category']}] {special_char(news['title'])}",
                                                    special_char(news["description"]),
                                                    news["link"],
                                                    image])
        return information