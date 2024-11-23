from marshmallow import Schema, fields


class PredictionSchema(Schema):
    year_of_release = fields.Integer(required=True)
    critic_score = fields.Float(required=True)
    critic_count = fields.Integer(required=True)
    user_score = fields.Float(required=True)
    user_count = fields.Integer(required=True)
