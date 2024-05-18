from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from operations.routers import get_specific_operations

router = APIRouter(
    prefix='/pages',
    tags=['Pages']
)

templates = Jinja2Templates(directory='templates')


@router.get('/')
def get_base_template(request: Request):
    return templates.TemplateResponse(
        'index.html',
        {
            'request': request
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
