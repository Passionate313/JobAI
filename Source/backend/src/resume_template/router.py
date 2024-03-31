import os

from fastapi import APIRouter, Body, Request
from fastapi.responses import FileResponse
from starlette import status
from starlette.exceptions import HTTPException

from src.models import ResponseModel, ErrorResponseModel
from src.resume_template.models import ResumeTemplate
from src.resume_template import dependencies as resume_templates

# set router
router = APIRouter(prefix="/resume_template", tags=["Resume_Template"])


@router.post("/", response_description="Create a new resume template", status_code=status.HTTP_200_OK)
async def create_resume(request: Request,
                        resume_template: ResumeTemplate = Body(...)):
    """Creates a resume"""
    try:
        return ResponseModel(data=resume_templates.create_resume_template(request, resume_template),
                             code=status.HTTP_200_OK,
                             message="Resume Template created successfully.")
    except HTTPException as e:
        return ErrorResponseModel(error=e.detail, code=e.status_code, message="An error occurred")


@router.get("/", response_description="Get a list of resume templates")
def retrieve_resumes(request: Request):
    """Gets all resume templates"""
    try:
        return ResponseModel(data=resume_templates.retrieve_resume_templates(request), code=status.HTTP_200_OK,
                             message="Resume Templates retrieved successfully.")
    except HTTPException as e:
        return ErrorResponseModel(error=e.detail, code=e.status_code, message="An error occurred")


@router.get("/{id}", response_description="Get a resume template by its id")
def retrieve_resume(request: Request, id: str):
    """Gets a resume template"""
    try:
        return ResponseModel(data=resume_templates.retrieve_resume_template(request, id), code=status.HTTP_200_OK,
                             message="Resume template retrieved successfully.")
    except HTTPException as e:
        return ErrorResponseModel(error=e.detail, code=e.status_code, message="An error occurred")


@router.put("/{id}", response_description="Update a resume by its id")
def update_resume(request: Request, id: str, resume_template_update: ResumeTemplate = Body(...)):
    """Updates a resume"""
    try:
        return ResponseModel(data=resume_templates.update_resume_template(request, id, resume_template_update),
                             code=status.HTTP_200_OK,
                             message="Resume updated successfully.")
    except HTTPException as e:
        return ErrorResponseModel(error=e.detail, code=e.status_code, message="An error occurred")


@router.delete("/{id}", response_description="Delete a resume by its id")
def delete_resume(request: Request, id: str):
    """Deletes a resume"""
    try:
        return ResponseModel(data=resume_templates.delete_resume_template(request, id), code=status.HTTP_200_OK,
                             message="Resume deleted successfully.")
    except HTTPException as e:
        return ErrorResponseModel(error=e.detail, code=e.status_code, message="An error occurred")


@router.get("/files/{filename}", response_description="Download a resume template")
async def download_resume(filename: str):
    """Downloads a file"""

    # check if file exists
    if os.path.isfile(f'src/resume_template/templates/{filename}'):
        return FileResponse(
            f'src/resume_template/templates/{filename}',
            media_type='application/octet-stream',
            filename=filename
        )
    else:
        return ErrorResponseModel(code=status.HTTP_404_NOT_FOUND, message="file not found")
