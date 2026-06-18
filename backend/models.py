from pydantic import BaseModel


class CourseCreate(BaseModel):
    name: str
    desc: str
    color: str


class Course(BaseModel):
    id: str
    name: str
    desc: str
    color: str
