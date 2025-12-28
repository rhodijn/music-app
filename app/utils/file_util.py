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

config = Settings()


def get_barcode_from_filename(filename:str) -> str:
    """
    Extract the leading barcode from a filename.
    The chain of splits isolates the first token before any '.' , '_' or '-',
    then normalises it to upper-case.
    """
    return filename.split('.')[0].split('_')[0].split('-')[0].upper()

def get_file_extension(filename:str) -> str:
    """
    Return the file extension in lower-case (everything after the last dot).
    """
    return filename.split('.')[-1].lower()

def is_file_extension_allowed(filename:str) -> bool:
    """
    Check whether the file's extension is listed in the allowed extensions.
    """
    return filename.split('.')[-1].lower() in config.ALLOWED_EXTENSIONS