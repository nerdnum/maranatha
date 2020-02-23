from flask import Blueprint, render_template

main = Blueprint('main', __name__, template_folder='templates')


# @main.route('/')
@main.route('/home')
def home():
    return render_template('home.html')


@main.route('/values')
def values():
    return render_template('values.html')


@main.route('/scriptures')
def scriptures():
    return render_template('scriptures.html')
