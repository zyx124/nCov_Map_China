from flask import Blueprint, render_template, request, url_for, redirect, session, abort


user_app = Blueprint('user_app', __name__)


@user_app.route('/', methods=['GET'])
def main_page():

    return render_template('map/index.html')
