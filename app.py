#!/usr/bin/env python3

#   ###################
#   ##                 ##
#   ##               ##
#     ######       ##
#       ##       ######
#     ##               ##
#   ##                 ##
#     ###################


from app.config.settings import Settings
from app.config.template import register_template_functions
from app.controllers.upload_controller import upload_controller
from flask import Flask

config = Settings()


app = Flask(
        __name__,
        static_folder='resources/static',
        template_folder='resources/views'
    )

app.secret_key = config.FLASK_SECRET_KEY
app.register_blueprint(upload_controller)
register_template_functions(app)


if __name__ == '__main__':
    app.run(host=config.APP_HOST, port=config.APP_PORT, debug=config.APP_DEBUG)