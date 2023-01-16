from fastapi import FastAPI, Request, Form, Depends
from typing import Optional
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from schemas import MyForm
from enum import Enum
import uvicorn

import numpy as np
import pandas as pd
import pickle

model = pickle.load(open("model.pkl", "rb"))

app = FastAPI()

templates = Jinja2Templates(directory="templates/")

type_of_iris = {0: 'Iris-setosa', 1: 'Iris-versicolor', 2: 'Iris-virginica'}



@app.get("/", response_class=HTMLResponse)
def redirect_fastapi(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/new_form", response_class=HTMLResponse)
def post_form(request: Request):
    result = "Type a number"
    return templates.TemplateResponse("test_item.html", {"request": request, 'result': result})


@app.post("/new_form", response_class=HTMLResponse)
def post_form(request: Request, form_data : MyForm = Depends(MyForm.as_form)):
    print(form_data)

    sepal_length = form_data.sepal_length
    sepal_width  = form_data.sepal_width
    petal_length = form_data.petal_length
    petal_width  = form_data.petal_width 

    # if not all([sepal_length, sepal_width, petal_length, petal_width]):
    #     result = "Neeed 4 numbers"
    # else:

    predict = model.predict([
        [sepal_length,
        sepal_width,
        petal_length,
        petal_width]
    ])
    res1 = np.argmax(predict, axis=1)[0]
    res2 = np.max(predict, axis=1)[0]

    res2 = np.round(res2, 4)

    result = f"Model dumayet, 4to etot iris - {type_of_iris[res1]}, s vero9tnost'u {res2}"
    return templates.TemplateResponse("test_item.html", {"request": request, 'result': result})


# class CommonQueryParams:
#     def __init__(self, 
#                  sepal_length : float | None = None,
#                  sepal_width  : float | None = None,
#                  petal_length : float | None = None,
#                  petal_width  : float | None = None):
#         self.sepal_length = sepal_length
#         self.sepal_width  = sepal_width 
#         self.petal_length = petal_length 
#         self.petal_width  = petal_width 


# @app.get("/items/", response_class=HTMLResponse)
# def read_items(request: Request):

#     result = "Type a number"
#     return templates.TemplateResponse("test_item.html", {"request": request, 'result': result})


# @app.post("/items/", response_class=HTMLResponse)
# def read_items(request: Request, form_data: CommonQueryParams = Depends(CommonQueryParams)):
#     print(form_data)

#     sepal_length = Form()
#     sepal_width  = Form()
#     petal_length = Form()
#     petal_width  = Form()

#     result = str(1)
#     if petal_length:
#         print(sepal_length, sepal_width, petal_length, petal_width)
#         result = str(2)

    

#     return templates.TemplateResponse("test_item.html", {"request": request, 'result': result})

#     result = "Type a number"
#     return templates.TemplateResponse("new_form.html", {"request": request, 'result': result})

#     response = {}
#     if commons.q:
#         response.update({"q": commons.q})
#     items = fake_items_db[commons.skip : commons.skip + commons.limit]
#     response.update({"items": items})
#     return response



# 
# Криво сделано, но работает, если че
# 


# @app.get("/form")
# def form_post(request: Request):
#     result = "Type a number"
#     return templates.TemplateResponse('test_item.html', context={'request': request, 'result': result})


# @app.post("/form")
# def form_post(request: Request, 
#               num1: int = Form(), 
#               num2: int = Form(), 
#               num3: int = Form(), 
#               num4: int = Form()):
#     predict = model.predict([
#         [num1,
#          num2,
#          num3,
#          num4]
#     ])

#     res1 = np.argmax(predict, axis=1)[0]
#     res2 = np.max(predict, axis=1)[0]

#     result = f"Model dumayet, 4to etot iris - {type_of_iris[res1]}, s vero9tnost'u {np.round(res2, 4)}"
#     return templates.TemplateResponse('test_item.html', context={'request': request, 'result': result})