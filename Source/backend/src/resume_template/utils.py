def resume_template_helper(resume_template) -> dict:
    """Converts _id of resume template from ObjectId to str"""
    return {
        "id": str(resume_template["_id"]),
        "description": resume_template["description"]
    }
