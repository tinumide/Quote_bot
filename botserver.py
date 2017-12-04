from flask import Flask, request
import json
import requests
from Quotes_Api import get_quotes
import sys
import os



try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai

app = Flask(__name__)

PAT = 'EAAHjrJmTizABAHmTvWSvHLRujOwgxcHupZBmP38MuF8ZBVGBdZCAS5Pk7cB9idS0pDhJmyVV8v9whwJoBkY9cCY4OBoQFc6zRupZAZA6G6wWJ7fnpQJVJXIWlHM3AZCBYXwdLIvTh3Ct14jHyWLwc7Ecv0BxBKJEW0sodBugbNYChYTP7zJlxy'

CLIENT_ACCESS_TOKEN = '4e35359adfa1433e971e6daca16682cb' 

#VERIFY_TOKEN = 'tinuade'

@app.route('/webhook', methods=['GET'])
def handle_verification():
  print("Handling Verification.")
  if request.args.get('hub.verify_token', '') == 'I_am_Alexandrer':
    print("Verification successful!")
    return request.args.get('hub.challenge', '')
  else:
    print("Verification failed!")
    return 'Error, wrong validation token'

@app.route('/webhook', methods=['POST'])
def handle_messages():
  print("Handling Messages")
  payload = request.get_data()
  print(payload)
  for sender, message in messaging_events(payload):
    print("Incoming from %s: %s" % (sender, message))
    # send message api ai
    bot_response = parse_user_message(message)
    # send response from api ai to facebook
    send_message(PAT, sender, bot_response)
  return "ok"

def messaging_events(payload):
  """Generate tuples of (sender_id, message_text) from the
  provided payload.
  """
  data = json.loads(payload)
  messaging_events = data["entry"][0]["messaging"]
  for event in messaging_events:
    if "message" in event and "text" in event["message"]:
      yield event["sender"]["id"], event["message"]["text"].encode('unicode_escape')
    else:
      yield event["sender"]["id"], "I can't echo this"


def send_message(token, recipient, text):
  """Send the message text to recipient with id recipient.
  """

  r = requests.post("https://graph.facebook.com/v2.6/me/messages",
    params={"access_token": token},
    data=json.dumps({
      "recipient": {"id": recipient},
      "message": {"text": text}
    }),
    headers={'Content-type': 'application/json'})
  if r.status_code != requests.codes.ok:
    print(r.text)
    

def parse_user_message(user_text):
    '''
    Send the message to API AI which invokes an intent
    and sends the response accordingly
    The bot response is appened with quotes data fetched from
    the Quotes_api
    '''
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    r = ai.text_request()
    r.query = user_text.decode('utf-8')
    # r.getresponse()

    response = json.loads(r.getresponse().read().decode('utf-8'))
    responseStatus = response['status']['code']

    if (responseStatus == 200):
        print("API AI response", response['result']['fulfillment']['speech'])
        api_response = response['result']
        quotes = None
       # attractions = None
        # print(response['result'])
        
        try:
            if api_response['metadata']['intentName'] == 'quotes':
                quotes = get_quotes()

        except KeyError:
            pass

        response = api_response['fulfillment']['speech']
        if quotes:
            response += ':\n\n' + quotes

    return response

    '''def send_message_response(sender_id, message_text):

    sentenceDelimiter = ". "
    messages = message_text.split(sentenceDelimiter)'''
    
    # for message in messages:
    #     send_message(sender_id, message)


if __name__ == '__main__':
  app.run()

