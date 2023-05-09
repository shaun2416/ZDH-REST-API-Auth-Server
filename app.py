import json
#import ssl

from auth import (authenticate_client,  generate_access_token, LIFE_SPAN)
from flask import Flask, request

app = Flask(__name__)

@app.route('/basicAuth', methods = ['POST']) 
def basicAuthRouteHandler():
  print(request.authorization["username"]) 
  print(request.authorization["password"])

  client_id = request.authorization["username"]
  client_secret = request.authorization["password"]
  scope = request.form.get('scope') if request.form.get('scope') else "*"

  if None in [client_id, client_secret]:
    return json.dumps({
      "error": "invalid_request"
    }), 400
  
  if not authenticate_client(client_id, client_secret):
    return json.dumps({
      "error": "invalid_client"
    }), 400

  access_token = generate_access_token(scope)
  
  return json.dumps({ 
    "access_token": access_token,
    "token_type": "JWT",
    "expires_in": LIFE_SPAN
  })

@app.route('/auth', methods = ['POST'])
def auth():
  # Issues access token
  client_id = request.form.get('client_id')
  client_secret = request.form.get('client_secret')

  if None in [client_id, client_secret]:
    return json.dumps({
      "error": "invalid_request"
    }), 400
  
  if not authenticate_client(client_id, client_secret):
    return json.dumps({
      "error": "invalid_client"
    }), 400

  scope = request.form.get('scope') if request.form.get('scope') else "*"
  access_token = generate_access_token(scope)
  return json.dumps({ 
    "access_token": access_token,
    "token_type": "JWT",
    "expires_in": LIFE_SPAN
  })


#if __name__ == '__main__':
  #context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
  #context.load_cert_chain('domain.crt', 'domain.key')
  #app.run(port = 5000, debug = True, ssl_context = context)
  #app.run(port = 5001, debug = True)