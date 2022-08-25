from typing import Any

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Body

from dependencies import get_db
from models.ingredient import Ingredient
from models.recipe import Recipe

router = APIRouter(prefix='/recipe')

