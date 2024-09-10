#!/usr/bin/env python3
'''Force locale with URL parameter
'''

from flask import Flask, render_template, request, g
from flask_babel import Babel, _

app = Flask(__name__)

# Mock user database
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}

# Configure Babel
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'fr']

babel = Babel(app)


# Define locale selector
@babel.localeselector
def get_locale():
    user = g.get('user', None)
    if user and user['locale']:
        return user['locale']
    LOCALE = "app.config['BABEL_SUPPORTED_LOCALES']"
    return request.accept_languages.best_match(LOCALE)


# Function to get user based on login_as parameter
def get_user():
    login_as = request.args.get('login_as')
    if login_as:
        user_id = int(login_as)
        return users.get(user_id)
    return None


# before_request function to set user globally
@app.before_request
def before_request():
    g.user = get_user()


# Route for home page
@app.route('/')
def home():
    return render_template('5-index.html')


if __name__ == "__main__":
    app.run()
