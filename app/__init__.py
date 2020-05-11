from celery import Celery
from flask import Flask
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_mail_sendgrid import MailSendGrid
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from app import settings


db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
csrf_protect = CSRFProtect()
admin = Admin(name="Maranatha Namibia", template_mode="bootstrap3", url="/nimda_aram")
login_manager = LoginManager()
bcrypt = Bcrypt()
mail_send_grid = MailSendGrid()
celery = Celery(__name__, broker=settings.CELERY_BROKER)


def create_app():
    app = Flask(__name__)

    # Get setting from the setting file
    app.config.from_object('app.settings')

    # Set up the database
    db.init_app(app)

    # Set up flask migrate
    migrate.init_app(app, db)

    # Set up flask mail
    mail.init_app(app)

    # Enable CSRF protection for forms
    csrf_protect.init_app(app)

    bcrypt.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = '/user/login'

    mail_send_grid.init_app(app)

    admin.init_app(app)

    celery.conf.update(app.config)

    # Load the main Blueprint
    from app.main.views import main
    app.register_blueprint(main)

    from app.geography.views import geo
    app.register_blueprint(geo)

    # Load users blue print
    from app.users.views import users
    app.register_blueprint(users)

    from app.messages.views import messages
    app.register_blueprint(messages)

    from app.errors.handlers import errors
    app.register_blueprint(errors)

    add_admin_views()

    return app


def add_admin_views():
    from app.users.models import User, Role
    from app.users.views import UserUploadView, UserView
    admin.add_view(UserView(User, db.session, category='Users'))
    admin.add_view(ModelView(Role, db.session, category='Users'))

    admin.add_view(UserUploadView('Upload users', endpoint='Upload', category='Users'))
    admin.add_sub_category(name='User Management', parent_name='Users')

    from app.geography.models import Country, SubdivisionType, Subdivision, PopulatedAreaType, PopulatedArea
    admin.add_view(ModelView(Country, db.session, category='Geo'))
    admin.add_view(ModelView(SubdivisionType, db.session, category='Geo'))
    admin.add_view(ModelView(Subdivision, db.session, category='Geo'))
    admin.add_view(ModelView(PopulatedAreaType, db.session, category='Geo'))
    admin.add_view(ModelView(PopulatedArea, db.session, category='Geo'))

    admin.add_sub_category(name='Geo', parent_name='Geo')

