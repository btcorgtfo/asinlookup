# Amazon ASIN lookup
Easy way to frequently check if a ASIN on amazon can be ordered and send a message to a telegram channel.

## Installation and setups
`git clone git@github.com:btcorgtfo/asinlookup.git`

`pip install -r requirements.txt`

## Setup
### Get a Scraper API key
You can try to scrape amazon by yourself or use a service. [scraperapi](https://www.scraperapi.com/?fp_ref=noreferral) will be used in this example, where you can have 1000 
api calls per month for free or subscribe to a small plan on a monthly basis. 

So go to [this](https://www.scraperapi.com/?fp_ref=noreferral) page, get the free account and copy your access token from there.

### Optional: Telegram Bot integration
If you are interested in a telegram bot which can send a message to a group chat (maybe as update if a product turns available) you can get more information about bots [here](https://core.telegram.org/bots). A `token` is needed to configure the `SimpleTelegramBot`.

Once you have a bot with a token you need to add him to the group chat and retrieve the corrresponding `chat_id` ([tutorial](https://stackoverflow.com/questions/32423837/telegram-bot-how-to-get-a-group-chat-id)).

## Basic Usage
```
from models import AmazonSearcher, check_html_for_str, SimpleTelegramBot

api_key = 'your-api-key-nobody-else-knows-for-the-scraperapi'
marketplace = 'US'
asin = 'B07VGRJDFY'

searcher = AmazonSearcher(marketplace=marketplace,
                          api_key=api_key)

result = searcher.get_product_page(asin=asin)
```
`result` will contain the product detail page in plain html, so you have to decide yourself for what to look for. You can
use the `check_html_for_str(html=, search_str=)` function to match to a specific string, e.g. 'product not available'.

```
if check_html_for_str(html=result, search_str='not available'):
    message = f"product ({asin}) not available."
else:
    message = "product ({asin}) is available."

print(message)
```

If you want to use the chat bot, you can use it via
```
bot = SimpleTelegramBot(token='your-chatbot-token',
                        chat_id='chat_id-where-the-bot-should-send-message-to')
```

and drop a message to the chat with `bot.send_text('A message.')`