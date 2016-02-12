import datetime
import random

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
    if (event['session']['application']['applicationId'] !=
             "arn:aws:lambda:us-east-1:058390151647:function:blackFriday"):
         raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    print event['request']['type']
    
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


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
    return today_is(None, session)


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'] +
          ", intent_name=" + intent_name)

    return today_is(intent, session)
            
def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Functions that control the skill's behavior ------------------


def today_is(intent, session):
    resp = {}
    resp['Monday'] = ["It's Monday.", "Today is Monday", "It's Monday, again?", "I'm sorry to say that it's Monday.", "It's the least favorite day of the week, Monday."]
    resp['Tuesday'] = ["It's Tuesday.", "Today is Tuesday", "It's only the day after Monday.", "Ugh, it's only Tuesday", "It's not quite Wednesday, but it's a little better than Monday."]
    resp['Wednesday'] = ["It's Wednesday.", "Today is Wednesday", "It's hump day, also known as Wednesday.", "It's the day of the week with the most letters."]
    resp['Thursday'] = ["It's Thursday.", "Today is Thursday", "Uhhh, it's only Thursday?", "Keep it going, it's already Thursday."]
    resp['Saturday'] = ["It's Saturday.", "Today is Saturday"]
    resp['Sunday'] = ["It's Sunday.", "Today is Sunday"]
    cardtext = ""

    day = datetime.datetime.now().strftime("%A")
    #print "DEBUG: Today is " + day + "."
    if day == 'Friday':
        speech_output = "<speak>Oh my. <audio src='https://s3-us-west-1.amazonaws.com/blackfriday-echossml/friday.mp3' /></speak>"
        cardtext = "It's Friday!"
    else:
        cardtext = random.choice(resp[day])
        speech_output = "<speak>" + cardtext + "</speak>"
    
    response = build_speechlet_response("Rebecca Black Says", speech_output, cardtext, "", True)
    return build_response({}, response)


# --------------- Helpers that build all of the responses ----------------------
def build_speechlet_response(title, output, cardtext, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': output
        },
        'card': {
            'type': 'Simple',
            'title': 'Ask Rebecca Black What Day It Is',
            'content': cardtext
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'SSML',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response }
