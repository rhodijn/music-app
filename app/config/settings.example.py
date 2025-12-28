#!/usr/bin/env python3

#   ###################
#   ##                 ##
#   ##               ##
#     ######       ##
#       ##       ######
#     ##               ##
#   ##                 ##
#     ###################


class Settings:

    ALLOWED_EXTENSIONS: set = {'pdf'}
    API_URL: str = 'https://api-eu.hosted.exlibrisgroup.com/almaws/v1/'
    API_KEY: str = ''

    API_PARAM_GET: str = '?view=full&expand=p_avail'
    API_PARAM_PUT: str = '?validate=true&override_warning=true&override_lock=false&stale_version_check=false&cataloger_level=50&check_match=false'

    APP_HOST: str = '127.0.0.1'
    APP_PORT: int = 5000
    APP_DEBUG: bool = True

    FLASK_SECRET_KEY: str = ''

    FTP_URL: str = ''
    FTP_USER: str = ''
    FTP_PASS: str = ''
    FTP_PORT: int = 22

    FTP_PARAM_LIB: dict = {}

    PATH_LOG: str = ''
    PATH_REMOTE: str = ''
    PATH_UPLOAD: str = ''