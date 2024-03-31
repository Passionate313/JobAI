from typing import Optional
from pydantic import BaseModel


# These models are used for creating, reading, deleting resumes.
class Contact(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    linkedin_url: Optional[str] = None
    personal_website: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None


class Experience(BaseModel):
    role: Optional[str] = None
    company: str
    exp_skills: Optional[str] = None
    exp_start: Optional[str] = None
    exp_end: Optional[str] = None
    exp_location: Optional[str] = None
    activity: Optional[str] = None


class Project(BaseModel):
    title: str
    organization: Optional[str] = None
    pro_start: Optional[str] = None
    pro_end: Optional[str] = None
    content: Optional[str] = None


class Education(BaseModel):
    degree: str
    university: Optional[str] = None
    edu_location: Optional[str] = None
    earn_year: Optional[str] = None
    specialization: Optional[str] = None
    gpa: Optional[str] = None


class Certification(BaseModel):
    name: str
    where: Optional[str] = None
    get_year: Optional[str] = None
    relevant: Optional[str] = None


class SkillSets(BaseModel):
    skills: Optional[str] = None
    tools: Optional[str] = None


class Resume(BaseModel):
    name: str
    exp: str
    contact: Optional[Contact] = None
    experience: Optional[list[Experience]] = None
    project: Optional[list[Project]] = None
    education: Optional[list[Education]] = None
    certification: Optional[list[Certification]] = None
    skill_sets: Optional[SkillSets] = None

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "name": "MyResume",
                "exp": "Software Engineer",
                "contact": {
                    "full_name": "Alex Newman",
                    "email": "alexnewman@gmail.com",
                    "phone_number": "+1(835)778-4510",
                    "linkedin_url": "https://www.linkedin.com/in/alex-newman-9109845",
                    "personal_website": "https://www.alex.com",
                    "city": "New York",
                    "state": "CA",
                    "country": "United State"
                },
                "experience": [
                    {
                        "role": "Software Engineer",
                        "company": "Google",
                        "exp_skills": "React, Vue",
                        "exp_start": "2023-08-08",
                        "exp_end": "2023-08-08",
                        "exp_location": "Canada",
                        "activity": "Developed a website"
                    }
                ],
                "project": [
                    {
                        "title": "AI Bot",
                        "organization": "Google",
                        "pro_start": "2023-08-08",
                        "pro_end": "2023-08-08",
                        "content": "Developed a AI Bot"
                    }
                ],
                "education": [
                    {
                        "degree": "Bachelor Degree of Computer Science",
                        "university": "York University",
                        "edu_location": "Ottawa",
                        "earn_year": "2018",
                        "specialization": "specialization",
                        "gpa": "gpa"
                    }
                ],
                "certification": [
                    {
                        "name": "React Expert",
                        "where": "York University",
                        "get_year": "2013",
                        "relevant": "relevant"
                    }
                ],
                "skill_sets": {
                    "skills": "React, Vue",
                    "tools": "Microservice"
                }
            }
        }


# These models are used for updating resumes.
# Properties of subclasses in ResumeUpdate should be optional.
class ExperienceUpdate(BaseModel):
    role: Optional[str] = None
    company: Optional[str] = None
    exp_skills: Optional[str] = None
    exp_start: Optional[str] = None
    exp_end: Optional[str] = None
    exp_location: Optional[str] = None
    activity: Optional[str] = None


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    organization: Optional[str] = None
    pro_start: Optional[str] = None
    pro_end: Optional[str] = None
    content: Optional[str] = None


class EducationUpdate(BaseModel):
    degree: Optional[str] = None
    university: Optional[str] = None
    edu_location: Optional[str] = None
    earn_year: Optional[str] = None
    specialization: Optional[str] = None
    gpa: Optional[str] = None


class CertificationUpdate(BaseModel):
    name: Optional[str] = None
    where: Optional[str] = None
    get_year: Optional[str] = None
    relevant: Optional[str] = None


class ResumeUpdate(BaseModel):
    name: Optional[str] = None
    exp: Optional[str] = None
    contact: Optional[Contact] = None
    experience: Optional[list[ExperienceUpdate]] = None
    project: Optional[list[ProjectUpdate]] = None
    education: Optional[list[EducationUpdate]] = None
    certification: Optional[list[CertificationUpdate]] = None
    skill_sets: Optional[SkillSets] = None

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "contact": {
                    "full_name": "Smart Resume"
                }
            }
        }


# It is used for writing experience, projects with AI
class AIBaseInfo(BaseModel):
    type: str
    prompt: str
    skills: Optional[str] = None
    experience: Optional[str] = None
    pre_experience: Optional[str] = None

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "type": "experience",
                "prompt": "React Developer",
                "experience": "Develop a website with React and Node.js"
            }
        }


# It is used for selecting resume template
class SelectResumeTemplate(BaseModel):
    template_id: str
    resume_id: str
