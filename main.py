# -*- coding: utf-8 -*-
"""
Created on Sun Oct  5 21:25:49 2025

@author: DELL
"""

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from models import Visitor, Base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import os

app = FastAPI()
#    engine = create_engine("sqlite:///test.db")
import os
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def read_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/submit")
def submit_form(nombre: str = Form(...), categoria: str = Form(...)):
    tag = categoria.lower()
    with Session(engine) as session:
        visitor = Visitor(nombre=nombre, categoria=categoria, lead_tag=tag)
        session.add(visitor)
        session.commit()
    return {"message": "Form submitted", "lead_tag": tag}

# Route to append the registered visitors 
from fastapi.responses import HTMLResponse

# DB in Table form
@app.get("/visitors", response_class=HTMLResponse)
def list_visitors():
    with Session(engine) as session:
        visitors = session.query(Visitor).all()
        html = """
        <h2>Visitor List</h2>
        <table border="1" cellpadding="5">
            <tr><th>Nombre</th><th>Categoría</th><th>Lead Tag</th></tr>
        """
        for v in visitors:
            html += f"<tr><td>{v.nombre}</td><td>{v.categoria}</td><td>{v.lead_tag}</td></tr>"
        html += "</table>"
    return HTMLResponse(content=html)

# Add search adn filter to the table above
@app.get("/search", response_class=HTMLResponse)
def search_visitors(request: Request, nombre: str = "", categoria: str = ""):
    with Session(engine) as session:
        query = session.query(Visitor)
        if nombre:
            query = query.filter(Visitor.nombre.ilike(f"%{nombre}%"))
        if categoria:
            query = query.filter(Visitor.categoria.ilike(f"%{categoria}%"))
        visitors = query.all()

        html = """
        <h2>Search Visitors</h2>
        <form method="get">
            <input name="nombre" placeholder="Nombre" value="{0}" />
            <input name="categoria" placeholder="Categoría" value="{1}" />
            <button type="submit">Buscar</button>
        </form>
        <table border="1" cellpadding="5">
            <tr><th>Nombre</th><th>Categoría</th><th>Lead Tag</th></tr>
        """.format(nombre, categoria)

        for v in visitors:
            html += f"<tr><td>{v.nombre}</td><td>{v.categoria}</td><td>{v.lead_tag}</td></tr>"
        html += "</table>"
    return HTMLResponse(content=html)
