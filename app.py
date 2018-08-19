import log
from crawler.Crawler import Crawler


if __name__ == '__main__':
    logger = log.set_logger("main")
    crawler = Crawler()
    crawler.crawl(
        download=False,
        remove_files=False,
        start_page=1,
        end_page=30
   )
