import argparse
import re
import subprocess
import sys

from datetime import datetime, timedelta

from bs4 import BeautifulSoup


class AuditorSaleSearch(object):
    def __init__(self, query, date):
        self.query = query
        self.date = date
        self.addresses = {}

    def get_page(self, page):
        command  = "curl 'http://oh-mahoning-auditor.publicaccessnow.com/SalesSearch.aspx?page479={}&SearchType=1'"
        command += " -H 'Cookie: C_F1L={}; C_F1H={}; C_F2L=-1; C_F3L=-1; C_F4L=-1; C_F5L=-1; C_F6L=-1; C_F7L=-1; C_F8L=-1; C_F10L=-1; C_F11L=-1; C_s1=1; C_s2=1; C_s3=1; C_s4=1; C_s5=1; C_s6=1; C_s7=1; C_s8=1; C_F9L=-1;'"
        command += " --compressed --insecure"

        page_command = command.format(page, self.date, self.date)
        p = subprocess.Popen(page_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        return out

    def parse_page(self, page):
        page_content = self.get_page(page)

        for result in BeautifulSoup(page_content, 'html.parser').find_all('div', class_='resultsDiv'):
            parcel = result.div.table.table.find_all('tr')[1].find_all('td')[0].text
            owner = result.div.table.table.find_all('tr')[1].find_all('td')[1].text
            address = result.div.table.table.find_all('tr')[2].table.table.tr.find_all('td')[1].text

            if self.query in owner.lower():
                # Got an owner match, add address to final list
                if parcel not in self.addresses.keys():
                    self.addresses[parcel.strip()] = re.sub('\s+', ' ', address).strip()

    def scrape(self):
        # Grab first page to see page count
        first_page = self.get_page(1)

        first_page_parsed = BeautifulSoup(first_page, 'html.parser')

        if first_page_parsed.body.find_all(text='No Results Found'):
            print('No transfers found')
            sys.exit(1)

        page_count = int(first_page_parsed.find_all('div', class_='search-results-bar')[0].find_all('a')[-2].text)

        # Try each iteration multiple times because the site doesn't do an ORDER BY
        for retry in range(2):
            for page in range(1, page_count+1):
                self.parse_page(page)

        if self.addresses:
            print('Found transfers:')
            for parcel, address in self.addresses.items():
                if re.search(r'\d', address):
                    print(parcel, address, 'https://www.google.com/maps/place/{}+mahoning+county+oh/'.format(address.replace(' ', '+')))
                else:
                    print(parcel, address)
        else:
            print('No transfers found')


def main():
    yesterday = (datetime.today() - timedelta(days=1)).strftime('%m/%d/%Y')

    parser = argparse.ArgumentParser()
    parser.add_argument('query', type=str)
    parser.add_argument('date', nargs='?', default=yesterday)
    args = parser.parse_args()

    scraper = AuditorSaleSearch(args.query, args.date)
    scraper.scrape()


if __name__ == "__main__":
    main()
