import log
from crawler.Crawler import Crawler


if __name__ == '__main__':
    logger = log.set_logger("main")
    crawler = Crawler()
    crawler.crawl(
        download_searches=True,
        download_offers=True,
        remove_files=True,
        start_page=1,
        end_page=30
        rent=True
   )
