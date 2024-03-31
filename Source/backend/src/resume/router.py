import shutil
import os

from fastapi import APIRouter, Body, Request, status, UploadFile, File
from fastapi.responses import FileResponse

from starlette.exceptions import HTTPException

from src.models import ResponseModel, ErrorResponseModel
from src.resume.models import Resume, ResumeUpdate, AIBaseInfo, SelectResumeTemplate
from src.resume.services.resume_builder import resume_builder
from src.resume.services.resume_parser import resume_parser
from src.resume.services.ai_resume_writer import ai_resume_writer

import src.resume.dependencies as resumes

# constants
STATUS_CODE = 0
DATA = 1
ERROR = 1

# set router
router = APIRouter(prefix="/resume", tags=["Resume"])


@router.post("/", response_description="Create a new resume", status_code=status.HTTP_200_OK)
def create_resume(request: Request, resume: Resume = Body(...)):
    """Creates a resume"""
    try:
        return ResponseModel(data=resumes.create_resume(request, resume), code=status.HTTP_200_OK,
                             message="Resume created successfully.")
    except HTTPException as e:
        return ErrorResponseModel(error=e.detail, code=e.status_code, message="An error occurred")


@router.get("/", response_description="Get a list of resumes")
def retrieve_resumes(request: Request):
    """Gets all resumes"""
    try:
        return ResponseModel(data=resumes.retrieve_resumes(request), code=status.HTTP_200_OK,
                             message="Resumes retrieved successfully.")
    except HTTPException as e:
        return ErrorResponseModel(error=e.detail, code=e.status_code, message="An error occurred")


@router.get("/{id}", response_description="Get a resume by its id")
def retrieve_resume(request: Request, id: str):
    """Gets a resume"""
    try:
        return ResponseModel(data=resumes.retrieve_resume(request, id), code=status.HTTP_200_OK,
                             message="Resume retrieved successfully.")
    except HTTPException as e:
        return ErrorResponseModel(error=e.detail, code=e.status_code, message="An error occurred")


@router.put("/{id}", response_description="Update a resume by its id")
def update_resume(request: Request, id: str, resume_update: ResumeUpdate = Body(...)):
    """Updates a resume"""
    try:
        return ResponseModel(data=resumes.update_resume(request, id, resume_update), code=status.HTTP_200_OK,
                             message="Resume updated successfully.")
    except HTTPException as e:
        return ErrorResponseModel(error=e.detail, code=e.status_code, message="An error occurred")


@router.delete("/{id}", response_description="Delete a resume by its id")
def delete_resume(request: Request, id: str):
    """Deletes a resume"""
    try:
        return ResponseModel(data=resumes.delete_resume(request, id), code=status.HTTP_200_OK,
                             message="Resume deleted successfully.")
    except HTTPException as e:
        return ErrorResponseModel(error=e.detail, code=e.status_code, message="An error occurred")


@router.post("/parse/", response_description="Upload and parse a resume")
async def parse_resume(file: UploadFile = File(...)):
    """
        Uploads a resume and parses the resume by using online resume parser service.
    """

    # If files directory doesn't exist, make folder named files. Uploaded resumes will be stored into the folder.
    os.makedirs('files', exist_ok=True)

    file_location = f"files/{file.filename}"

    # Copy uploaded resume to file folder
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Parse a resume by using resume parser online service
    result = resume_parser.parse_resume_by_eden_ai(file.filename)

    if result[STATUS_CODE] == status.HTTP_200_OK:
        return ResponseModel(data=result[DATA], code=result[STATUS_CODE], message="Resume parsed successfully")
    else:
        return ErrorResponseModel(error=result[ERROR], code=result[STATUS_CODE], message="An error occurred")


@router.get("/files/{filename}", response_description="Download a resume")
async def download_resume(filename: str):
    """Downloads a file"""

    # check if file exists
    if os.path.isfile(f'files/{filename}'):
        return FileResponse(f'files/{filename}', media_type='application/octet-stream', filename=filename)
    else:
        return ErrorResponseModel(code=status.HTTP_404_NOT_FOUND, message="file not found")


@router.post("/write_description/", response_description="Write description of resume by AI")
async def write_description(ai_base_info: AIBaseInfo = Body(...)):
    """
    Writes or Completes description based on the information that users provide by OpenAI
    """

    try:
        return ResponseModel(data=ai_resume_writer.write_description(ai_base_info), code=status.HTTP_200_OK,
                             message="Written by AI successfully")
    except HTTPException as e:
        return ErrorResponseModel(error=e.detail, code=e.status_code, message="An error occurred")


@router.post("/select_template/", response_description="Select a resume template")
def select_resume_template(request: Request, select_resume_template: SelectResumeTemplate = Body(...)):
    """Rebuild resume with selected resume template"""

    try:
        resume_dict = resumes.retrieve_resume(request, select_resume_template.resume_id)
        resume = Resume.parse_obj(resume_dict)
        resume_builder.build_resume(select_resume_template.resume_id, resume, select_resume_template.template_id)
        return ResponseModel(data=None, code=status.HTTP_200_OK,
                             message="Rebuild with the template successfully")
    except HTTPException as e:
        return ErrorResponseModel(error=e.detail, code=e.status_code, message="An error occurred")
