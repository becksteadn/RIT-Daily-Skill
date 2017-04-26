from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import ritdaily

app = Flask(__name__)
ask = Ask(app, "/")

DAILY = "  "


@ask.launch
def getBrief():
    DAILY = ritdaily.alexaGet()
    briefing = render_template('briefing')


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
    app.run(host="0.0.0.0", port=443, debug=True)
