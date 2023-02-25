from fastapi import FastAPI, Request, Form, Depends, status
from typing import Optional
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from schemas import Flower
from enum import Enum
import uvicorn

import numpy as np
import pandas as pd
import pickle

from sqlalchemy.orm import Session

import models

from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

model = pickle.load(open("model.pkl", "rb"))

app = FastAPI()

templates = Jinja2Templates(directory="templates/")

type_of_iris = {0: 'Iris-setosa', 1: 'Iris-versicolor', 2: 'Iris-virginica'}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/predict")
def predict(request: Request, db: Session = Depends(get_db)):
    flowers = db.query(models.Flowers_db).all()
    return templates.TemplateResponse("template.html", {"request": request, "flowers_list": flowers})


@app.post("/predict/add")
def add(request: Request, form_data : Flower = Depends(Flower.as_form), db: Session = Depends(get_db)):
    print(form_data)

    sepal_length = form_data.sepal_length
    sepal_width  = form_data.sepal_width
    petal_length = form_data.petal_length
    petal_width  = form_data.petal_width 

    predict = model.predict([
        [sepal_length,
        sepal_width,
        petal_length,
        petal_width]
    ])
    res = np.argmax(predict, axis=1)[0]

    new_flower = models.Flowers_db(input=f"({sepal_length}, {sepal_width}, {petal_length}, {petal_width})", output=type_of_iris[res])
    db.add(new_flower)
    db.commit()

    url = app.url_path_for("predict")
    return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)


@app.get("/delete/{flower_id}")
def delete(request: Request, flower_id: int, db: Session = Depends(get_db)):
    flower = db.query(models.Flowers_db).filter(models.Flowers_db.id == flower_id).first()
    db.delete(flower)
    db.commit()

    url = app.url_path_for("predict")
    return RedirectResponse(url=url, status_code=status.HTTP_302_FOUND)