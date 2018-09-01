from crawler.Downloader import Downloader
from crawler.Filer import Filer
from crawler.Scraper import Scraper
from crawler.Parser import ParserOtodom, ParserGratka
from crawler.Database import MySQL
import logging

log = logging.getLogger("main")


class Crawler:
    def crawl(self, download=True, remove_files=False, start_page=1, end_page=30):
        download_path = "downloaded_files"
        download_path_searches = "searches"
        download_path_offers = "offers"

        services = [
            "otodom",
            "gratka"
        ]

        if download:
            log.info("Downloading files")
            if remove_files:
                filer = Filer("{}/{}".format(download_path, download_path_offers))
                filer.empty_dir()

                filer = Filer("{}/{}".format(download_path, download_path_searches))
                filer.empty_dir()

            for service in services:
                d = Downloader(download_path, download_path_searches, download_path_offers, service, rent=False)
                d.download_main_pages(start_page, end_page)

        """
        Get all links to offers
        """
        filer = Filer("{}/{}".format(download_path, download_path_searches))
        all_offers = {}
        all_files = filer.get_all_files()

        for service in services:
            all_offers[service] = []
            for file in all_files:
                if service in file:
                    with open("{}/{}/{}".format(download_path, download_path_searches, file), "r", encoding="utf-8") as f:
                        scraper = Scraper(f.read(), service)
                        for link in scraper.get_search_results():
                            all_offers[service].append(link)
        log.debug("Found links:\t{}".format(len(all_offers)))

        """
        Download offers
        """
        if download:
            for service in services:
                d = Downloader(download_path, download_path_searches, download_path_offers, service)
                progress = 0
                total = len(all_offers[service])
                for url in all_offers[service]:
                    if d.download_offer_page(url):
                        progress += 1
                    log.info("Downloaded:\t{}/{}".format(progress, total))

        filer = Filer("{}/{}".format(download_path, download_path_offers))
        all_files = filer.get_all_files()


        for file in all_files:
            params = {}
            with open("{}/{}/{}".format(download_path, download_path_offers, file), "r", encoding="utf-8") as f:
                if "gratka" in file:
                    log.debug("Parsing file:\t{}".format(file))
                    parser = ParserGratka(f.read())
                    params = parser.parse_site()

                elif "otodom" in file:
                    log.debug("Parsing file:\t{}".format(file))
                    parser = ParserOtodom(f.read())
                    params = parser.parse_site()

                for k, v in params.items():
                    if isinstance(v, list):
                        params[k] = ",".join(v)

                keys = [key for key in params]
                vals = [str(val).replace("\"", '\\"') for key, val in params.items()]

                keys_string = "`" + "`,`".join(keys) + "`"
                vals_string = "\"" + "\",\"".join(vals) + "\""

                query = "INSERT IGNORE INTO `offers` ({}) VALUES ({})".format(keys_string, vals_string)
                new_row_id = mysql.new_query(query)
                log.debug("Inserted row:\t{}".format(new_row_id))
