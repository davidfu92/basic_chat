from flask_oidc import OpenIDConnect
from flask import Flask, json, g, request
from app.service import Service
from app.db.schema import Message
from flask_cors import CORS

app = Flask(__name__)
oidc = OpenIDConnect(app)
CORS(app)

@app.route("/msgs", methods=["GET"])
def index():
  return json_response(Service(g.oidc_token_info['sub']).find_all_msgs())


@app.route("/msgs", methods=["POST"])
def create():
  input_msg = Message().load(json.loads(request.data))
  
  if input_msg.errors:
    return json_response({'error': input_msg.errors}, 422)

  msg = Service(g.oidc_token_info['sub']).create_msg(input_msg)
  return json_response(msg)


@app.route("/msg/<int:msg_id>", methods=["GET"])
def show(msg_id):
  msg = Service(g.oidc_token_info['sub']).find_msg(msg_id)

  if msg:
    return json_response(msg)
  else:
    return json_response({'error': 'msg not found'}, 404)


@app.route("/msg/<int:msg_id>", methods=["PUT"])
@oidc.accept_token(True)
def update(msg_id):
   msg_input = Message().load(json.loads(request.data))
  
   if msg_input.errors:
     return json_response({'error': msg_input.errors}, 422)

   msg_service = Service(g.oidc_token_info['sub'])
   if msg_service.update_msg(msg_id, msg_input):
     return json_response(msg_input.data)
   else:
     return json_response({'error': 'msg not found'}, 404)


@app.route("/msg/<int:msg_id>", methods=["DELETE"])
def delete(msg_id):
  msg_service = Service(g.oidc_token_info['sub'])
  if msg_service.delete_msg(msg_id):
    return json_response({})
  else:
    return json_response({'error': 'msg not found'}, 404)


def json_response(payload, status=200):
  return (json.dumps(payload), status, {'content-type': 'application/json'})
