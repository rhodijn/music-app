#!/usr/bin/env python3

#   ###################
#   ##                 ##
#   ##               ##
#     ######       ##
#       ##       ######
#     ##               ##
#   ##                 ##
#     ###################


import datetime
from app.config.settings import Settings


class LogService:

    def __init__(self):
        self.config = Settings()

    def log(self, message_type:str, message:str) -> bool:
        """
        Append a timestamped log entry to the error log file.
        Returns True on success (implicit, since no explicit return is needed).
        """
        with open(f"{self.config.PATH_LOG}/error_log.txt", 'a') as file:
            file.write(f"{datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')}\t{message_type}\t{message}\n")