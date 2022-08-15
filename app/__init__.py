from flask import Flask, jsonify
from flask_restful import Api
from flask_cors import CORS
from app.common.error_handling import ObjectNotFound, AppErrorBaseClass, ObjectForbidden, ObjectUnauthorized
from app.common.mail import mail
from app.movies.api_v1_0 import api_v1_0_bp
from app.ext import ma, migrate
from app.db import db

cors = CORS()

def create_app(settings_module):

	app = Flask(__name__)

	# Carga los parámetros de configuración según el entorno
	app.config.from_object(settings_module)

	cors.init_app(app, resources={r"/api/*": {"origins": "*"}})

	# Inicializar las extensiones
	# from app.movies.models import UserModel, FilmModel, GenderModel, GenderFilmModel, RatingModel, ResetPwdModel
	db.init_app(app)
	ma.init_app(app)
	migrate.init_app(app, db)
	mail.init_app(app)

	# Captura todos los errores 404
	Api(app, catch_all_404s=True)

	# Deshabilita el modo estricto de acabado de una URL con /
	app.url_map.strict_slashes = False

	# Registra los blueprints
	app.register_blueprint(api_v1_0_bp)

	# Custom error handlers
	register_error_handlers(app)

	return app

def register_error_handlers(app):

	@app.errorhandler(Exception)
	def handle_exception_error(e):
		return jsonify({'msg': 'Internal server error'}), 500

	@app.errorhandler(405)
	def handle_405_error(e):
		return jsonify({'msg': 'Method not allowed'}), 405

	@app.errorhandler(403)
	def handle_403_error(e):
		return jsonify({'msg': 'Forbidden error'}), 403

	@app.errorhandler(404)
	def handle_404_error(e):
		return jsonify({'msg': 'Not Found error'}), 404

	@app.errorhandler(AppErrorBaseClass)
	def handle_app_base_error(e):
		return jsonify({'msg': str(e)}), 500

	@app.errorhandler(ObjectNotFound)
	def handle_object_not_found_error(e):
		return jsonify({'msg': str(e)}), 404

	@app.errorhandler(ObjectForbidden)
	def handle_object_forbidden(e):
		return jsonify({'msg': str(e)}), 403

	@app.errorhandler(ObjectUnauthorized)
	def handle_object_unauthorized(e):
		return jsonify({'msg': str(e)}), 401
