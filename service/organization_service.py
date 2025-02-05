from sqlalchemy.future import select
from ..database import get_db
from models import Organization

async def create_organization(name: str, description: str, contact_info: str, website: str = None):
    """
    Создаёт новую организацию.
    """
    async for db in get_db():
        async with db as session:
            organization = Organization(
                name=name,
                description=description,
                contact_info=contact_info,
                website=website
            )
            session.add(organization)
            await session.commit()
            return organization

async def get_all_organizations():
    """
    Получает список всех организаций.
    """
    async for db in get_db():
        async with db as session:
            result = await session.execute(select(Organization))
            return result.scalars().all()

async def delete_organization(org_id: int):
    """
    Удаляет организацию.
    """
    async for db in get_db():
        async with db as session:
            result = await session.execute(select(Organization).where(Organization.id == org_id))
            organization = result.scalars().first()
            if organization:
                await session.delete(organization)
                await session.commit()
                return True
            return False
async def get_organization_by_id(org_id: int):
    """
    Получает организацию по ID.
    """
    async for db in get_db():
        async with db as session:
            result = await session.execute(select(Organization).where(Organization.id == org_id))
            return result.scalars().first()  # Вернёт None, если не найдено

async def update_organization(org_id: int, name: str = None, description: str = None, contact_info: str = None, website: str = None):
    """
    Обновляет информацию об организации. Можно передавать частичные изменения.
    """
    async for db in get_db():
        async with db as session:
            result = await session.execute(select(Organization).where(Organization.id == org_id))
            organization = result.scalars().first()
            if not organization:
                return None  # Если организации нет, вернуть None

            # Обновляем только те поля, которые переданы
            if name:
                organization.name = name
            if description:
                organization.description = description
            if contact_info:
                organization.contact_info = contact_info
            if website:
                organization.website = website

            await session.commit()
            return organization  # Возвращаем обновлённый объект