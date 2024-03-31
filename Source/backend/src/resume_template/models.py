from typing import Optional

from pydantic import BaseModel


class ResumeTemplate(BaseModel):
    description: Optional[str] = None

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "description": "Creative"
            }
        }
