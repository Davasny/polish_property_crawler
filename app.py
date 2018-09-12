"""Usage: app.py [options]

Options:
  -h, --help            show this help message and exit
  -c CITY --city=CITY  City to crawl [default: warsaw]
  -t PROPERTY_TYPE --type=PROPERTY_TYPE
                        Type of property to crawl (house/apartment)
                        [default: apartment]
  -o OFFER_TYPE --offer-type=OFFER_TYPE
                        Type of offer type to search (rent/sell) [default: rent]
  -s START_PAGE --start-page=START_PAGE
                        Start page of searches results [default: 1]
  -e END_PAGE --end-page=END_PAGE
                        End page of searches results [default: 2]
  -nds --not-download-searches
                        Do not download search result pages [default: False]
  -ndo --not-download-offers
                        Do not download offers [default False]
  -nr --not-remove-files     Do not empty dirs containing old files [default: False]
"""
from docopt import docopt

import log
from crawler.crawler import Crawler

if __name__ == '__main__':
    logger = log.set_logger("main")
    arguments = docopt(__doc__)
    integer_params = ['--start-page', '--end-page']
    for i in integer_params:
        arguments[i] = int(arguments[i])

    crawler = Crawler(arguments['--city'], arguments['--type'])
    crawler.crawl(
        download_searches=not arguments['--not-download-searches'],
        download_offers=not arguments['--not-download-offers'],
        remove_files=not arguments['--not-remove-files'],
        start_page=arguments['--start-page'],
        end_page=arguments['--end-page'],
        rent=arguments['--offer-type'],
    )
