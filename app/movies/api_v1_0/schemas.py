from marshmallow import fields, EXCLUDE

from app.ext import ma

class UserSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    public_id = fields.String(dump_only=True)
    user = fields.String()
    password = fields.String()
    admin = fields.Boolean()

class FilmSchema(ma.Schema):
    class Meta:
        unknown = EXCLUDE
    id = fields.Integer(dump_only=True)
    title = fields.String()
    rating = fields.Integer()
    gender = fields.Nested('GenderSchema', many=True, dump_only=True)
    year = fields.Integer()
    synopsis = fields.String()
    duration = fields.String()
    picture = fields.String()
    user = fields.Integer(dump_only=True)

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
