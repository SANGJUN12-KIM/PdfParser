import json
import os
import shutil
import urllib.parse
from datetime import datetime
from shutil import copyfile
from zipfile import ZipFile

import requests as requests
from fastapi.logger import logger

from app.definitions import TEMP_DIR, CONVERTED_DIR
from numpyencoder import NumpyEncoder


#PUBPLE_HOST = "https://o2o-gwapi-devqa.altbooks.co.kr"
PUBPLE_HOST = "https://o2o-gwapi.altbooks.co.kr"

def get_token():
    headers = {'Content-Type': 'text/json',
               'Access-legacy-ext': 'OCR',
               'Access-legacy-security': 'r1OxaE18AJMfIBYfUhufzqZuxqKdlwXnkDeYr5ahze2GoFLbZwQT607LKE+yPRLx'
               }
    url = PUBPLE_HOST + "/v2/legacy/secure/token"
    response = requests.get(url, headers=headers)
    json_obj = response.json()
    secure_token = json_obj['result']['secureToken']

    return secure_token


def get_presigned_url(secure_token, task_id, file_name, file_size):
    headers = {'Content-Type': 'text/json',
               'Access-legacy-ext': 'OCR',
               'Authorization': 'Bearer ' + secure_token
               }
    file_name = urllib.parse.quote_plus(file_name)
    url = PUBPLE_HOST + f"/v2/legacy/secure/signbucket/OCR?taskId={task_id}&fileName={file_name}&fileSize={file_size}"
    response = requests.get(url, headers=headers)
    print(response)
    json_obj = response.json()
    file_id = json_obj['result']['fileId']
    presigned_url = json_obj['result']['presignedUrl']

    return file_id, presigned_url


def call_webhook(callback, file_id, final_path, presigned_url, secure_token, task_id):
    with open(final_path, 'rb') as f:
        data = f.read()
    headers = {'Content-Type': 'application/zip'}
    upload_response = requests.put(presigned_url, headers=headers, data=data)  # deal with this upload_response
    if upload_response.ok:
        logger.warning('---------- file uploaded at %s', datetime.now().strftime('%m/%d/%Y, %H:%M:%S'))
        print(upload_response)
    else:
        logger.warning('---------- file upload failed at %s', datetime.now().strftime('%m/%d/%Y, %H:%M:%S'))

    headers = {'Content-Type': 'application/json',
               'Access-legacy-ext': 'OCR',
               'Authorization': 'Bearer ' + secure_token
               }

    body = {'legacy': {
        'taskList': [{
            "brailleId": "BR-3020320302032",
            "taskId": task_id,
            "taskTp": "OCR",
            "taskState": "0001",
            "taskStateDtl": "OK",
            "fileId": file_id
        }]
    }}
    json_body = json.dumps(body)
    response = requests.put(callback, headers=headers, data=json_body)
    if upload_response.ok:
        logger.warning('---------- callback called successfully at %s', datetime.now().strftime('%m/%d/%Y, %H:%M:%S'))
    else:
        logger.warning('---------- callback failed at %s', datetime.now().strftime('%m/%d/%Y, %H:%M:%S'))
    return response


def make_result_zip(pdf_file_name):
    conv_working_path = str(TEMP_DIR) + "/" + os.path.splitext(pdf_file_name)[0]
    zip_path = str(CONVERTED_DIR) + "/" + os.path.splitext(pdf_file_name)[0] + ".zip"
    with ZipFile(zip_path, 'w') as result_zip:
        for root, dirs, files in os.walk(conv_working_path):
            if root.find('detect') != -1 or root.find('original') != -1:
                continue
            for folder_name in dirs:
                folder_arc = os.path.relpath(os.path.join(root, folder_name),
                                             os.path.join(conv_working_path, '.'))
                result_zip.write(os.path.join(root, folder_name), folder_arc)
            for file in files:
                file_arc = os.path.relpath(os.path.join(root, file),
                                           os.path.join(conv_working_path, '.'))
                result_zip.write(os.path.join(root, file), file_arc)

    return zip_path


def arrange_converted_folder(pdf_file_name):
    conv_working_path = str(TEMP_DIR) + "/" + os.path.splitext(pdf_file_name)[0]

    page_image_path = conv_working_path + "/images/pages"
    equation_image_path = conv_working_path + "/images/equation"
    figure_image_path = conv_working_path + "/images/figure"
    try:
        os.makedirs(equation_image_path)
        os.makedirs(figure_image_path)
    except OSError:
        pass

    page_info_path = conv_working_path + "/pages"
    for filename in os.listdir(page_info_path):
        if not filename.endswith('.json'):
            continue
        json_path = page_info_path + "/" + filename
        file = open(json_path)
        page = json.load(file)

        page_no = page['page']
        objects = page['objects']
        for obj in objects:
            src = page_image_path + '/' + str(page_no).zfill(4) + '/' + str(obj['id']).zfill(4) + '.png'
            if obj['type'] == 'image':
                dest = figure_image_path + '/' + str(page_no).zfill(4) + '_' + str(obj['id']).zfill(4) + '.png'
                url = '../images/figure/' + str(page_no).zfill(4) + '_' + str(obj['id']).zfill(4) + '.png'
            elif obj['type'] == 'math':
                dest = equation_image_path + '/' + str(page_no).zfill(4) + '_' + str(obj['id']).zfill(4) + '.png'
                url = '../images/equation/' + str(page_no).zfill(4) + '_' + str(obj['id']).zfill(4) + '.png'
            else:
                continue

            obj['url'] = url
            copyfile(src, dest)

        file.close()
        with open(json_path, 'w', encoding="utf-8") as outfile:
            json.dump(page, outfile, ensure_ascii=False, cls=NumpyEncoder, indent="\t")

    original_image_path = conv_working_path + "/images/original"
    pages_image_path = conv_working_path + "/images/pages"
    shutil.rmtree(original_image_path)
    shutil.rmtree(pages_image_path)
