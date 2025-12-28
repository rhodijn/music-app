#!/usr/bin/env python3

#   ###################
#   ##                 ##
#   ##               ##
#     ######       ##
#       ##       ######
#     ##               ##
#   ##                 ##
#     ###################


import requests, xmltodict
from app.config.settings import Settings
from app.services.log_service import LogService


class AlmaService:

    def __init__(self):
        self.config = Settings()
        self.log_service = LogService()

    def get_item_by_barcode(self, barcode:str) -> dict|None:
        """
        Retrieve an item record from Alma using its barcode.
        Returns a dict parsed from the XML response, or None on error.
        """
        try:
            request = f"{self.config.API_URL}/items?item_barcode={barcode}&apikey={self.config.API_KEY}"
            response = requests.get(request)
            return xmltodict.parse(response.content)
        except Exception as e:
            self.log_service.log('error', f"Fehler: {e}")
            return None
        
    def get_networkid_by_mmsid(self, mmsid:int) -> dict|None:
        """
        Retrieve a bibliographic record (network ID) from Alma by its MMS ID.
        Returns a dict parsed from the XML response, or None on error.
        """
        try:
            request = f"{self.config.API_URL}/bibs/{mmsid}{self.config.API_PARAM_GET}&apikey={self.config.API_KEY}"
            response = requests.get(request)
            return xmltodict.parse(response.content)
        except Exception as e:
            self.log_service.log('error', f"Fehler: {e}")
            return None