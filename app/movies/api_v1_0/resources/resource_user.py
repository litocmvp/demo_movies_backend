import jwt, datetime
from . import api
from ..schemas import UserSchema
from ...models import UserModel, ResetPwdModel
from ....common.error_handling import ObjectNotFound
from ....common.mail import send_email
from flask import request, current_app
from flask_restful import Resource, abort

user_schema = UserSchema()

class UserListResource(Resource):
    def get(self):
        users = UserModel.get_all()
        return user_schema.dump(users, many=True)

class UserResource(Resource):
    @UserModel.token_required
    def get(self, id):
        user = UserModel.get_by_id(id)
        resp = user_schema.dump(user)
        return resp
    def post(self):
        data = request.get_json()
        # Reseteo de Password
        if 'reset_pwd' in data and data['reset_pwd']:
            # Generar Código
            if len(str(data['code'])) == 0:
                user_model = UserModel.query.filter_by(user= data['user']).first()
                if not user_model is None:
                    pre_code = ResetPwdModel.query.filter_by(user=user_model.id).first()
                    if not pre_code is None:
                        if datetime.datetime.utcnow() < pre_code.vigency:
                            msg='Ya se encuentra una prevía solicitud vigente, por favor revisé su correo.'
                            icon = 'info'
                            return {'msg': msg, 'icon': icon, 'auth': True}, 200
                        else:
                            ResetPwdModel.delete(user_model.id)
                            registro = ResetPwdModel(user=user_model.id)
                            registro.save()
                            emisor = current_app.config['DONT_REPLY_FROM_EMAIL']
                            asunto = f"Solicitud de cambio de contraseña en el sitio web ({current_app.config['URL_INITIAL']})"
                            cuerpo = f"Su código de verificación para modificar su contraseña de usuario es: <strong>{registro.code}</strong>, el cual tendrá validez de <strong>30 minutos</strong>, a partir de la emisión de este correo.<br><br>Si usted no solicitó este código, le pedimos por favor que ignore este correo.<br><br><br>Att. <strong>CMVP - Soporte Técnico</strong><br><br><br><p><small><strong>Nota:</strong> Este correo no recibe correos entrantes. Por favor no responda a este correo.</small></p>"
                            enviar_email = send_email(subject=asunto, sender=emisor, recipients=[user_model.user], text_body='', html_body=cuerpo)
                            if enviar_email:
                                msg='Solicitud exitosa, por favor revisé su correo.'
                                icon = 'info'
                                return {'msg': msg, 'icon': icon, 'auth': True}, 200
                    else:
                        registro = ResetPwdModel(user=user_model.id)
                        registro.save()
                        emisor = current_app.config['DONT_REPLY_FROM_EMAIL']
                        asunto = f"Solicitud de cambio de contraseña en el sitio web ({current_app.config['URL_INITIAL']})"
                        cuerpo = f"Su código de verificación para modificar su contraseña de usuario es: <strong>{registro.code}</strong>, el cual tendrá validez de <strong>30 minutos</strong>, a partir de la emisión de este correo.<br><br>Si usted no solicitó este código, le pedimos por favor que ignore este correo.<br><br><br>Att. <strong>CMVP - Soporte Técnico</strong><br><br><br><p><small><strong>Nota:</strong> Este correo no recibe correos entrantes. Por favor no responda a este correo.</small></p>"
                        enviar_email = send_email(subject=asunto, sender=emisor, recipients=[user_model.user], text_body='', html_body=cuerpo)
                        if enviar_email:
                            msg='Solicitud exitosa, por favor revisé su correo.'
                            icon = 'info'
                            return {'msg': msg, 'icon': icon, 'auth': True}, 200
                else:
                    return {'msg': 'Usuario no encontrado', 'icon': 'warning', 'auth': False}, 200
            # Verificar Código
            elif len(data['pwd']) == 0:
                user_model = UserModel.query.filter_by(user= data['user']).first()
                if not user_model is None:
                    code = ResetPwdModel.query.filter_by(user=user_model.id).first()
                    if not code is None:
                        print(data)
                        if code.code == data['code']:
                            return {'msg': 'Verificación de código exitosa', 'icon': 'success', 'auth': True}, 200
                        else:
                            return {'msg': 'Verificación de código erroneo', 'icon': 'error', 'auth': False}, 200
                    else:
                        return {'msg': 'Verificación de código erroneo', 'icon': 'error', 'auth': False}, 200
                else:
                    return {'msg': 'Usuario no encontrado', 'icon': 'error', 'auth': False}, 200
            # Cambio de Contraseña:
            elif len(str(data['code'])) != 0 and len(data['pwd']) > 5:
                user_model = UserModel.query.filter_by(user= data['user']).first()
                if not user_model is None:
                    code = ResetPwdModel.query.filter_by(user=user_model.id).first()
                    if not code is None:
                        if code.code == data['code']:
                            UserModel.new_password(user_model.id, data['pwd'])
                            ResetPwdModel.delete(user_model.id)
                            return {'msg': 'Actualización de datos exitosa', 'icon': 'success', 'auth': True}, 200
                        else:
                            return {'msg': 'Código de verificación erroneo', 'icon': 'error', 'auth': False}, 200
                    else:
                        return {'msg': 'Código de verificación erroneo', 'icon': 'error', 'auth': False}, 200
                else:
                    return {'msg': 'Usuario no encontrado', 'icon': 'error', 'auth': False}, 200
            else:
                return abort(403)


class Auth(Resource):
    def get(self):
        data = request.headers.get('Authorization').split(':')
        email = data[0][6:].lower()
        pwd = data[1]
        user_model = UserModel.query.filter_by(user=email).first()
        if not user_model is None and user_model.check_password(pwd):
            user = user_schema.dump(user_model)
            token = jwt.encode({'public_id': user['public_id'],
							'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},
							current_app.config["SECRET_KEY"], algorithm="HS256")
            return {'token': token}, 200
        else:
            raise ObjectNotFound('El usuario no existe o incorrecta contraseña')
    def post(self):
        data = request.get_json()
        user_dict = user_schema.load(data)
        preview_user = UserModel.query.first()
        user = UserModel(user = user_dict['user'],
                         admin = True if preview_user is None else False)
        user.set_password(user_dict['password'])
        user.save_user()
        resp = user_schema.dump(user)
        return resp, 201

api.add_resource(UserListResource, '/api/v1.0/users')
api.add_resource(UserResource, '/api/v1.0/user/', '/api/v1.0/user/<int:id>')
api.add_resource(Auth, '/api/v1.0/user/auth', endpoint='login')