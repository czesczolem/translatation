from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config
from flaskblog.language_apps.translator import Translator
from flaskblog.language_apps.brain import Brain
from flaskblog.language_apps.quiz import Quiz
from flaskblog.language_apps.DataLoader import DataLoader



db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    app.translator = Translator()
    app.dataloader = DataLoader(app.config['X_MYSQL_HOST'], app.config['X_MYSQL_USER'], app.config['X_MYSQL_PASS'], 'transly')
    app.dataloader.get_data("SELECT p1, p2, p3 FROM starke_verbe;")
    app.quiz = Quiz(app.dataloader)
    # app.brain = Brain()

    from flaskblog.users.routes import users
    from flaskblog.language_apps.routes import language_apps
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(language_apps)

    return app
