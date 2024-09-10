#!usr/bin/env python3

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


def get_user():
    """Retrieve user from mock database based on login_as parameter."""
    login_as = request.args.get('login_as')
    if login_as:
        try:
            user_id = int(login_as)
            return users.get(user_id)
        except ValueError:
            return None
    return None


@app.before_request
def before_request():
    """Set the current user globally before each request."""
    g.user = get_user()


@babel.localeselector
def get_locale():
    """
    Select the best locale for the user.

    Priority:
    1. Locale from URL parameters
    2. Locale from user settings
    3. Locale from request headers
    4. Default locale
    """
    # 1. Check if locale is provided in URL parameters
    locale_param = request.args.get('locale')
    if locale_param and locale_param in app.config['BABEL_SUPPORTED_LOCALES']:
        return locale_param

    # 2. Check if user is logged in and has a preferred locale
    user = g.get('user', None)
    if user and user['locale'] in app.config['BABEL_SUPPORTED_LOCALES']:
        return user['locale']

    # 3. Use request headers (Accept-Language)
    LOCALE = app.config['BABEL_SUPPORTED_LOCALES']
    return request.accept_languages.best_match(LOCALE)


@app.route('/')
def home():
    """Render the home page."""
    return render_template('6-index.html')


if __name__ == "__main__":
    app.run()
