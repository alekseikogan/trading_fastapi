from conftest import async_session_maker, client
from sqlalchemy import insert, select

from auth.models import role


async def test_add_role():
    """Добавляет роль в тестовую базу."""

    async with async_session_maker() as session:
        stmt = insert(role).values(id=1, name='admin', permissions=None)
        await session.execute(stmt)
        await session.commit()

        query = select(role)
        result = await session.execute(query)
        assert result.all() == [(1, 'admin', None)], 'Роль не добавилась!'


def test_register():
    """Тестирование регистрации."""

    response = client.post(
        '/auth/register',
        json={
            "email": "string",
            "password": "string",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
            "username": "string",
            "role_id": 1
        }
    )

    assert response.status_code == 201, 'Ошибка при регистрации!'
