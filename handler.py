"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
from external_libraries import requests


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "You have started Crypto Ticker. " \
                    "Please ask me for a crypto currency price by saying, " \
                    "what is the price of bitcoin? Or, tell me the price" \
                    "of Ethereum."
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please ask me for the price of a crypto currency by saying, " \
                    "what is the price of bitcoin?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for using Crypto Ticker. " \
                    "Have a nice day!"
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def get_bitcoin_price(intent, session):
    card_title = "Bitcoin Price"
    response = requests.get('https://api.coinbase.com/v2/prices/BTC-USD/spot')
    price = response.json()['data']['amount']
    log_price(price, 'bitcoin')
    if price is None:
        speech_output = "The price of bitcoin could not be retrieved at this time. Sorry."
    else:
        dollars_and_cents = price.split('.')
        speech_output = "The current price of bitcoin is " + dollars_and_cents[0] + " dollars and " + dollars_and_cents[1] + " cents."
    return build_response({}, build_speechlet_response(card_title, speech_output, None, should_end_session=True))


def get_ether_price(intent, session):
    card_title = "Ether Price"
    response = requests.get('https://api.coinbase.com/v2/prices/ETH-USD/spot')
    price = response.json()['data']['amount']
    log_price(price, 'ether')
    if price is None:
        speech_output = "The price of ether could not be retrieved at this time. Sorry."
    else:
        dollars_and_cents = price.split('.')
        speech_output = "The current price of ether is " + dollars_and_cents[0] + " dollars and " + dollars_and_cents[1] + " cents."
    return build_response({}, build_speechlet_response(card_title, speech_output, None, should_end_session=True))


def get_litecoin_price(intent, session):
    card_title = "Litecoin Price"
    response = requests.get('https://api.coinbase.com/v2/prices/LTC-USD/spot')
    price = response.json()['data']['amount']
    log_price(price, 'litecoin')
    if price is None:
        speech_output = "The price of litecoin could not be retrieved at this time. Sorry."
    else:
        dollars_and_cents = price.split('.')
        speech_output = "The current price of litecoin is " + dollars_and_cents[0] + " dollars and " + dollars_and_cents[1] + " cents."
    return build_response({}, build_speechlet_response(card_title, speech_output, None, should_end_session=True))

def get_price(intent, seession):
    pass

def log_price(price, cointype):
    print("Price of " + cointype + ": " + price)


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "GetBitcoinPriceIntent":
        return get_bitcoin_price(intent, session)
    elif intent_name == "GetEtherPriceIntent":
        return get_ether_price(intent, session)
    elif intent_name == "GetLitecoinPriceIntent":
        return get_litecoin_price(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
