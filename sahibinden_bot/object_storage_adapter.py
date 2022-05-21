import json
from contextlib import AsyncExitStack
from typing import AsyncIterable, List

from aiobotocore import session
from core import Product, SahibindenMeta
from settings import settings


class ObjectStorageAdapter:
    def __init__(self, bucket):
        self._bucket = bucket
        self._filename = "data.json"
        self._exit_stack = AsyncExitStack()
        self._s3_client = None

        self.sahibinden_meta = None

    async def _get_meta_from_s3(self) -> SahibindenMeta:
        response = await self._s3_client.get_object(Bucket=self._bucket, Key=self._filename)
        async with response["Body"] as stream:
            raw_data = json.loads(await stream.read())
            return SahibindenMeta(**raw_data)

    async def _upload_meta_to_s3(self):
        self.sahibinden_meta.published_ids = self.sahibinden_meta.published_ids[-50:]
        json_str = self.sahibinden_meta.json() + "\n"
        await self._s3_client.put_object(
            Bucket=self._bucket,
            Key=self._filename,
            Body=json_str.encode("utf-8"),
            ContentType="application/json",
        )

    async def __aenter__(self) -> "ObjectStorageAdapter":
        boto_session = session.get_session()
        self._s3_client = await self._exit_stack.enter_async_context(
            boto_session.create_client(
                service_name="s3",
                endpoint_url="https://storage.yandexcloud.net",
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            )
        )
        self.sahibinden_meta = await self._get_meta_from_s3()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._exit_stack.__aexit__(exc_type, exc_val, exc_tb)

    async def determine_new_products(self, products: List[Product]) -> AsyncIterable[Product]:
        published_ids_set = set(self.sahibinden_meta.published_ids)
        for product in products:
            if product.id not in published_ids_set:
                yield product

    async def set_products_published(self, published_product_ids: List[int]):
        self.sahibinden_meta.published_ids += published_product_ids
        await self._upload_meta_to_s3()
