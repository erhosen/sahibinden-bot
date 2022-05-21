import logging
import sys

import httpx
from bs4 import BeautifulSoup
from core import Product
from settings import settings


class SahibindenClient:
    BASE_URL = "https://www.sahibinden.com"

    def __init__(self, cookie: str):
        self.cookie = cookie

    def _get_headers(self) -> dict:
        return {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",  # noqa
            "cookie": self.cookie,
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36",  # noqa
            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
            "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
        }

    async def get_soup(self, url: str) -> BeautifulSoup:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url, headers=self._get_headers())
            if response.status_code == 200:
                return BeautifulSoup(response.content, "html.parser")
            else:
                logging.error(f"Sahibinden unexpected status: {response.status_code}")
                sys.exit(-1)

    async def get_products(self, list_url: str) -> list[Product]:
        list_response = await self.get_soup(list_url)
        results_items = list_response.findAll("tr", {"class": "searchResultsItem"})

        product_list = []
        for result_item in results_items:
            try:
                # Get product id
                item_id = int(result_item["data-id"])
                # Get product url
                item_link = result_item.find("a", {"class": "classifiedTitle"})["href"]
                item_link = f"{self.BASE_URL}{item_link}"
                # Get product image
                item_image = result_item.find("img")["src"]
                item_image = item_image.replace("/lthmb_", "/x5_")
                # Get product title
                item_title = result_item.find("a", {"class": "classifiedTitle"}).get_text(strip=True)
                # Get product price
                item_price = result_item.find("td", {"class": "searchResultsPriceValue"}).get_text(strip=True)
                # Get product location
                item_location = result_item.find("td", {"class": "searchResultsLocationValue"}).get_text(
                    " ", strip=True
                )  # noqa
                # Create product object
                product = Product(
                    id=item_id,
                    link=item_link,
                    image=item_image,
                    title=item_title,
                    price=item_price,
                    location=item_location,
                )
                product_list.append(product)
            except Exception:
                continue

        return product_list


sahibinden_client = SahibindenClient(settings.SAHIBINDEN_COOKIE)
