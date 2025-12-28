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
from app.services.alma_service import AlmaService
from app.services.session_service import SessionService
from app.services.upload_service import UploadService
from app.utils.file_util import *
from flask import Blueprint, render_template, request, redirect

alma_service = AlmaService()
config = Settings()
session_service = SessionService()
upload_controller = Blueprint('upload_controller', __name__)


@upload_controller.get('/')
def upload():
    return render_template('upload.html')

@upload_controller.post('/result')
def result():
    marc_field_856 = None
    url_to_toc = None

    file = request.files['file']
    library_code = request.form.get('library')
    if not is_file_extension_allowed(file.filename):
        session_service.set_message('danger', f"Das ausgewählte Dateiformat ist ungültig (.{file.filename.split('.')[-1].lower()}).")
        return redirect('/')

    barcode = get_barcode_from_filename(file.filename)
    response = alma_service.get_item_by_barcode(barcode)

    if response is None:
        session_service.set_message('danger', f"Der Strichcode {barcode} wurde in Alma nicht gefunden.")
        return redirect('/')

    if not bool(response.get('item')):
        session_service.set_message('danger', f"Fehler: {response['web_service_result']['errorList']['error']['errorMessage']}")
        return redirect('/')

    mmsid_iz = response['item']['bib_data']['mms_id']
    response = alma_service.get_networkid_by_mmsid(mmsid_iz)

    if not response or not bool(response.get('bib')):
        session_service.set_message('danger', f"Die MMS ID {mmsid_iz} wurde in der Netzwerkzone nicht gefunden.")
        return redirect('/')

    network_id = response['bib']['linked_record_id']['#text']
    upload_service = UploadService(f"{barcode}.{get_file_extension(file.filename)}", library_code, network_id)
    upload_service.save_local_file(file)
    url_to_toc = upload_service.upload_pdf()

    if url_to_toc is False:
        session_service.set_message('danger', f"Die Datei ({network_id}.pdf) ist bereits online.")
        return redirect('/')

    elif url_to_toc == '':
        session_service.set_message('danger', f"Die Datei ({network_id}.pdf) konnte nicht hochgeladen werden.")
        return redirect('/')

    marc_field_856 = f"$$3 Inhaltsverzeichnis $$q PDF $$u {url_to_toc}"
    session_service.set_message('success', f"Die Datei ({network_id}.pdf) wurde erfolgreich hochgeladen.")
    return render_template('result.html', id=network_id, marc=marc_field_856, barcode=barcode, url=url_to_toc)