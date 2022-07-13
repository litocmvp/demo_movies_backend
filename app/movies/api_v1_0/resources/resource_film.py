from app.db import db
from . import api
from ..schemas import FilmSchema, GenderSchema, RatinSchema
from ...models import UserModel, FilmModel, GenderModel, GenderFilmModel, RatingModel
from flask import request, abort
from flask_restful import Resource

movie_schema = FilmSchema()
rating_schema = RatinSchema()
gender_schema = GenderSchema()

class RatingListResource(Resource):
    def get(self):
        ratings = RatingModel.get_all()
        resp = rating_schema.dump(ratings, many=True)
        return resp, 201

class RatingResource(Resource):
    @UserModel.token_required
    def post(current_user, self):
        if not current_user.admin : return abort(403)
        data = request.get_json()
        rating_dict = rating_schema.load(data)
        new_rating = RatingModel(rating = rating_dict['rating'],
                                description = rating_dict['description'],
                                picture = rating_dict['picture'])
        new_rating.save()
        resp = rating_schema.dump(new_rating)
        return {'icon':'success', 'msg': 'Registro Exitoso' ,'record': resp}, 201
    @UserModel.token_required
    def put(current_user, self, id):
        if not current_user.admin : return abort(403)
        data = request.get_json()
        rating_dict = rating_schema.load(data)
        RatingModel.update(id, rating_dict['rating'], rating_dict['description'], rating_dict['picture'])
        old_rating = RatingModel.get_by_id(id)
        resp = rating_schema.dump(old_rating)
        return {'icon':'success', 'msg': 'Actualización Exitosa' ,'record': resp}, 201
    @UserModel.token_required
    def delete(current_user, self, id):
        if not current_user.admin : return abort(403)
        delete_record = RatingModel.get_by_id(id)
        delete_record.delete()
        return {'icon':'warning', 'msg': 'Eliminación Exitosa'}, 201

class GenderListResource(Resource):
    def get(self):
        genders = GenderModel.get_all()
        resp = gender_schema.dump(genders, many=True)
        return resp, 201

class GenderResource(Resource):
    @UserModel.token_required
    def post(current_user, self):
        if not current_user.admin : return abort(403)
        data = request.get_json()
        gender_dict = gender_schema.load(data)
        new_gender = GenderModel(gender = gender_dict['gender'],
                                description = gender_dict['description'],
                                picture = gender_dict['picture'])
        new_gender.save()
        resp = gender_schema.dump(new_gender)
        return {'icon':'success', 'msg': 'Registro Exitoso' ,'record': resp}, 201
    @UserModel.token_required
    def put(current_user, self, id):
        if not current_user.admin : return abort(403)
        data = request.get_json()
        gender_dict = gender_schema.load(data)
        GenderModel.update(id, gender_dict['gender'], gender_dict['description'], gender_dict['picture'])
        modified_gender = GenderModel.get_by_id(id)
        resp = gender_schema.dump(modified_gender)
        return {'icon':'success', 'msg': 'Actualización Exitosa' ,'record': resp}, 201
    @UserModel.token_required
    def delete(current_user, self, id):
        if not current_user.admin : return abort(403)
        delete_record = GenderModel.get_by_id(id)
        delete_record.delete()
        return {'icon':'warning', 'msg': 'Eliminación Exitosa'}, 201

class MovieListResource(Resource):
    def get(self):
        movies = FilmModel.get_all()
        resp = movie_schema.dump(movies, many=True)
        return resp, 201

class MovieResource(Resource):
    @UserModel.token_required
    def get(current_user, self):
        myMovies = FilmModel.simple_filter(useradd=current_user.id)
        resp = movie_schema.dump(myMovies, many=True)
        return resp, 201
    @UserModel.token_required
    def post(current_user, self):
        data = request.get_json()
        movie_dict = movie_schema.load(data)
        new_movie = FilmModel(title = movie_dict['title'], rating = movie_dict['rating'],
                                year = movie_dict['year'], synopsis = movie_dict['synopsis'],
                                duration = movie_dict['duration'], picture = movie_dict['picture'],
                                preview = movie_dict['preview'], useradd = current_user.id)
        new_movie.save()
        for gender in data['gender']:
            search_gender = GenderModel.get_by_id(gender)
            new_movie.gender.append(search_gender)
            db.session.commit()
        resp = movie_schema.dump(new_movie)
        return {'icon':'success', 'msg': 'Registro Exitoso' ,'record': resp}, 201
    @UserModel.token_required
    def put(current_user, self, id):
        movie = FilmModel.get_by_id(id)
        if not movie.useradd == current_user.id : return abort(403)
        data = request.get_json()
        movie_dict = movie_schema.load(data)
        FilmModel.update(id, movie_dict['title'], movie_dict['rating'], movie_dict['year'],
            movie_dict['synopsis'], movie_dict['duration'], movie_dict['picture'], movie_dict['preview'])
        db.session.execute(f"DELETE FROM generos_en_peliculas WHERE film ={id}") # Delete old Genders
        modified_film = FilmModel.get_by_id(id)
        for gender in data['gender']: # Modify Genders
            search_gender = GenderModel.get_by_id(gender)
            modified_film.gender.append(search_gender)
            db.session.commit()
        resp = movie_schema.dump(modified_film)
        return {'icon':'success', 'msg': 'Actualización Exitosa' ,'record': resp}, 201
    @UserModel.token_required
    def delete(current_user, self, id):
        movie = FilmModel.get_by_id(id)
        if not movie.useradd == current_user.id : return abort(403)
        movie.delete()
        return {'icon':'warning', 'msg': 'Eliminación Exitosa'}, 201

api.add_resource(RatingListResource, '/api/v1.0/cinema/ratings')
api.add_resource(RatingResource, '/api/v1.0/cinema/rating', '/api/v1.0/cinema/rating/<int:id>')
api.add_resource(GenderListResource, '/api/v1.0/cinema/genders')
api.add_resource(GenderResource, '/api/v1.0/cinema/gender', '/api/v1.0/cinema/gender/<int:id>')
api.add_resource(MovieListResource, '/api/v1.0/cinema/movies')
api.add_resource(MovieResource, '/api/v1.0/cinema/movie', '/api/v1.0/cinema/movie/<int:id>')