from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
from OpenSSL import SSL
import ritdaily

app = Flask(__name__)
ask = Ask(app, "/")

DAILY = "  "
help = 'For events, ask, "Alexa, ask R.I.T. Daily to get events". For sports, ask, "Alexa, ask R.I.T. Daily to get sports scores".'
qlaunch = 'Would you like to know upcoming events or sports scores?'

@ask.launch
def launch():
    #DAILY = ritdaily.alexaGet()
    #briefing = render_template('briefing')
    #briefing = DAILY[0] + DAILY[1]
    return statement(help).simple_card('Open', help)
    #return question(qlaunch)

#@ask.intent("HelpIntent")
#def getHelp():
    #help = "ask me for events or sports scores"
    #help = 'For events, ask ,"Alexa, ask R.I.T. Daily to get events". For sports, ask ,"Alexa, ask R.I.T. Daily to get sports scores".'
#    return statement(help).simple_card('Help', help)

@ask.intent("EventsIntent")
def getEvents():
    DAILY = ritdaily.alexaGet()
    events = DAILY[0]
    return statement(events).simple_card('Events', events)

@ask.intent("SportsIntent")
def getSports():
    DAILY = ritdaily.alexaGet()
    sports = DAILY[1]
    return statement(sports).simple_card('Sports', sports)

if __name__ == '__main__':
#    context = SSL.Context(SSL.SSLv23_METHOD)
#    context.use_privatekey_file('privkey.pem')
#    context.use_certification_file('fullchain.pem')
#    context.load_cert_chian("ritdaily.crt", "private.key")
#    app.run(host="0.0.0.0", port=443, debug=True, ssl_context=context)
     app.run(debug=True) 
