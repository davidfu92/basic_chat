from marshmallow import Schema, fields

class Message(Schema):
  msg_id = fields.Str(required=True)
  user_id = fields.Int(required=True)
  time_received = fields.DateTime(required=True)
  msg = fields.Str(allow_none=True)
  deleted = fields.Boolean(default=False)
  language = fields.Str()
  description = fields.Str()
  repo_url = fields.URL()

class User(Schema):
  user_id = fields.Email(required=True)
  full_name = fields.Str()
  email = fields.Email()
  last_login = fields.DateTime()
