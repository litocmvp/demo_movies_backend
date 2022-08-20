from app.db import db
from . import api
from ..schemas import FilmSchema, GenderSchema, RatinSchema
from ...models import UserModel, FilmModel, GenderModel, GenderFilmModel, RatingModel
from ....common.error_handling import ObjectNotFound, ObjectForbidden
from flask import request
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
        if not current_user.admin :
            raise ObjectForbidden('El usuario no posee los permisos suficientes para este registro, contacte a soporte')
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
        if not current_user.admin :
            raise ObjectForbidden('El usuario no posee los permisos suficientes para esta modificación, contacte a soporte')
        data = request.get_json()
        rating_dict = rating_schema.load(data)
        RatingModel.update(id, rating_dict['rating'], rating_dict['description'], rating_dict['picture'])
        old_rating = RatingModel.get_by_id(id)
        resp = rating_schema.dump(old_rating)
        return {'icon':'success', 'msg': 'Actualización Exitosa' ,'record': resp}, 201
    @UserModel.token_required
    def delete(current_user, self, id):
        if not current_user.admin :
            raise ObjectForbidden('El usuario no posee los permisos suficientes para esta eliminación, contacte a soporte')
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
        if not current_user.admin :
            raise ObjectForbidden('El usuario no posee los permisos suficientes para este registro, contacte a soporte')
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
        if not current_user.admin :
            raise ObjectForbidden('El usuario no posee los permisos suficientes para esta modificación, contacte a soporte')
        data = request.get_json()
        gender_dict = gender_schema.load(data)
        GenderModel.update(id, gender_dict['gender'], gender_dict['description'], gender_dict['picture'])
        modified_gender = GenderModel.get_by_id(id)
        resp = gender_schema.dump(modified_gender)
        return {'icon':'success', 'msg': 'Actualización Exitosa' ,'record': resp}, 201
    @UserModel.token_required
    def delete(current_user, self, id):
        if not current_user.admin :
            raise ObjectForbidden('El usuario no posee los permisos suficientes para esta eliminación, contacte a soporte')
        delete_record = GenderModel.get_by_id(id)
        delete_record.delete()
        return {'icon':'warning', 'msg': 'Eliminación Exitosa'}, 201

class MovieListResource(Resource):
    def get(self):
        movies = FilmModel.get_all()
        resp = movie_schema.dump(movies, many=True)
        return resp, 201
    def post(self):
        data = request.get_json()
        movies = []
        key = list(data.items())[1][0]
        kwargs = {key: data[key]}
        prev = False
        next = False
        if not key in ['title','gender']: # key is year or rating
            movies = FilmModel.paginate_filter(data['page'], **kwargs)
            if len(movies.items) > 0:
                if movies.has_next: next = True
                if movies.has_prev: prev = True
                movies = movies.items
            else:
                raise ObjectNotFound('Recursos no encontrados')
        elif 'title' in key:
            movies = FilmModel.query.filter(FilmModel.title.like(f"%{data[key]}%")).paginate(page=data['page'], per_page=20, error_out=False)
            if len(movies.items) > 0:
                if movies.has_next: next = True
                if movies.has_prev: prev = True
                movies = movies.items
            else:
                raise ObjectNotFound('Recurso no encontrado')
        else:
            list_movies = db.session.query(GenderFilmModel).filter(GenderFilmModel.c.gender==data[key]).paginate(page=data['page'], per_page=20, error_out=False)
            if list_movies.has_next: next = True
            if list_movies.has_prev: prev = True
            for film in list_movies.items:
                movie = FilmModel.get_by_id(film.film)
                movies.append(movie)
            if len(movies) == 0:
                raise ObjectNotFound('Recursos no encontrados')
        resp = movie_schema.dump(movies, many=True)
        return {'movies':resp, 'preview': prev, 'next': next}, 201

class MovieResource(Resource):
    @UserModel.token_required
    def get(current_user, self):
        myMovies = FilmModel.simple_filter(useradd=current_user.id)
        if myMovies is None:
            raise ObjectNotFound('Recursos no encontrados')
        resp = movie_schema.dump(myMovies, many=True)
        resp2 = []
        if current_user.admin:
            moviesByOtherAuthors = FilmModel.query.filter(FilmModel.useradd != current_user.id).all()
            if not moviesByOtherAuthors is None:
                resp2 = movie_schema.dump(moviesByOtherAuthors, many=True)
        return {'myMovies': resp, 'otherMovies': resp2}, 201
    @UserModel.token_required
    def post(current_user, self):
        data = request.get_json()
        movie_dict = movie_schema.load(data)
        new_movie = FilmModel(title = movie_dict['title'], rating = movie_dict['rating'],
                                year = movie_dict['year'], synopsis = movie_dict['synopsis'],
                                duration = movie_dict['duration'], picture = movie_dict['picture'],
                                useradd = current_user.id)
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
        if not (movie.useradd == current_user.id or current_user.admin):
            raise ObjectForbidden('El usuario no posee los permisos suficientes para esta modificación, contacte a soporte')
        data = request.get_json()
        movie_dict = movie_schema.load(data)
        FilmModel.update(id, movie_dict['title'], movie_dict['rating'], movie_dict['year'],
            movie_dict['synopsis'], movie_dict['duration'], movie_dict['picture'])
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
        if not (movie.useradd == current_user.id or current_user.admin):
            raise ObjectForbidden('El usuario no posee los permisos suficientes para esta eliminación, contacte a soporte')
        movie.delete()
        db.session.execute(f"DELETE FROM generos_en_peliculas WHERE film ={id}") # Delete old movie
        db.session.commit()
        return {'icon':'warning', 'msg': 'Eliminación Exitosa'}, 201

api.add_resource(RatingListResource, '/api/v1.0/cinema/ratings')
api.add_resource(RatingResource, '/api/v1.0/cinema/rating', '/api/v1.0/cinema/rating/<int:id>')
api.add_resource(GenderListResource, '/api/v1.0/cinema/genders')
api.add_resource(GenderResource, '/api/v1.0/cinema/gender', '/api/v1.0/cinema/gender/<int:id>')
api.add_resource(MovieListResource, '/api/v1.0/cinema/movies')
api.add_resource(MovieResource, '/api/v1.0/cinema/movie', '/api/v1.0/cinema/movie/<int:id>')