from fastapi import APIRouter

from .auth import create_auth_router
from .user import create_user_router
from .virtual_machine import create_virtual_machine_router
from presentation.ws.controllers import create_connection_status_router


app_router = APIRouter()
app_router.include_router(create_auth_router())
app_router.include_router(create_user_router())
app_router.include_router(create_virtual_machine_router())
app_router.include_router(create_connection_status_router(), prefix="/ws")
