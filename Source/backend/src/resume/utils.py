from pdf2image import convert_from_path

from src.resume.models import Resume, Contact, ExperienceUpdate, EducationUpdate
from src.utils import get_year_from_date_string, get_first_value_of_list


def resume_helper(resume) -> dict:
    """Converts _id of resume from ObjectId to str"""
    return {
        "id": str(resume["_id"]),
        "name": resume["name"],
        "exp": resume["exp"],
        "contact": resume["contact"],
        "experience": resume["experience"],
        "project": resume["project"],
        "education": resume["education"],
        "certification": resume["certification"],
        "skill_sets": resume["skill_sets"]
    }


def map_resume_to_builder_pattern(resume: Resume):
    """
    This function is used for mapping Resume model to data schema for building resume.
    In experience, project, converts '\n' to '<br>' to implement line break
    """

    # experience
    if resume.experience:
        experiences = []
        for experience in resume.experience:
            if experience.activity:
                experience.activity = experience.activity.replace("\n", "<br>")
            if experience.exp_start:
                experience.exp_start = experience.exp_start[:7]
            if experience.exp_end:
                experience.exp_end = experience.exp_end[:7]
            experiences.append(experience)
        resume.experience = experiences

    # project
    if resume.project:
        projects = []
        for project in resume.project:
            if project.content:
                project.content = project.content.replace("\n", "<br>")
            projects.append(project)
        resume.project = projects

    return resume


def map_parsed_result_to_resume(parsed_result):
    """
    Maps result parsed by Eden AI Resume Parser online service to resume model.
    """
    resume = Resume(name="Resume", exp="Software Engineer")

    # contact
    contact = parsed_result["personal_infos"]
    resume.contact = Contact(
        full_name=contact["name"]["raw_name"],
        email=get_first_value_of_list(contact["mails"]),
        phone_number=get_first_value_of_list(contact["phones"]),
        personal_website=get_first_value_of_list(contact["urls"]),
        city=contact["address"]["city"],
        state=contact["address"]["region"],
        country=contact["address"]["country"]
    )

    # experience
    experiences = []
    parsed_work_experiences = parsed_result["work_experience"]
    for work_experience in parsed_work_experiences["entries"]:
        experience = ExperienceUpdate(
            role=work_experience["title"],
            company=work_experience["company"],
            exp_start=work_experience["start_date"],
            exp_end=work_experience["end_date"],
            exp_location=work_experience["location"]["formatted_location"],
            activity=work_experience["description"],
        )
        experiences.append(experience)
    resume.experience = experiences

    # education
    educations = []
    parsed_educations = parsed_result["education"]
    for parsed_education in parsed_educations["entries"]:
        education = EducationUpdate(
            degree=parsed_education["accreditation"],
            university=parsed_education["establishment"],
            edu_location=parsed_education["location"]["formatted_location"],
            earn_year=get_year_from_date_string(parsed_education["end_date"]),
            gpa=str(parsed_education["gpa"]),
        )
        educations.append(education)
    resume.education = educations

    return resume


def convert_first_page_to_image(resume_id):
    images = convert_from_path(f"files/{resume_id}.pdf")
    # Save the first image from the list of images.
    if len(images) > 0:
        images[0].save(f"files/{resume_id}.jpeg", "JPEG")  # you can save it in other formats like 'PNG'
