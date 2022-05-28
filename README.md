# sahibinden-bot

<img align="left" width="200" src="https://github.com/ErhoSen/sahibinden-bot/raw/master/img/demo.png">

Bot that tracks new ads at sahibinden.com and notifies telegram channel

## Uses
* [httpx](https://www.python-httpx.org/) to make http requests
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) to parse html
* [pydantic](https://pydantic-docs.helpmanual.io/) to type objects
* [aiogram](https://docs.aiogram.dev/en/latest/) to send messages to telegram
* [s3-objects-tracker](https://github.com/ErhoSen/s3-objects-tracker) to track already processed ads

The bot is running as [Yandex.Function](https://cloud.yandex.ru/docs/functions/), so it can be triggered by cron job.

But also you can run it on [AWS Lambda](https://aws.amazon.com/lambda/) or [Google Cloud Functions](https://cloud.google.com/functions/).

It's required to use proxy to make requests to sahibinden.com outside Turkey.

## Run manually

```bash
$ python3 main.py
```

## Configuration

**Sahibinden-bot** can be configured using environment variables.
The optimal way is to create an `.env` file in the root `sahibinden_bot` directory.

```bash
SAHIBINDEN_SOURCE_URL='https://www.sahibinden.com/en/computers-laptops-notebooks?address_city=35'

TELEGRAM_BOT_TOKEN='bot_token'
TELEGRAM_CHANNEL_ID='channel_id '

AWS_ACCESS_KEY_ID='aws_access_key_id'
AWS_SECRET_ACCESS_KEY='aws_access_key_id'
AWS_BUCKET_NAME='aws_bucket_name'
AWS_ENDPOINT_URL='https://s3.amazonaws.com'
```

**SAHIBINDEN_SOURCE_URL**: The URL of the search results page to scrape.

### Optional integration with Sentry.

```bash
SENTRY_DSN='sentry_dsn'
```

### Optionally uses a proxy.

```bash
PROXY_URL='http://user:pass@ip:port'
PROXY_URL_BACKUP='http://user:pass@ip:port'
```
