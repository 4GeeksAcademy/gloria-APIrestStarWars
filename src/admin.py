import os
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import db, User, Character, Planets, Films, Favorites

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    # Agregar los modelos al panel de administración
    admin.add_view(ModelView(User, db.session))        # Tabla: usuario
    admin.add_view(ModelView(Character, db.session))   # Tabla: character
    admin.add_view(ModelView(Planets, db.session))     # Tabla: planets
    admin.add_view(ModelView(Films, db.session))       # Tabla: films
    admin.add_view(ModelView(Favorites, db.session))   # Tabla: favorites