from marshmallow import Schema, fields, validate

class SignupSchema(Schema):
    email = fields.Email(required=True, validate=validate.Email())
    password = fields.Str(required=True, validate=validate.Length(min=6))
    full_name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    experience_level = fields.Str(required=True, validate=validate.OneOf(['beginner', 'intermediate', 'advanced', 'expert']))
    preferred_role = fields.Str(required=True, validate=validate.OneOf(['frontend', 'backend', 'fullstack', 'devops', 'data', 'mobile', 'other']))
    is_interviewer = fields.Bool(required=True)
    is_candidate = fields.Bool(required=True)

class LoginSchema(Schema):
    email = fields.Email(required=True, validate=validate.Email())
    password = fields.Str(required=True, validate=validate.Length(min=6))