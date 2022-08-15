from flask import request, current_app
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import db, BaseModelMixin
import uuid
import jwt
from functools import wraps
from datetime import datetime, timedelta
from random import randint
from ..common.error_handling import ObjectNotFound, ObjectUnauthorized

class UserModel(db.Model, BaseModelMixin):
	""" Modelo para la tabla usuarios """

	__tablename__ = 'usuarios'

	id = db.Column(db.Integer, primary_key=True)
	public_id = db.Column(db.Integer, unique=True)
	user = db.Column(db.String(255), unique=True, nullable=False)
	password = db.Column(db.String, nullable=False)
	admin = db.Column(db.Boolean, default=False)

	film_relation = db.relationship('FilmModel', backref='usuarios', lazy=True,
									cascade="all, delete", passive_deletes=True)
	pwdreset_relation = db.relationship('ResetPwdModel',
										backref='cambios_pwd',
										lazy=True,
										cascade="all, delete",
										passive_deletes=True)

	def __repr__(self):
		return f"User ({self.user})"

	def __str__(self):
		return f"{self.user}"

	def set_password(self, password):
		self.password = generate_password_hash(password,  method='sha256')

	def check_password(self, password):
		return check_password_hash(self.password, password)

	def new_password(id , npass):
		pwd = generate_password_hash(npass)
		UserModel.query.filter_by(id=id).update(dict(password=pwd))
		db.session.commit()

	def save_user(self):
		if not self.id:
			self.public_id = str(uuid.uuid4())
			db.session.add(self)
			saved = False
			while not saved:
				try:
					db.session.commit()
					saved = True
				except IntegrityError:
					db.session.rollback()
					self.public_id = str(uuid.uuid4())

	def get(id):
		return UserModel.query.get(id)

	def token_required(f):
		@wraps(f)
		def decorator(*args, **kwargs):
			token = None

			if 'Authorization' in request.headers:
				token = request.headers['Authorization'][7:]

			if not token:
				raise ObjectNotFound('Token de autentificación no encontrado')

			try:
				data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
				current_user = UserModel.query.filter_by(public_id=data['public_id']).first()
			except:
				raise ObjectUnauthorized('Token de autentificación invalido, contacte a soporte')

			return f(current_user, *args, **kwargs)
		return decorator

class ResetPwdModel(db.Model):
	""" Modelo para la tabla restauracion de contraseñas de usuarios """

	__tablename__ = 'cambios_pwd'

	id = db.Column(db.Integer, primary_key=True)
	user = db.Column(db.Integer, db.ForeignKey('usuarios.id', ondelete='CASCADE'), nullable=False, unique=True)
	code = db.Column(db.Integer, nullable=False, unique=True)
	vigency = db.Column(db.DateTime, nullable=False, default=datetime.utcnow()+timedelta(minutes=30))

	def save(self):
		if not self.id:
			saved = False
			while not saved:
				codes = ""
				for x in range(9):
					codes +=str(randint(0,9))
				self.code = int(codes)
				try:
					db.session.add(self)
					db.session.commit()
					saved = True
				except IntegrityError:
					db.session.rollback()

	@staticmethod
	def delete(user):
		ResetPwdModel.query.filter_by(user=user).delete()
		db.session.commit()

GenderFilmModel = db.Table('generos_en_peliculas',
	db.Column('gender', db.Integer, db.ForeignKey('generos.id', ondelete='CASCADE'), nullable=False),
	db.Column('film', db.Integer, db.ForeignKey('peliculas.id', ondelete='CASCADE'), nullable=False)
)

class FilmModel(db.Model, BaseModelMixin):
	""" Modelo para la tabla de Peliculas """

	__tablename__ = 'peliculas'

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(90), nullable=False)
	rating = db.Column(db.Integer, db.ForeignKey('clasificaciones.id',
													ondelete='CASCADE'),
													nullable=False) # Fk solped)
	year = db.Column(db.Integer, nullable=False)
	synopsis = db.Column(db.String(255), nullable=False)
	duration = db.Column(db.String, nullable=True)
	picture = db.Column(db.String, nullable=False)
	useradd =  db.Column(db.Integer, db.ForeignKey('usuarios.id',
													ondelete='CASCADE'),
													nullable=False) # Fk solped)

	gender = db.relationship('GenderModel', secondary=GenderFilmModel, backref='films', lazy=True,
									cascade="all, delete", passive_deletes=True)

	def __init__(self, title, rating, year, synopsis, duration, picture, useradd):
		self.title = title
		self.rating = rating
		self.year = year
		self.synopsis = synopsis
		self.duration = duration
		self.picture = picture
		self.useradd = useradd

	def __repr__(self):
		return f"Film ({self.title})"

	def __str__(self):
		return f"{self.title}"

	def update(id, title, rating, year, synopsis, duration, picture):
		FilmModel.query.filter_by(id=id).update(dict(title=title, rating=rating, year=year,
			synopsis=synopsis, duration=duration, picture=picture))
		db.session.commit()

class GenderModel(db.Model, BaseModelMixin):
	""" Modelo para la tabla de Generos """

	__tablename__ = 'generos'

	id = db.Column(db.Integer, primary_key=True)
	gender = db.Column(db.String, nullable=False)
	description = db.Column(db.String, nullable=False)
	picture = db.Column(db.String, nullable=False)

	def __init__(self, gender, description, picture):
		self.gender = gender
		self.description = description
		self.picture = picture

	def __repr__(self):
		return f"Gender ({self.gender})"

	def __str__(self):
		return f"{self.gender}"

	def update(id, title, description, picture):
		GenderModel.query.filter_by(id=id).update(dict(gender=title, description=description, picture=picture))
		db.session.commit()

class RatingModel(db.Model, BaseModelMixin):
	""" Modelo para la tabla de Clasificaciones"""

	__tablename__ = 'clasificaciones'

	id = db.Column(db.Integer, primary_key=True)
	rating = db.Column(db.String, nullable=False)
	description = db.Column(db.String, nullable=False)
	picture = db.Column(db.String, nullable=False)

	film_relation = db.relationship('FilmModel', backref='clasificaciones', lazy=True,
									cascade="all, delete", passive_deletes=True)

	def __init__(self, rating, description, picture):
		self.rating = rating
		self.description = description
		self.picture = picture

	def __repr__(self):
		return f"Rating ({self.rating})"

	def __str__(self):
		return f"{self.rating}"

	def update(id, title, description, picture):
		RatingModel.query.filter_by(id=id).update(dict(rating=title, description=description, picture=picture))
		db.session.commit()
