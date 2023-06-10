from flask import Blueprint
from apps.cicd.restplus import api
from apps.cicd.settings import config
from apps.cicd.views.unittest import UnittestApp
from library.api.tFlask import tflask

def register_blueprints(app):
    blueprint = Blueprint('v1', __name__, url_prefix='/v1')
    api.init_app(blueprint)
    api.add_namespace(UnittestApp)
    app.register_blueprint(blueprint)


def create_app():
    app = tflask(config)
    register_blueprints(app)
    return app

if __name__ == '__main__':
    create_app().run(port=config.PORT)