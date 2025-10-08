# -*- coding: utf-8 -*-
"""
Created on Sun Oct  5 21:22:20 2025

@author: DELL
"""

# models.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Visitor(Base):
    __tablename__ = "visitors"
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    categoria = Column(String)
    lead_tag = Column(String)