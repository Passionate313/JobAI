from fastapi import APIRouter
from src.resume import router as resume_router
from src.resume_template import router as resume_template_router

router = APIRouter()
router.include_router(resume_router.router)
router.include_router(resume_template_router.router)
