#!/usr/bin/env python3

#   ###################
#   ##                 ##
#   ##               ##
#     ######       ##
#       ##       ######
#     ##               ##
#   ##                 ##
#     ###################


import os, paramiko
from app.services.log_service import LogService
from app.config.settings import Settings
from typing import BinaryIO


class UploadService:

    def __init__(self, filename:str, library_code:str, network_id:int):
        self.__filename = filename
        self.__library_code = library_code
        self.__network_id = network_id
        self.config = Settings()
        self.log_service = LogService()

    def save_local_file(self, file:BinaryIO):
        file.save(f"{self.config.PATH_UPLOAD}/{self.__filename}")

    def open_connection(self):
        self.__ssh_client = paramiko.SSHClient()
        self.__ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.__ssh_client.connect(
            hostname=self.config.FTP_URL,
            port=self.config.FTP_PORT,
            username=self.config.FTP_USER,
            password=self.config.FTP_PASS,
            look_for_keys=False
        )
        self.__sftp_client = self.__ssh_client.open_sftp()

    def verify_remote_files(self) -> bool:
        """
        Return True if the target PDF is NOT already present on the remote side.
        """
        remote_files = self.__sftp_client.listdir(f"{self.config.PATH_REMOTE}/{self.config.FTP_PARAM_LIB[self.__library_code]}")
        return f"{self.__network_id}.pdf" not in remote_files

    def close_connection(self):
        self.__sftp_client.close()
        self.__ssh_client.close()

    def upload_pdf(self) -> str|bool:
        """
        Upload the local PDF to the remote library folder.
        Returns:
            - URL string on success,
            - False if the file already existed remotely,
            - empty string on error.
        """
        url = None
        self.open_connection()

        if self.verify_remote_files():
            try:
                self.__sftp_client.put(f"{self.config.PATH_UPLOAD}/{self.__filename}", f"{self.config.PATH_REMOTE}/{self.config.FTP_PARAM_LIB[self.__library_code]}/{self.__network_id}.pdf")
                url = f"https://{self.config.FTP_URL}/{self.config.PATH_REMOTE}/{self.config.FTP_PARAM_LIB[self.__library_code]}/{self.__network_id}.pdf"
            except Exception as e:
                self.log_service.log('error', f"Fehler: {e}")
                url = ''
        else:
            self.log_service.log('info', f"pdf already online ({self.__network_id})")
            url = False

        self.close_connection()

        if os.path.exists(f"{self.config.PATH_UPLOAD}/{self.__filename}"):
            try:
                os.remove(f"{self.config.PATH_UPLOAD}/{self.__filename}")
            except Exception as e:
                self.log_service.log('warning', f"Fehler: {e}")
        return url