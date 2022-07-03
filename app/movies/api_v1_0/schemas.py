from marshmallow import fields

from app.ext import ma

class UserSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    public_id = fields.String(dump_only=True)
    user = fields.String()
    password = fields.String()
    admin = fields.Boolean()

class FilmSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String()
    clasif = fields.String()
    gender = fields.Nested('GenderSchema', many=True)
    year = fields.Integer()
    synopsis = fields.String()
    duration = fields.Time()
    user = fields.Integer()

class GenderSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    gender = fields.String()
    description = fields.String()
    picture = fields.String()

class RatinSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    rating = fields.String()
    description = fields.String()
    picture = fields.String()
