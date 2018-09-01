from bs4 import BeautifulSoup as bs
import re
import json
import base64
import logging
import datetime
import re

log = logging.getLogger("main")


class ParserOtodom:
    def __init__(self, site_string):
        if len(site_string) > 0:
            self.soup = bs(site_string, 'html.parser')

        self.map = {
            "Build_year": "build_year",
            "Building_floors_num": "building_floors_num",
            "Building_material": "building_material",
            "Building_ownership": "building_ownership",
            "Building_type": "building_type",
            "business": "offer_type",
            "city_name": "city_name",
            "Construction_status": "construction_status",
            "Country": "country",
            "description": "description",
            "district_name": "district_name",
            "Equipment_types": "equipment",
            "Extras_types": "extras_surface",
            "Floor_no": "floor_num",
            "Heating": "heating",
            "language": "language",
            "latitude": "latitude",
            "longitude": "longitude",
            "Media_types": "media",
            "Id": "offer_id",
            "Price": "price",
            "price_currency": "price_currency",
            "ProperType": "proper_type",
            "region_name": "region_name",
            "Rent": "rent_price",
            "rooms": "rooms_num",
            "Security_types": "security_types",
            "seller_id": "seller_id",
            "source": "source",
            "Subregion": "subregion_name",
            "surface": "surface",
            "Title": "title",
            "Windows_type": "windows_type"
        }

    def parse_site(self):
        """
        ninja has under_line
        gpt has camelCase

        :return: dictionary with lists and etc.
        """
        ninja = self.parse_json("window.ninjaPV")
        gpt = self.parse_json("GPT.targeting")

        params = {}
        for key, val in {**ninja, **gpt}.items():
            if key in self.map:
                params[self.map[key]] = val
            else:
                if 'unknown' not in params:
                    params['unknown'] = []
                params['unknown'].append({key: val})

        params["latitude"] = self.get_coordinates("latitude")
        params["longitude"] = self.get_coordinates("longitude")
        params["description"] = self.get_description()
        params["source"] = "otodom"

        params["title"] = base64.b64decode(params["title"]).decode("utf-8")

        if "build_year" in params:
            if re.match(r"\d{4}", params["build_year"]):
                params["build_year"] = datetime.datetime.strptime(params['build_year'], "%Y")
            else:
                del params["build_year"]

        return params

    def get_coordinates(self, type):
        meta = self.soup.find("meta", {"itemprop": type})
        if meta is not None:
            return meta["content"]
        return 0.0

    def get_description(self):
        desc = ""
        for p in self.soup.find("div", {"itemprop": "description"}).find_all("p"):
            if p.text != "":
                desc += "</br>{}".format(p.text)
        return desc

    def parse_json(self, keyword):
        ninja_pv = self.soup.find(text=re.compile(keyword))
        raw_json = re.sub(
            r"^.*" + keyword + ".=.", "",
            re.findall(r"^.*" + keyword + ".*};",
                       ninja_pv, flags=re.M)[0]).replace(";", "")
        return json.loads(raw_json)


class ParserGratka:
    def __init__(self, site_string):
        if len(site_string) > 0:
            self.soup = bs(site_string, 'html.parser')

    def parse_site(self):
        params = {}
        params["json_string"] = {}
        ul = self.soup.find("ul", {"class": "parameters__rolled"})
        if ul is not None:
            for tag in ul.find_all("li"):
                span = tag.find("span")
                b = tag.find("b")
                if span is not None:
                    params["json_string"][span.text.strip()] = b.text.strip()
                else:
                    p = tag.find("p")
                    if p is not None:
                        k = tag.find("p", {"class": "parameters__label"}).text.strip()
                        v = tag.find("b", {"class": "parameters__multiValue"}).text.strip()
                        params["json_string"][k] = v


        params["Price"] = self.get_price()
        params["description"] = self.get_description()
        params["latitude"], params["longitude"] = self.get_coords()
        params["source"] = "gratka"
        params["offer_id"] = self.get_offer_id()
        params["city_name"], params["region_name"] = self.parse_localization(params["json_string"]["Lokalizacja"])
        params["title"] = self.get_title()

        return params

    def get_price(self):
        price = re.search(r"^(.*price:.*'?)$", self.soup.text, flags=re.M)
        if price is not None:
            price = price[0] \
                    .split("/")[0] \
                    .strip() \
                    .replace("zł", "") \
                    .replace("price:", "") \
                    .replace(",",".")\
                    .replace(" ", "")\
                    .replace("'", "")
            return price
        return 0

    def get_description(self):
        return self.soup.find("div", {"class": "description__rolled"})

    def get_coords(self):
        longitude = 0
        latitude = 0

        longitude_match = re.search(r"^(.*longitude:.*[0-9].)$", self.soup.text, flags=re.M)
        latitude_match = re.search(r"^(.*latitude:.*[0-9].)$", self.soup.text, flags=re.M)

        if longitude_match is not None:
            longitude = longitude_match[0].replace("longitude:", "").replace(" ", "").replace(",","")

        if latitude_match is not None:
            latitude = latitude_match[0].replace("latitude:", "").replace(" ", "").replace(",","")

        return longitude, latitude

    def get_offer_id(self):
        return self.soup.find("link", {"rel": "canonical"})['href'].split("/")[-1]

    def get_title(self):
        return self.soup.find("h1", {"class": "sticker__title"}).text

    def parse_localization(self, location_string):
        splitted = location_string.split(",")
        return splitted[0], splitted[1]

