#!/usr/bin/env python3

#   ###################
#   ##                 ##
#   ##               ##
#     ######       ##
#       ##       ######
#     ##               ##
#   ##                 ##
#     ###################


from flask import session


class SessionService:

    def has_message(self, key:str) -> bool:
        """
        Return True if the given key exists and has a truthy value.
        """
        return bool(session.get(key))

    def get_message(self, key:str) -> str|None:
        """
        Retrieve the stored message and clear it from the session.
        """
        if self.has_message(key):
            session_message = session[key]
            session[key] = None
            return session_message
        return None

    def set_message(self, key:str, value:str) -> None:
        """
        Store a message only if the slot is currently empty.
        """
        if not self.has_message(key):
            session[key] = value
        return None