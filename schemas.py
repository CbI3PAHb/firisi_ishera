from fastapi import Form
from typing import Optional
from pydantic import BaseModel

class MyForm(BaseModel):
    sepal_length : float
    sepal_width : float
    petal_length : float | None
    petal_width : float

    @classmethod
    def as_form(
        cls,
        sepal_length : float = Form(...),
        sepal_width : float = Form(...),
        petal_length : float | None = Form(...),
        petal_width : float = Form(...)
    ):
        return cls(    
            sepal_length = sepal_length,
            sepal_width = sepal_width, 
            petal_length = petal_length,
            petal_width = petal_width 
        )
