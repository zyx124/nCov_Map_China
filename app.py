from flask import Flask, render_template, jsonify
from datetime import timedelta


def create_app(**config_overrides):
    app = Flask(__name__)

    from map.views import user_app
    app.register_blueprint(user_app)
    return app

