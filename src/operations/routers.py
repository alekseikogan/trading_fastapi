from http.client import HTTPException
import time
from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_cache.decorator import cache
from src.database import get_async_session

from .models import operation

router = APIRouter(
    prefix='/operations',
    tags=['Operations']
)


@router.get('/')
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    """Выдача операций запрошенного типа."""
    try:
        query = select(operation).where(operation.c.type == operation_type)
        result = await session.execute(query)
        return {
            'status': 'error',
            'result': result.all(),
            'details': None
            }
    except Exception:
        raise HTTPException(
            status_code=500,
            detail={
                'status': 'error',
                'data': None,
                'details': None
            }
        )


@router.post('/')
async def add_specific_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    """Добавление операции."""
    stmt = insert(operation).values(**new_operation.dict())
    await session.execute(stmt)
    return {'status': 'success'}


@router.get('long_operation')
@cache(expire=30)
def get_long_oper():
    time.sleep(3)
    return 'Данных много, поэтому они вычислялись 3 секунды!'
