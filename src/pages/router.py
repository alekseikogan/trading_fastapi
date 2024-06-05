from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from operations.routers import get_specific_operations
from database import get_async_session
from operations.models import operation

router = APIRouter(
    prefix='/pages',
    tags=['Pages']
)

templates = Jinja2Templates(directory='templates')


@router.get('/')
async def get_index_template(request: Request, session: AsyncSession = Depends(get_async_session)):
    """Выдача главной страницы."""

    query = select(operation)
    result = await session.execute(query)
    return templates.TemplateResponse(
        'index.html',
        {
            'request': request,
            'operations': result.all(),
        }
    )


@router.get('/search/{operation_type}')
def get_search_page(request: Request, operations=Depends(get_specific_operations)):
    return templates.TemplateResponse(
        'search.html',
        {
            'request': request,
            'operations': operations['data']
        }
    )
