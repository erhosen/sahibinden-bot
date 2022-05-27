import logging
import sys

import httpx
from bs4 import BeautifulSoup
from core import Product
from fake_headers import Headers
from settings import settings


class SahibindenClient:
    BASE_URL = "https://www.sahibinden.com"

    def __init__(self, timeout: int):
        self.timeout = timeout
        self.fake_headers = Headers(headers=True)  # do generate misc headers

    async def _make_request(self, url: str) -> httpx.Response:
        for proxies in settings.httpx_proxies:
            try:
                async with httpx.AsyncClient(timeout=self.timeout, proxies=proxies, verify=False) as client:
                    response = await client.get(url, headers=self.fake_headers.generate())
                    if response.status_code == 200:
                        return response
                    else:
                        logging.error(f"Sahibinden unexpected status: {response.status_code}")
                        continue
            except Exception as exc:
                logging.error(f"Sahibinden request error: {exc}", exc_info=True)
                continue

        logging.error("Sahibinden request error: No proxies available")
        sys.exit(-1)

    async def get_products(self, list_url: str) -> list[Product]:
        response = await self._make_request(list_url)
        soup = BeautifulSoup(response.content, "html.parser")
        results_items = soup.find_all("tr", {"class": "searchResultsItem"})

        product_list = []
        for result_item in results_items:
            try:
                if len(result_item.attrs["class"]) > 1:  # searchResultsPromoSuper and other ads
                    continue
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
                )
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


sahibinden_client = SahibindenClient(settings.SAHIBINDEN_TIMEOUT)
