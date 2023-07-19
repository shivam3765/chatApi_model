from pydantic import BaseModel


class Doc(BaseModel):
    pdf_url: str
    subject: str