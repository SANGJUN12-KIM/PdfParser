import json
import os

from libs.predictor import predictor_image, new_predictor_image

from app.definitions import TEMP_DIR
from numpyencoder import NumpyEncoder


def make_toc(conv_working_path: str):
    toc_path = conv_working_path + "/toc"
    try:
        os.makedirs(toc_path)
    except OSError as err:
        pass
    toc_figure = {'type': 'image', 'objects': []}
    toc_math = {'type': 'math', 'objects': []}
    toc_table = {'type': 'table', 'objects': []}
    toc_text = {'type': 'text', 'objects': []}

    with open(toc_path + '/toc_image.json', 'w', encoding="utf-8") as outfile:
        json.dump(toc_figure, outfile, ensure_ascii=False, cls=NumpyEncoder, indent="\t")

    with open(toc_path + '/toc_math.json', 'w', encoding="utf-8") as outfile:
        json.dump(toc_math, outfile, ensure_ascii=False, cls=NumpyEncoder, indent="\t")

    with open(toc_path + '/toc_table.json', 'w', encoding="utf-8") as outfile:
        json.dump(toc_table, outfile, ensure_ascii=False, cls=NumpyEncoder, indent="\t")

    with open(toc_path + '/toc_text.json', 'w', encoding="utf-8") as outfile:
        json.dump(toc_text, outfile, ensure_ascii=False, cls=NumpyEncoder, indent="\t")


def detect_image(pdf_file_name: str):
    pdf_path = str(TEMP_DIR) + "/" + pdf_file_name
    conv_working_path = str(TEMP_DIR) + "/" + os.path.splitext(pdf_file_name)[0]
    new_predictor_image(pdf_path, pdf_file_name, conv_working_path)
    make_toc(conv_working_path)
