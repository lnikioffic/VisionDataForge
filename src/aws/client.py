import asyncio
import aiofiles
from aiobotocore.session import get_session
from contextlib import asynccontextmanager
from src.config import settings
from pathlib import Path


class S3Client:
    def __init__(
        self, access_key: str, secret_key: str, endpoint_url: str, bucket_name: str
    ) -> None:
        self.config = {
            'aws_access_key_id': access_key,
            'aws_secret_access_key': secret_key,
            'endpoint_url': endpoint_url,
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client('s3', **self.config) as client:
            yield client

    async def upload_bytes(self, file: bytes, file_name: str):
        async with self.get_client() as client:
            await client.put_object(Bucket=self.bucket_name, Key=file_name, Body=file)

    async def upload_file_path(self, file_path: str, file_name: str):
        async with aiofiles.open(file_path, 'rb') as file:
            content = await file.read()
            await self.upload_bytes(content, file_name)

    async def delete_file(self, file_name: str):
        async with self.get_client() as client:
            await client.delete_object(self.bucket_name, file_name)

    async def get_file(self, file_name: str):
        async with self.get_client() as client:
            response = await client.get_object(self.bucket_name, file_name)
        async with response['Body'] as stream:
            data = await stream.read()
        return data


s3_client = S3Client(
    access_key=settings.AWS_ACCESS_KEY_ID,
    secret_key=settings.AWS_SECRET_ACCESS_KEY,
    endpoint_url='https://s3.storage.selcloud.ru/',
    bucket_name='test-forge',
)
