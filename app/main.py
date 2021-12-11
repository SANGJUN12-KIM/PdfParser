import sys
import traceback
from datetime import datetime

import requests as requests
import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.logger import logger
from fastapi.responses import JSONResponse

# Configuration File
import app.core.config as cfg
from app.routes import api

import logging
from fastapi.logger import logger as fastapi_logger

from app.ocr.image_detector import detect_image
from app.apis.ocr_api.converter import *
from app.ocr.math import add_math_ocr_result
from app.ocr.table import add_table_ocr_result
from app.ocr.text import add_text_ocr_result
from app.routes.api import add_ocr_result

app = FastAPI()
app.include_router(api.router)


@app.get("/")
async def read_main():
    return {"msg": "ocr_api"}


@app.get("/initiate")
async def initiate_process():
    headers = {'Content-Type': 'text/json',
               'Access-legacy-ext': 'OCR',
               }
    url = "https://o2o-gwapi-devqa.altbooks.co.kr/v2/legacy/braille/link?endpoint=http://203.232.210.26:3000/ocr_api/v1/convert"
    # url = "https://o2o-gwapi-devqa.altbooks.co.kr/v2/legacy/braille/link?endpoint=http://175.200.66.141:3000/ocr_api/v1/convert"

    logger.warning('---------- Ask pubple server to call our convert endpoint at %s',
                   datetime.now().strftime('%m/%d/%Y, %H:%M:%S'))
    response = requests.get(url, headers=headers)
    logger.warning('---------- pubple server responded at %s', datetime.now().strftime('%m/%d/%Y, %H:%M:%S'))
    return JSONResponse(response.json())

@app.get("/test")
async def do_test():
    pdf_file_name = "CT-20211001000100001_source_1633051500733.pdf"
    detect_image(pdf_file_name)  # it will save detected sub images and info under tmp dir
    zip_filename = pdf_file_name.split('.')[0] + ".zip"
    zip_path = make_result_zip(pdf_file_name)

if __name__ == '__main__':
    print(f'Starting API Server: {cfg.api["host"]}:{cfg.api["port"]}\n')

    try:
        uvicorn.run(
            "app.main:app",
            host=cfg.api["host"],
            port=cfg.api["port"],
            workers=cfg.api["workers"],
            log_level=cfg.api["log_level"],
            reload=cfg.api["reload"],
            debug=cfg.api["debug"]
        )
    except KeyboardInterrupt:
        print(f'\nExiting\n')
    except Exception as e:
        print(f'Failed to Start API')
        print('=' * 100)
        traceback.print_exc(file=sys.stdout)
        print('=' * 100)
        print('Exiting\n')
    print(f'\n\n')
