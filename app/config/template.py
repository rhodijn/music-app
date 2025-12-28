#!/usr/bin/env python3

#   ###################
#   ##                 ##
#   ##               ##
#     ######       ##
#       ##       ######
#     ##               ##
#   ##                 ##
#     ###################


from app.services.session_service import SessionService


def register_template_functions(app) -> None:
    app.jinja_env.globals.update(session_service=SessionService())