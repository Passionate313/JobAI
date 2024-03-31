from fastapi import Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from bson import ObjectId

from src.resume_template.models import ResumeTemplate
from src.resume_template.utils import resume_template_helper


def get_collection_resume_templates(request: Request):
    """
    Returns resume table with request

    :param request:
    :return: resume table object
    """
    return request.app.database["resume_templates"]


def create_resume_template(request: Request, resume_template: ResumeTemplate = Body(...)):
    """
    Creates a new resume_template and return the resume_template along with inserted resume id

    :param request: http request object
    :param resume_template: resume template object to create
    :return: the new created resume template
    """

    resume_template_dict = jsonable_encoder(resume_template)
    new_resume_template = get_collection_resume_templates(request).insert_one(resume_template_dict)
    created_resume_template = get_collection_resume_templates(request).find_one(
        {"_id": new_resume_template.inserted_id})
    return resume_template_helper(created_resume_template)


def retrieve_resume_template(request: Request, id: str):
    """
    Finds a resume by id and return it. But if not exist, raises HTTPException with 404 error

    :param request: Http request
    :param id: id of resume template to find
    :return: a resume template with given id
    """

    if resume := get_collection_resume_templates(request).find_one({"_id": ObjectId(id)}):
        return resume_template_helper(resume)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Resume Template with id {id} not found!")


def retrieve_resume_templates(request: Request):
    """
    Gets all resume templates

    :return: a list of resume templates
    """

    resume_templates = []
    for resume_template in get_collection_resume_templates(request).find():
        resume_templates.append(resume_template_helper(resume_template))
    return resume_templates


def delete_resume_template(request: Request, id: str):
    """
    Delete a resume template by its id. If the resume template with id doesn't exist, raises HTTPException with 404
    error

    :param request: http request
    :param id: the id of the resume template to delete
    :return: success message including deleted resume template id
    """

    deleted_resume_template = get_collection_resume_templates(request).delete_one({"_id": ObjectId(id)})

    if deleted_resume_template.deleted_count == 1:
        return f"Resume with id {id} deleted successfully"

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Resume with id {id} not found!")


def update_resume_template(request: Request, id: str, resume_template_update: ResumeTemplate):
    """
    Updates a resume with its id and new resume data to update. If the resume with given id doesn't exist,
    raises HttpException with 404 error

    :param request: http request
    :param id: the id of the resume template to update
    :param resume_template_update: the resume template data to update
    :return: the updated resume template
    """

    # removes all items with None as value
    resume_template_update = {k: v for k, v in resume_template_update.dict().items() if v is not None}

    # if resume template to update has at least one non-null item, updates resume template with its id and given data
    if len(resume_template_update) >= 1:
        update_result = get_collection_resume_templates(request).update_one(
            {
                "_id": ObjectId(id)
            },
            {
                "$set": resume_template_update
            }
        )

        # if resume template that has such id doesn't exist, raises 404 error
        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Resume template not found!")

    # if success, return the updated resume template
    if (existing_resume_template := get_collection_resume_templates(request)
            .find_one({"_id": ObjectId(id)})) is not None:
        # return updated resume template
        return resume_template_helper(existing_resume_template)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Resume Template not found!")
