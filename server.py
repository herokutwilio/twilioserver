from flask import Flask, request
from twilio.util import TwilioCapability
import twilio.twiml

ACCOUNT_SID = 'AC399ea9c308d1cc32573baac7336d0754'
AUTH_TOKEN = '3b4a61f0def634eeb241a188e44a3c87'
#APP_SID = 'APabe7650f654fc34655fc81ae71caa3ff'
APP_SID = 'APabe7650f654fc34655fc81ae71caa3ff'
CALLER_ID = '+12345678901'
CLIENT = 'jenny'

app = Flask(__name__)

@app.route('/token')
def token():
  capability = TwilioCapability(ACCOUNT_SID, AUTH_TOKEN)

  # This allows outgoing connections to application
  if request.values.get('allowOutgoing') != 'false':
     capability.allow_client_outgoing(APP_SID)

  # This allows incoming connections to client (if specified)
  client = request.values.get('client')
  if client != None:
    capability.allow_client_incoming(client)

  # This returns a token to use with Twilio based on the account and capabilities defined above
  return capability.generate()

@app.route('/call', methods=['GET', 'POST'])
def call():
  """ This method routes calls from/to client                  """
  """ Rules: 1. From can be either client:name or PSTN number  """
  """        2. To value specifies target. When call is coming """
  """           from PSTN, To value is ignored and call is     """
  """           routed to client                               """
  resp = twilio.twiml.Response()
  from_client = request.values.get('From').startswith('client')
  from_value = request.values.get('From')
  to = request.values.get('To')
  if not from_client:
    # PSTN -> client
    resp.dial(callerId=from_value).client(CLIENT)
  elif to.startswith("client:"):
    # client -> client
    resp.dial(callerId=from_value).client(to[7:])
  else:
    # client -> PSTN
    resp.dial(to, callerId=CALLER_ID)
  return str(resp)

if __name__ == "__main__":
  app.run(debug=True)