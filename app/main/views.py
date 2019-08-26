from flask import Blueprint, render_template

main = Blueprint('main', __name__, template_folder='templates')


@main.route('/')
def home():
    return render_template('home.html', templates_folder='app/templates')
