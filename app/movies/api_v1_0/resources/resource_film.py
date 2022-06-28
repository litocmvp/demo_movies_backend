from . import api
from ..schemas import FilmSchema, GenderSchema, RatinSchema
from ...models import FilmModel, GenderModel, GenderFilmModel, RatingModel
from flask import request
from flask_restful import Resource

movie_schema = FilmSchema()


