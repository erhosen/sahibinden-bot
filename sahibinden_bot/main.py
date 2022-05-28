import asyncio
import logging
from typing import Dict, Optional

import sentry_sdk
from aiogram import Bot
from core import Product
from s3_objects_tracker import S3ObjectsTracker
from sahibinden import sahibinden_client
from settings import settings

logging.getLogger().setLevel(logging.DEBUG)
sentry_sdk.init(settings.SENTRY_DSN, traces_sample_rate=1.0)

SOURCE_URL = "https://www.sahibinden.com/en/bicycles?address_town=655&address_city=48"


async def send_message(bot: Bot, product: Product):
    await bot.send_photo(
        chat_id=settings.TELEGRAM_CHANNEL_ID,
        photo=product.image,
        caption=product.to_message(),
        parse_mode="HTML",
    )


async def _handler(event: Optional[Dict], context: Optional[Dict]):
    products = await sahibinden_client.get_products(SOURCE_URL)
    logging.info(f"Found products: {[p.id for p in products]}")

    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    async with S3ObjectsTracker(**settings.s3_credentials) as tracker:
        for product in tracker.determine_new(products):
            await send_message(bot, product)
            await tracker.publish(product)
            logging.info(f"Published new product: {product}")
            await asyncio.sleep(1)


def handler(event: Optional[Dict], context: Optional[Dict]):
    """
    Synchronous wrapper of `_handler`, that can be called trough command line.
    Yandex.Function do it this way..
    """
    asyncio.run(_handler(event, context))


if __name__ == "__main__":
    handler(None, None)
