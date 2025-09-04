import flask


import dotenv
import os

dotenv.load_dotenv()

def create_app():
    app = flask.Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint, url_prefix='/')

    from .api import api as api_blueprint

    app.register_blueprint(api_blueprint, url_prefix='/api')

    from .user import user as user_blueprint

    app.register_blueprint(user_blueprint, url_prefix='/user')


    return app


