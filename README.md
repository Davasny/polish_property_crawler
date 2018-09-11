# Polish property crawler

### About
This program downloads and parses offers of rents and salles houses and apartments published at otodom and gratka

### Usage
1. Copy `config.py.example` to `config.py` and change values to your own
2. Install requirements by `pip install -r requirements.txt`
3. Run `app.py`

### Docker
1. Create `config.py` next to the `Dockerfile`
2. Build and run `Dockerfile`

### Available command line options
```
Usage: app.py [options]

Options:
  -h, --help            show this help message and exit
  -c CITY, --city=CITY  City to crawl [warsaw]
  -t PROPERTY_TYPE, --type=PROPERTY_TYPE
                        Type of property to crawl (house/apartment)
                        [apartment]
  -o OFFER_TYPE, --offer-type=OFFER_TYPE
                        Type of offer type to search (rent/sell) [rent]
  -s START_PAGE, --start-page=START_PAGE
                        Start page of searches results [1]
  -e END_PAGE, --end-page=END_PAGE
                        End page of searches results [2]
  -d DOWNLOAD_SEARCHES, --download-searches=DOWNLOAD_SEARCHES
                        Download search result pages (True/False) [True]
  -n DOWNLOAD_OFFERS, --download-offers=DOWNLOAD_OFFERS
                        Download offers (True/False) [True]
  -r REMOVE_FILES, --remove-files=REMOVE_FILES
                        Empty dirs containing old files (True/False) [True]
```
