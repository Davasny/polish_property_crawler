import datetime
import logging
import random
import re
from time import sleep

import requests

import config

log = logging.getLogger("main")


class Downloader:
    def __init__(
            self,
            download_path_searches,
            download_path_offers,
            city,
            property_type="apartment",
            service="otodom",
            rent=True,
    ):
        self.service = service
        rent_string = "sprzedaz"
        if rent:
            rent_string = "wynajem"

        if service == "otodom":
            if property_type == "apartment":
                property_type = "mieszkanie"
            else:
                property_type = "dom"
            self.url = "https://www.otodom.pl/{}/{}/{}/".format(rent_string, property_type, city)
            self.url_search = "?search[order]=created_at_first:desc"

        elif service == "gratka":
            if property_type == "apartment":
                property_type = "mieszkania"
            else:
                property_type = "domy"
            self.url = "https://gratka.pl/nieruchomosci/{}".format(property_type)
            self.url_search = "?rodzaj-ogloszenia={}&lokalizacja_miejscowosc={}".format(rent_string, city)

        self.download_path_searches = download_path_searches
        self.download_path_offers = download_path_offers

        self._s = requests.Session()

    def download_main_pages(self, start_page=1, end_page=5):
        if start_page <= 0:
            log.error("Incorrect start page\t{}".format(start_page))
            return False

        if start_page >= end_page:
            log.error("Incorrect end page:\t{}".format(end_page))
            return False

        for page_num in range(start_page, end_page):
            url = "{}{}&page={}".format(self.url, self.url_search, page_num)
            log.info("Downloading:\t{}".format(url))

            filename = self.generate_file_name(self.download_path_searches)

            self.get_site_to_file(url=url, filename=filename)
            sleep(self.randomize_wait_time())
        return True

    def download_offer_page(self, offer_link):
        if not re.match(
                r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,4}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)",
                offer_link):
            log.error("Incorrect link")
            return False

        filename = self.generate_file_name(self.download_path_offers)

        log.debug("New filename for link:\t{}\t->\t{}".format(offer_link, filename))

        self.get_site_to_file(url=offer_link, filename=filename)
        return True

    def generate_file_name(self, path):
        return "{}/{}_{}.html".format(
            path,
            self.service,
            datetime.datetime.now().timestamp())

    def get_site_to_file(self, url, filename):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/66.0.3359.139 Safari/537.36 OPR/53.0.2907.37',
        }
        log.debug("Sending request")
        response = self._s.get(url=url, headers=headers)
        if response.status_code == 200:
            log.debug("Recived 200, saving to:\t{}".format(filename))

            with open(filename, "w", encoding="utf-8") as f:
                f.write(response.text)

            return True
        else:
            log.error("Response:\t".format(response.status_code))
            return False

    def randomize_wait_time(self):
        time = random.uniform(config.DOWNLOADER['minimal_time'], config.DOWNLOADER['maximal_time'])
        if time is not None:
            return time
        return 0.75
