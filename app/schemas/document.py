from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: int
    filename: str
    stored_filename: str

    model_config = {
        "from_attributes": True
    }
