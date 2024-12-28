from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
db = SQLAlchemy()
DB_NAME = 'database.sqlite3'

def create_database():
    db.create_all()
    print("Database created")


# Initializing flask application
def create_app():
    app = Flask(__name__)
    # For each flask application we have a secret key
    app.config["SECRET_KEY"]= 'hsddgshdfssssu'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html')

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    # retrieving the user data
    @login_manager.user_loader
    def load_user(id):
        return Customer.query.get(int(id))


    # Importing routes Bluprints before returning our app
    from website.routes import routes
    from website.admin import admin
    from website.auth import auth
    from website.models import Customer,Cart,Product,Order

    # Registering routes Blueprints using our application variable app
    app.register_blueprint(routes,url_prefix=('/')) # localhost:5000/cart,about-us etc
    app.register_blueprint(auth, url_prefix=('/')) # localhost:5000/auth/login,sign-up,change-password
    app.register_blueprint(admin, url_prefix=('/')) #

    # with app.app_context(): run this for once only
    #     create_database()


    return app
