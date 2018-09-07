import log
import optparse
from crawler.Crawler import Crawler


if __name__ == '__main__':
    logger = log.set_logger("main")

    parser = optparse.OptionParser()
    parser.add_option("-c", "--city",
                      dest="city",
                      default="warszawa",
                      help="City to crawl [warsaw]")

    parser.add_option("-t", "--type",
                      dest="property_type",
                      default="apartment",
                      help="Type of property to crawl (house/apartment) [apartment]")

    parser.add_option("-o", "--offer-type",
                      dest="offer_type",
                      default="rent",
                      help="Type of offer type to search (rent/sell) [rent]")

    parser.add_option("-s", "--start-page",
                      dest="start_page",
                      type="int",
                      default=1,
                      help="Start page of searches results [1]")

    parser.add_option("-e", "--end-page",
                      dest="end_page",
                      type="int",
                      default=2,
                      help="End page of searches results [2]")

    parser.add_option("-d", "--download-searches",
                      dest="download_searches",
                      default=True,
                      help="Download search result pages (True/False) [True]")

    parser.add_option("-n", "--download-offers",
                      dest="download_offers",
                      default=True,
                      help="Download offers (True/False) [True]")

    parser.add_option("-r", "--remove-files",
                      dest="remove_files",
                      default=True,
                      help="Empty dirs containing old files (True/False) [True]")

    opt, _ = parser.parse_args()

    crawler = Crawler(opt.city, opt.property_type)
    crawler.crawl(
            download_searches=opt.download_searches,
            download_offers=opt.download_offers,
            remove_files=opt.remove_files,
            start_page=opt.start_page,
            end_page=opt.end_page,
            rent=opt.offer_type
       )
