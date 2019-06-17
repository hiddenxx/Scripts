import random

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from lxml import etree

ua = UserAgent()  # From here we generate a random user agent
proxies = []  # Will contain proxies [ip, port]


def treeMethod():
    url = 'https://www.uscho.com/rankings/d-i-mens-poll'

    def get_html(url):
        tree = etree.HTML(requests.get(url).text)
        soup = BeautifulSoup(tree.text, 'html.parser')
        return soup

    soup = get_html(url)
    print(soup.prettify())

    #
    # for section in tree.xpath('//section[@id="rankings"]'):
    #     print(section.xpath('h1[1]/text()')[0])
    #     print(section.xpath('h3[1]/text()')[0])
    #     for row in section.xpath('table/tr[@class="even" or @class="odd"]'):
    #         print('%-3s %-20s %10s %10s %10s %10s' % tuple(''.join(col.xpath('.//text()')) for col in row.xpath('td')))


def tableIDMethod():
    proxies_req = requests.get('https://www.sslproxies.org/')
    proxies_req.add_header('User-Agent', ua.random)
    proxies_doc = requests.get(proxies_req).read().decode('utf8')

    soup = BeautifulSoup(proxies_doc, 'html.parser')
    proxies_table = soup.find(id='proxylisttable')

    # Save proxies in the array
    for row in proxies_table.tbody.find_all('tr'):
        proxies.append({
            'ip': row.find_all('td')[0].string,
            'port': row.find_all('td')[1].string
        })

    print(len(proxies))


def random_proxy():
    return random.randint(0, len(proxies) - 1)


def main():
    treeMethod()


if __name__ == '__main__':
    main()
