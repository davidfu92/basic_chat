from app.db import Repository
from app.db..mongo import MongoRepository
from app.db.schema import Schema
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import ChatGrant
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException


class Service(object):
  def __init__(self, user_id, repo_client=Repository(adapter=MongoRepository)):
    self.repo_client = repo_client
    self.user_id = user_id
    load_dotenv()
    twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    twilio_auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    twilio_api_key_sid = os.environ.get('TWILIO_API_KEY_SID')
    twilio_api_key_secret = os.environ.get('TWILIO_API_KEY_SECRET')


    self.twilio_client = Client(twilio_account_sid, twilio_auth_token)
    
    token = AccessToken(twilio_account_sid, twilio_api_key_sid,
                        twilio_api_key_secret, identity=username)

    if not user_id:
      raise Exception("user id not provided")

  def find_all_msg(self):
    msgs = self.repo_client.find_all({'user_id': self.user_id})
    return [self.dump(msg) for msg in msgs]

  def find_msg(self, msg_id):
    msg = self.repo_client.find({'user_id': self.user_id, 'msg_id': msg_id})
    return self.dump(msg)

  def find_latest_msg(self, time):
      msg = self.repo_client.find().sort({'time_received':-1}).limit(1)
      return self.dump(msg.data)

  def create_msg(self, msg):
    self.repo_client.create(self.prepare_msg(msg))
    return self.dump(msg.data)

  def update_msg(self, msg_id, msg):
    records_affected = self.repo_client.update({'user_id': self.user_id, 'msg_id': msg_id}, self.prepare_msg(msg))
    return records_affected > 0

  def delete_msg(self, msg_id):
    records_affected = self.repo_client.delete({'user_id': self.user_id, 'msg_id': msg_id})
    return records_affected > 0

  def dump(self, data):
    return Message(exclude=['_id']).dump(data).data

  def prepare_msg(self, msg):
    data = msg.data
    data['user_id'] = self.user_id
    return data


  def send_msg(self, source, dest, msg):
    message = self.client.messages.create(body=msg, from_=source, to=dest)
    return message.sid

 def receive_msg(self):
   messages = self.client.messages.list(limit=5)
   for msg in messages:
       data = Message(id=msg.sid, msg=msg.body, time_received=msg.date_updated)
       data = self.prepare_msg(data)
       self.create_msg(data)

