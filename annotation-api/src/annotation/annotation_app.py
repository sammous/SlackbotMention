"""
Main Flask app for the sentiment annotation
Loads configuration and instantiate API
"""
from flask import Flask, request, make_response, render_template
from flask_restful import Api

from annotation.Resources.mention import Mention, Annotate, Information, Leaderboard
from annotation.Resources.slackbot import SlackbotSendMention, SlackbotButtonAction
#from form_parser import create_parsers
from slackclient import SlackClient

import os
CLIENT_ID = "***"
CLIENT_SECRET = "***"
token = '***'

app = Flask(__name__)
app.config.from_object('annotation.config.default')
# Override default config
# True allows missing env var
# Create Parsers used in Resources
#create_parsers(app.config)

api = Api(app)

api.add_resource(
    Mention, '/getMention', resource_class_kwargs={'config': app.config['DATABASE_DEFAULT']})
api.add_resource(
    Annotate, '/annotate', resource_class_kwargs={'config': app.config['DATABASE_DEFAULT']})
api.add_resource(
    Information, '/information', resource_class_kwargs={'config': app.config['DATABASE_DEFAULT']})
api.add_resource(
    Leaderboard, '/leaderboard', resource_class_kwargs={'config': app.config['DATABASE_DEFAULT']})

api.add_resource(
    SlackbotSendMention, '/slackbotsendmention', resource_class_kwargs={'config': app.config['DATABASE_DEFAULT']})

api.add_resource(
    SlackbotButtonAction, '/slackbotanswer', resource_class_kwargs={'config': app.config['DATABASE_DEFAULT']})



"""
Following code allows to install the app
"""

@app.route("/auth", methods=["GET"])
def pre_install():
    """This route renders the installation page with 'Add to Slack' button."""
    # Since we've set the client ID and scope on our Bot object, we can change
    # them more easily while we're developing our app.
    client_id = CLIENT_ID
    scope = 'commands, bot'
    # Our template is using the Jinja templating language to dynamically pass
    # our client id and scope
    return render_template("install.html", client_id=client_id, scope=scope)


@app.route("/thanks", methods=["GET", "POST"])
def thanks():
    """
    This route is called by Slack after the user installs our app. It will
    exchange the temporary authorization code Slack sends for an OAuth token
    which we'll save on the bot object to use later.
    To let the user know what's happened it will also render a thank you page.
    """
    # Let's grab that temporary authorization code Slack's sent us from
    # the request's parameters.
    code_arg = request.args.get('code')

    # The bot's auth method to handles exchanging the code for an OAuth token
    auth_response = SlackClient(token).api_call("oauth.access",
                            client_id=CLIENT_ID,
                            client_secret=CLIENT_SECRET,
                            code=code_arg
                                )

    return render_template("thanks.html")


if __name__ == '__main__':
    app.run()
