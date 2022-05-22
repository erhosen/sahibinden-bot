import json
from contextlib import AsyncExitStack
from typing import AsyncIterable, List, TypeVar

from aiobotocore import session
from pydantic import BaseModel
from settings import settings

T = TypeVar("T")


class ObjectStorageMeta(BaseModel):
    published_ids: List[int]


class ObjectStorageAdapter:
    def __init__(self, bucket):
        self._bucket = bucket
        self._filename = "data.json"
        self._exit_stack = AsyncExitStack()
        self._s3_client = None

        self._meta = None

    async def _get_meta_from_s3(self) -> ObjectStorageMeta:
        response = await self._s3_client.get_object(Bucket=self._bucket, Key=self._filename)
        async with response["Body"] as stream:
            raw_data = json.loads(await stream.read())
            return ObjectStorageMeta(**raw_data)

    async def _upload_meta_to_s3(self):
        self._meta.published_ids = self._meta.published_ids[-50:]
        json_str = self._meta.json() + "\n"
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
        self._meta = await self._get_meta_from_s3()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._exit_stack.__aexit__(exc_type, exc_val, exc_tb)

    async def determine_new_items(self, items: List[T]) -> AsyncIterable[T]:
        published_ids_set = set(self._meta.published_ids)
        for item in items:
            if item.id not in published_ids_set:  # type: ignore
                yield item

    async def set_published_items(self, published_items: List[T]):
        self._meta.published_ids += [item.id for item in published_items]  # type: ignore
        await self._upload_meta_to_s3()
