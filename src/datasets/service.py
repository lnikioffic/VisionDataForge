from sqlalchemy.engine import Result
from sqlalchemy import func, select, delete
from sqlalchemy.orm import joinedload, selectinload

from src.datasets.models import TypeDataset, Dataset
from src.datasets.schemas import TypeDatasetRead, DatasetCreate, DatasetRead
from src.service import Service


class TypeDatasetService(Service):
    async def get_type_by_id(self, id) -> TypeDatasetRead | None:
        type = await self.session.get(TypeDataset, id)
        return type

    async def get_types(self) -> list[TypeDatasetRead]:
        stmt = select(TypeDataset)
        result: Result = await self.session.execute(stmt)
        types = result.scalars().all()
        return list(types)


class DatasetService(Service):
    async def get_dataset_for_sale(
        self, page: int = 1, per_page: int = 10
    ) -> list[DatasetRead]:
        stmt = (
            select(Dataset)
            .filter(Dataset.for_sale == True)
            .options(selectinload(Dataset.user), selectinload(Dataset.type_dataset))
            .limit(per_page)
            .offset((page - 1) * per_page)
        )
        result: Result = await self.session.execute(stmt)
        datasets = result.scalars().all()
        return list(datasets)

    async def get_count_dataset_for_sale(self) -> int:
        stmt = select(
            func.count(Dataset.id)
        ).filter(  # используем func.count() для подсчета количества записей
            Dataset.for_sale == True
        )
        result: Result = await self.session.execute(stmt)
        total_count = (
            result.scalar()
        )  # используем result.scalar() для получения самого значения
        return total_count

    async def create_dataset(
        self, dataset: DatasetCreate, type_dataset_id: int, user_id: int
    ) -> DatasetRead:
        dataset_db = Dataset(
            **dataset.model_dump(), user_id=user_id, type_dataset_id=type_dataset_id
        )
        self.session.add(dataset_db)
        await self.session.commit()
        return dataset_db

    async def get_dataset_by_user_id(self, id) -> list[DatasetRead]:
        stmt = (
            select(Dataset)
            .filter(Dataset.user_id == id)
            .options(selectinload(Dataset.user), selectinload(Dataset.type_dataset))
        )
        result: Result = await self.session.execute(stmt)
        datasets = result.scalars().all()
        return list(datasets)

    async def get_dataset_by_id(self, id) -> DatasetRead:
        stmt = (
            select(Dataset)
            .filter(Dataset.id == id)
            .options(selectinload(Dataset.user), selectinload(Dataset.type_dataset))
        )
        result: Result = await self.session.execute(stmt)
        dataset = result.scalar()
        return dataset

    async def delete_dataset_by_id(self, id):
        try:
            stmt = delete(Dataset).filter(Dataset.id == id)
            await self.session.execute(stmt)
            await self.session.commit()
        except Exception as ex:
            await self.session.rollback()
            return f'excption {ex}'
