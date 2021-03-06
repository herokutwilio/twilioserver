from flask import Flask, request
from twilio.util import TwilioCapability
import twilio.twiml

#ACCOUNT_SID = 'AC399ea9c308d1cc32573baac7336d0754' # Trial account
ACCOUNT_SID = 'ACe56a1fe769fa2daf2cd4940de8ec00e3' # Dev account
#AUTH_TOKEN = '3b4a61f0def634eeb241a188e44a3c87' # Trial account
AUTH_TOKEN = 'a8e80c63c1df7ca067ea727f3c6db7c8' # Dev account
#APP_SID = 'APabe7650f654fc34655fc81ae71caa3ff' # Default magic number
#APP_SID = 'AP16406d3d5e0e48e6d07553f7a72172dd' # Trial account
APP_SID = 'AP92f6044c0f27931385c00c5cdaedb799' # Dev account

#CALLER_ID = '+16509222315'
CALLER_ID = '+16506785534'
DEFAULT_NUMBER = '+16509222315'
CLIENT = 'jenny'

app = Flask(__name__)

@app.route('/token')
def token():
  capability = TwilioCapability(ACCOUNT_SID, AUTH_TOKEN)

  # This allows outgoing connections to application
  if request.values.get('allowOutgoing') != 'false':
     print 1
     capability.allow_client_outgoing(APP_SID)

  # This allows incoming connections to client (if specified)
  client = request.values.get('client')
  if client != None:
    print 2
    capability.allow_client_incoming(client)

  # This returns a token to use with Twilio based on the account and capabilities defined above
  result = capability.generate()
  print result
  return result

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
  resp.say('10 9 8 7 6 5 4 3 2 1 0 Big brother watching you!')
  if not from_client:
    # PSTN -> client
    print 1
    resp.dial(callerId=from_value).client(CLIENT)
  elif to.startswith("client:"):
    # client -> client
    print 2
    resp.dial(callerId=from_value).client(to[7:])
  else:
    # client -> PSTN
    print 3
#    resp.dial(to, callerId=CALLER_ID)
    resp.dial(number=DEFAULT_NUMBER, callerId=CALLER_ID)
  result = str(resp)
  print result
  return result

if __name__ == "__main__":
  app.run(debug=True)
