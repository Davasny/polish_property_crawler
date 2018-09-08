from crawler.Downloader import Downloader
from crawler.Filer import Filer
from crawler.Scraper import Scraper
from crawler.Parser import ParserOtodom, ParserGratka
from crawler.Database import session, Offer
import logging
import config

log = logging.getLogger("main")


class Crawler:
    def __init__(self, city="warszawa", property_type="aparment"):
        self.download_path_searches = config.FILES['download_path_searches']
        _path_searches = Filer(self.download_path_searches)
        _path_searches.make_sure_if_path_exists()

        self.download_path_offers = config.FILES['download_path_offers']
        _path_offers = Filer(self.download_path_offers)
        _path_offers.make_sure_if_path_exists()

        self.services = [
            "otodom",
            "gratka"
        ]

        self.city = city
        self.property_type = property_type

    def crawl(self, download_searches=True, download_offers=True,
              remove_files=False, start_page=1, end_page=30, rent=True):
        if remove_files:
            log.info("Removing files")
            filer = Filer(self.download_path_offers)
            filer.empty_dir()

            filer = Filer(self.download_path_searches)
            filer.empty_dir()

        if download_searches:
            log.info("Downloading files")
            for service in self.services:
                d = Downloader(self.download_path_searches, self.download_path_offers,
                               service=service, city=self.city, property_type=self.property_type, rent=rent)
                d.download_main_pages(start_page, end_page)

        """
        Get all links to offers
        """
        filer_searches = Filer(self.download_path_searches)
        all_offers = {}

        for service in self.services :
            if service not in all_offers:
                all_offers[service] = []

            for file in filer_searches.get_all_files():
                with open("{}/{}".format(self.download_path_searches, file), "r", encoding="utf-8") as f:
                    scraper = Scraper(f.read(), service)
                    for link in scraper.get_search_results():
                        all_offers[service].append(link)

        log.debug("Links to offers:\t{}".format(len(all_offers)))

        """
        Download offers
        """
        if download_offers:
            for service in self.services:
                d = Downloader(self.download_path_searches, self.download_path_offers,
                               service=service, city=self.city)
                progress = 0
                for url in all_offers[service]:
                    if d.download_offer_page(url):
                        progress += 1
                    log.info("Downloaded [{}]:\t{}/{}".format(service, progress, len(all_offers[service])))

        filer = Filer(self.download_path_offers)
        all_files = filer.get_all_files()

        """
        Add offers to DB
        """
        counter = 0
        for file in all_files:
            if counter % 50 == 0:  # commit records in DB every 50 offers
                session.commit()
            params = {}

            with open("{}/{}".format(self.download_path_offers, file), "r", encoding="utf-8") as f:
                if "gratka" in file:
                    log.debug("Parsing gratka file:\t{}".format(file))
                    parser = ParserGratka(f.read())
                    params = parser.parse_site()

                elif "otodom" in file:
                    log.debug("Parsing otodom file:\t{}".format(file))
                    parser = ParserOtodom(f.read())
                    params = parser.parse_site()

                if "offer_id" in params:
                    instance = session.query(Offer).filter(Offer.offer_id == params['offer_id']).first()
                    if not instance:
                        log.info("Adding offer:\t{}\t{}/{}".format(params['offer_id'], counter, len(all_files)))
                        session.add(Offer(**params))
            counter += 1
        session.commit()
