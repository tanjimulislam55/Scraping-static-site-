from urllib3 import PoolManager
from bs4 import BeautifulSoup
import json


class Scrape:

    def __init__(self):
        self.manager = PoolManager()
        # self.all_baby_names_dict = {'boy': {}, 'girl': {}}
        self.all_baby_names_dict = dict()
        # self.gender = ''

    def scrape(self, url):
        html = self.manager.request("GET", f"https://www.searchtruth.com{url}").data
        bs = BeautifulSoup(html, 'lxml')
        data = bs.find('table', {'class': 'w3-card-4 w3-table-all w3-hoverable w3-medium'})

        try:
            for name, description in zip(data.find_all('td', {'itemprop': 'name'}), data.find_all('td', {'itemprop': 'description'})):
                # self.all_baby_names_dict[self.gender][name.text.strip()] = description.text.strip()
                self.all_baby_names_dict[name.text.strip()] = description.text.strip()

            for x in bs.find('div', {'class': 'w3-sand w3-center'}).find_all('a'):
                if 'Next' in x.text:
                    nextLink = x['href']
                    print(f'https://www.searchtruth.com/baby_names/{nextLink}')
            try:
                # recursion for every page from specific alphabet
                self.scrape(f'/baby_names/{nextLink}')
            except UnboundLocalError:
                print(f'throughing {UnboundLocalError}. no next link')
                pass
        except AttributeError:
            print(f'throughing {AttributeError}. no names from url: {url}')
            pass


    def urls(self):
        html = self.manager.request("GET", f'https://www.searchtruth.com/baby_names/names.php?ntype=m&find=2&letter=A').data
        bs = BeautifulSoup(html, 'lxml')
        for x in bs.find_all('a', {'class': 'w3-padding'}):
            # between 'boy' and 'girl'
            # self.gender = x.div.h2.strong.text.split()[1].lower()
            print(f"\nchecking for url:  https://www.searchtruth.com{x['href']}")
            self.scrape(x['href'])

        with open("babyNames.json", "w") as outfile:
            json.dump(self.all_baby_names_dict, outfile)
        print('\nDone.\n')



scraping = Scrape()
scraping.urls()

