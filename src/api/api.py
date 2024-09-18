from fastapi import APIRouter, Depends

from .routers import student, thread, comment
from ..dependencies import verify_token

router = APIRouter(
    prefix="/api",
    tags=["api"],
    dependencies=[Depends(verify_token)],
    responses={404: {"description": "Not found"}}
)

router.include_router(student.router)
router.include_router(thread.router)
router.include_router(comment.router)