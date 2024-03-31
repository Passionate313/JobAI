from fastapi import Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from src.resume.models import Resume, ResumeUpdate
from bson import ObjectId

from src.resume.services.resume_builder import resume_builder
from src.resume.utils import resume_helper
from src.utils import delete_file


def get_collection_resumes(request: Request):
    """
    Returns resume table with request

    :param request:
    :return: resume table object
    """
    return request.app.database["resumes"]


def create_resume(request: Request, resume: Resume = Body(...)):
    """
    Creates a new resume and return the resume along with inserted resume id

    :param request: http request object
    :param resume: resume object to create
    :return: the new created resume
    """
    
    resume_dict = jsonable_encoder(resume)
    new_resume = get_collection_resumes(request).insert_one(resume_dict)
    created_resume = get_collection_resumes(request).find_one({"_id": new_resume.inserted_id})

    # build updated resume
    resume_builder.build_resume(str(new_resume.inserted_id), resume)

    return resume_helper(created_resume)


def retrieve_resume(request: Request, id: str):
    """
    Finds a resume by id and return it. But if not exist, raises HTTPException with 404 error

    :param request: Http request
    :param id: id of resume to find
    :return: a resume with given id
    """

    if resume := get_collection_resumes(request).find_one({"_id": ObjectId(id)}):
        return resume_helper(resume)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Resume with id {id} not found!")


def retrieve_resumes(request: Request):
    """
    Gets all resume

    :return: a list of resume
    """

    resumes = []
    for resume in get_collection_resumes(request).find():
        resumes.append(resume_helper(resume))
    return resumes


def delete_resume(request: Request, id: str):
    """
    Delete a resume by its id. If the resume with id doesn't exist, raises HTTPException with 404 error

    :param request: http request
    :param id: the id of the resume to delete
    :return: success message including deleted resume id
    """

    deleted_resume = get_collection_resumes(request).delete_one({"_id": ObjectId(id)})

    if deleted_resume.deleted_count == 1:
        # delete pdf and html resume file
        delete_file(f"files/{id}.pdf")
        delete_file(f"files/{id}.html")

        return f"Resume deleted successfully"

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Resume with id {id} not found!")


def update_resume(request: Request, id: str, resume_update: ResumeUpdate):
    """
    Updates a resume with its id and new resume data to update. If the resume with given id doesn't exist,
    raises HttpException with 404 error

    :param request: http request
    :param id: the id of the resume to update
    :param resume_update: the resume data to update
    :return: the updated resume
    """

    # removes all items with None as value
    resume_update = {k: v for k, v in resume_update.dict().items() if v is not None}

    # if resume to update has at least one non-null item, updates resume with its id and given data
    if len(resume_update) >= 1:
        update_result = get_collection_resumes(request).update_one({"_id": ObjectId(id)}, {"$set": resume_update})

        # if resume that has such id doesn't exist, raises 404 error
        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Resume not found!")

    # if success, return the updated resume
    if (existing_resume := get_collection_resumes(request).find_one({"_id": ObjectId(id)})) is not None:
        # build updated resume
        existing_resume_obj = Resume.parse_obj(existing_resume)
        resume_builder.build_resume(id, existing_resume_obj)

        # return updated resume
        return resume_helper(existing_resume)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Resume not found!")


