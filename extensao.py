from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

bd = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'usuarios.login'