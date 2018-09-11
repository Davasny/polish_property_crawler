from bs4 import BeautifulSoup as bs


class Scraper:
    """
    Its only purpose is to get all links and titles from search results
    """
    def __init__(self, site_string, service):
        self.service = service
        if len(site_string) > 0:
            self.soup = bs(site_string, 'html.parser')

    def get_search_results(self):
        links = []
        if self.service == "otodom":
            for tag in self.soup.find_all("article", {"class": "offer-item"}):
                if tag.name == "article":
                    links.append(tag["data-url"])

        elif self.service == "gratka":
            for tag in self.soup.find_all("a", {"class": "teaser"}):
                if tag.name == "a":
                    links.append(tag['href'])
        return links
