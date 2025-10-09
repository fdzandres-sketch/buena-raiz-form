# -*- coding: utf-8 -*-
"""
Created on Sun Oct  5 21:25:49 2025

@author: DELL
"""
# main.py
from fastapi import FastAPI, Form
from models import Visitor, Base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import os

app = FastAPI()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///test.db")
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

@app.post("/submit")
def submit_form(
    nombre: str = Form(...),
    categoria: str = Form(...),
    telefono_movil: str = Form(...),
    geo_location: str = Form(...),
    price_history: str = Form(...)
):
    tag = categoria.lower()
    with Session(engine) as session:
        visitor = Visitor(
            nombre=nombre,
            categoria=categoria,
            telefono_movil=telefono_movil,
            geo_location=geo_location,
            price_history=price_history,
            lead_tag=tag
        )
        session.add(visitor)
        session.commit()
    return {"message": "Form submitted", "lead_tag": tag}