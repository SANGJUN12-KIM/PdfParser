from urllib.parse import urlparse

from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import JSONResponse

from app.apis.ocr_api.converter import *
from app.definitions import *
from app.ocr.image_detector import detect_image
from app.ocr.text import add_text_ocr_result
from app.statemodels.convert_request import ConvertRequest
from app.statemodels.status import Status

router = APIRouter()


# client_callback_router = APIRouter()


# noinspection PyCompatibility
@router.post("/ocr_api/v1/convert",
             response_model=Status)
async def convert(req: ConvertRequest, background_tasks: BackgroundTasks):
    # body = b''
    # async for chunk in request.stream():
    #     body += chunk

    status = Status()
    status.ok = True
    # status.respTime = datetime.now()
    contents = status.dict()
    response = JSONResponse(content=contents)
    background_tasks.add_task(convert_notification,
                              req.legacy.callback,
                              req.legacy.taskId,
                              req.legacy.pdfUrl,
                              req.legacy.referenceUrl
                              )

    return response


def convert_notification(callback: str,
                         task_id: str,
                         pdf_url: str,
                         reference_url: str
                         ):
    logger.warning(f'---------- {task_id} starts at %s', datetime.now().strftime('%m/%d/%Y, %H:%M:%S'))
    logger.warning('---------- pdf file download starts at %s', datetime.now().strftime('%m/%d/%Y, %H:%M:%S'))
    print(callback)

    print(pdf_url)
    pdf_resp = requests.get(pdf_url, allow_redirects=True)
    logger.warning('---------- pdf file download ends at %s', datetime.now().strftime('%m/%d/%Y, %H:%M:%S'))
    pdf_url_parsed = urlparse(pdf_url)
    pdf_file_name = pdf_url_parsed.path.rsplit('/', 1)[-1]
    pdf_path = str(TEMP_DIR) + "/" + pdf_file_name
    open(pdf_path, 'wb').write(pdf_resp.content)

    print(reference_url)
    reference_resp = requests.get(reference_url, allow_redirects=True)
    logger.warning('---------- reference file download ends at %s', datetime.now().strftime('%m/%d/%Y, %H:%M:%S'))
    reference_url_parsed = urlparse(reference_url)
    reference_file_name = reference_url_parsed.path.rsplit('/', 1)[-1]
    reference_path = str(TEMP_DIR) + "/" + reference_file_name
    open(reference_path, 'wb').write(reference_resp.content)

    # pdf_file_name = "pdf_test_5.pdf"

    logger.warning('---------- detectron starts at %s', datetime.now().strftime('%m/%d/%Y, %H:%M:%S'))
    detect_image(pdf_file_name)  # it will save detected sub images and info under tmp dir
    logger.warning('---------- detectron ends at %s', datetime.now().strftime('%m/%d/%Y, %H:%M:%S'))

    """
    logger.warning('---------- add_ocr_result starts at %s', datetime.now().strftime('%m/%d/%Y, %H:%M:%S'))
    add_ocr_result(pdf_file_name)
    logger.warning('---------- add_ocr_result ends at %s', datetime.now().strftime('%m/%d/%Y, %H:%M:%S'))

    arrange_converted_folder(pdf_file_name)
    """

    zip_filename = pdf_file_name.split('.')[0] + ".zip"
    zip_path = make_result_zip(pdf_file_name)
    zip_size = os.path.getsize(zip_path)

    secure_token = get_token()

    logger.warning(f"---------- get_presigned_url({task_id}), {datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}")
    file_id, presigned_url = get_presigned_url(secure_token, task_id, zip_filename, zip_size)
    response = call_webhook(callback, file_id, zip_path, presigned_url, secure_token, task_id)
    logger.warning(f"---------- ocr end - {presigned_url}), {datetime.now().strftime('%m/%d/%Y, %H:%M:%S')}")

    return JSONResponse(response.json())


def add_ocr_result(pdf_file_name):
    conv_working_path = str(TEMP_DIR) + "/" + os.path.splitext(pdf_file_name)[0]
    page_info_path = conv_working_path + "/pages"
    sub_image_path = conv_working_path + "/images/pages"
    for filename in os.listdir(page_info_path):
        if not filename.endswith('.json'):
            continue
        json_path = page_info_path + "/" + filename
        file = open(json_path)
        page = json.load(file)

        # add_math_ocr_result(page, sub_image_path)
        # add_table_ocr_result(page, sub_image_path)
        logger.warning('---------- add_text_ocr_result starts at %s', datetime.now().strftime('%m/%d/%Y, %H:%M:%S'))
        add_text_ocr_result(page, sub_image_path)
        logger.warning('---------- add_text_ocr_result ends at %s', datetime.now().strftime('%m/%d/%Y, %H:%M:%S'))
        file.close()

        with open(json_path, 'w', encoding="utf-8") as outfile:
            json.dump(page, outfile, ensure_ascii=False, cls=NumpyEncoder, indent="\t")
