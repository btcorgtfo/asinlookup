import requests
import urllib
import time
import datetime


class AmazonSearcher:
    AMAZON_URLS = {'DE': 'https://www.amazon.de/gp/product/',
                   'IT': 'https://www.amazon.it/dp/product',
                   'NL': 'https://www.amazon.nl/dp/product',
                   'UK': 'https://www.amazon.co.uk/dp/product',
                   'ES': 'https://www.amazon.es/dp/product',
                   'FR': 'https://www.amazon.fr/dp/product',
                   'US': 'https://www.amazon.com/dp/product',
                   'SE': 'https://www.amazon.se/dp/product',
                   }

    TIME_TO_SLEEP = 30  # time to wait between failed / empty api calls

    def __init__(self, marketplace: str, api_key: str):
        self.__marketplace = marketplace.upper()
        if self.__marketplace not in self.AMAZON_URLS.keys():
            raise NotImplementedError(f'marketplace: {self.__marketplace} not implemented yet.')

        self.__search_url = self.AMAZON_URLS.get(self.__marketplace)
        self.__api_key = api_key

    def search_url(self, asin: str) -> str:
        """
        generates the search url
        :param asin:
        :return:
        """
        return urllib.parse.urljoin(self.__search_url, asin)

    def payload(self, asin: str) -> dict:
        """
        payload for the scraper api call
        :param asin:
        :return:
        """
        d = {'api_key': self.__api_key }
        d['url'] = self.search_url(asin)

        return d

    def get_product_page(self, asin: str, max_retries=3) -> str:
        """
        returns the plain html from the product page

        :param asin: the asin
        :param max_retries: number of retires until an empty page is returned
        :return:
        """
        retry = 1

        while retry <= max_retries:
            print(f"{datetime.datetime.now()}: {retry}. try")
            r = requests.get('http://api.scraperapi.com',
                             params=self.payload(asin))

            if r.status_code == 200:
                if len(r.text) != 0:  # some time the .text is empty, html code == 200
                    return r.text
                else:
                    print("Empty page returned, will retry")
                    time.sleep(self.TIME_TO_SLEEP)
                    retry += 1
            elif r.status_code == 404:
                # page not found on the marketplace
                return str()
            else:
                retry += 1
                time.sleep(self.TIME_TO_SLEEP)

        return str()


class SimpleTelegramBot:
    """
    Simple telegram bot, which sends a message to a given chat_id

    Details on how to get the token and work with bot can be found here https://core.telegram.org/bots

    """
    def __init__(self, token: str, chat_id: str):
        self.__token = token
        self.__chat_id = chat_id

    def sendtext(self, message: str):
        bot_token = self.__token
        bot_chatID = self.__chat_id
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + message

        response = requests.get(send_text)

        return response.json()


def check_html_for_str(html: str, search_str: str) -> bool:
    """
    check in given plain html code if search_str occurs

    :param html:
    :param search_str:
    :return:
    """
    if search_str in html:
        return False
    else:
        return True