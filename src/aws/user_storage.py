from pathlib import Path

from src.aws.client import s3_client
from src.users.schemas import UserRead


class UserStorage:
    def __init__(self, user: UserRead) -> None:
        self.user = user


class UserStorageSave(UserStorage):
    def __init__(
        self, user: UserRead, file_path: str, first_frame: bytes, second_frame: bytes
    ) -> None:
        super().__init__(user)
        self.file_path = file_path
        self.first_frame = first_frame
        self.second_frame = second_frame

        self.folder_path_save = f'users/{user.username}/{Path(file_path).stem}'

        if user.is_superuser:
            self.folder_path_save = f'corp/{Path(file_path).stem}_{user.username}'

        self.file_path_save = f'{self.folder_path_save}/{Path(file_path).name}'
        self.first_frame_path_save = f'{self.folder_path_save}/first_frame.jpg'
        self.second_frame_path_save = f'{self.folder_path_save}/second_frame.jpg'

    async def save_file(self):
        await s3_client.upload_file_path(self.file_path, self.file_path_save)

    async def save_bytes_as_file(self):
        await s3_client.upload_bytes(self.first_frame, self.first_frame_path_save)
        await s3_client.upload_bytes(self.second_frame, self.second_frame_path_save)


class UserStorageController(UserStorage):
    def __init__(self, user: UserRead) -> None:
        super().__init__(user)

    async def delet_files(self, files_names: list[str]):
        for file_name in files_names:
            await s3_client.delete_file(file_name)

    async def get_file(self, file_name: str):
        data = await s3_client.get_file(file_name)
        return data
