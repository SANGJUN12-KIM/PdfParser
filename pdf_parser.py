import pdfplumber
import os
import json
import shutil
import tqdm
import cv2
import base64
from collections import OrderedDict
from numpyencoder import NumpyEncoder
import pandas as pd

from app.definitions import LIBS_DIR
from app.core.page import Page, Object


def to_matrix(l, n):
    return [l[i:i + n] for i in range(0, len(l), n)]


def parse_pdf(pdf, output_path):
    file_name = pdf.split('.', 1)
    if output_path == "":
        output_path = file_name[0]

    org_img_path = os.path.join(output_path, 'original')
    detect_img_path = os.path.join(output_path, 'detect')

    figure_img_path = os.path.join(output_path, 'images/figure')
    equation_img_path = os.path.join(output_path, 'images/equation')
    table_img_path = os.path.join(output_path, 'images/table')
    json_page_path = os.path.join(output_path, 'pages')

    try:
        if os.path.isdir(output_path):
            shutil.rmtree(output_path)

        os.makedirs(output_path)
        os.makedirs(org_img_path)
        os.makedirs(detect_img_path)
        os.makedirs(figure_img_path)
        os.makedirs(table_img_path)
        os.makedirs(equation_img_path)
        os.makedirs(json_page_path)
    except OSError:
        pass

    page_list = []
    pdf = pdfplumber.open(pdf, laparams={"line_margin": 2})
    pages = pdf.pages

    for i, page in tqdm.tqdm(enumerate(pages)):
        path = org_img_path + "/" + str(i + 1).zfill(4) + ".png"
        page_list.append(Page(path, i + 1))
        page.save(path, "PNG")
    print("PDF open is complete.")


    for page in tqdm.tqdm(page_list):
        im = cv2.imread(page.path)

        height, width, channels = im.shape
        page.set_size(width, height)

        #v = Visualizer(im[:, :, ::-1], MetadataCatalog.get(cfg.DATASETS.TRAIN[0]), scale=1.2)
        #out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
        #cv2.imwrite(detect_img_path + "/" + str(page.no) + '.png', out.get_image()[:, :, ::-1])

        table_no, figure_no = 1, 1
        tables_in_page = page.find_tables(
            table_settings={"vertical_strategy": "lines", "horizontal_strategy": "lines_strict",
                            "intersection_x_tolerance": 13})
        #테이블 탐색
        for table in tables_in_page:
            box = table.bbox
            table_content = table.extract()
            table_df = pd.DataFrame(table_content)
            table_html = table_df.to_html()

            x, y, w, h = box[0], box[1], box[2] - box[0], box[3] - box[1]
            cropped_img = im[y: y + h, x: x + w]
            table_obj = Object('table', table.bbox[0], table.bbox[1], table.bbox[2], table.bbox[3], f'../images/equation/{page.no:>04d}_{table_no:>04d}.png')

            try:
                table_result = table_html
                table_result_bytes = table_result.encode('utf8')
                table_result_base64 = base64.b64encode(table_result_bytes)
                table_result_base64_str = table_result_base64.decode('utf8')
                table_obj.set_content(table_result_base64_str)
            except:
                print(img_path)

            page.append_object(table_obj)
            table_no += 1

        #이미지 탐색
        images_in_page = page.images
        ph = page.height
        for image in images_in_page:
            box = (image['x0'], ph - image['y1'], image['x1'], ph - image['y0'])
            x, y, w, h = box[0], box[1], box[2] - box[0], box[3] - box[1]
            cropped_img = im[y: y + h, x: x + w]

            img_path = os.path.join(figure_img_path, f'{page.no:>04d}_{figure_no:>04d}.png')
            cv2.imwrite(img_path, cropped_img)
            page.append_object(Object('figure', box[0], box[1], box[2], box[3],
                                      f'../images/figure/{page.no:>04d}_{figure_no:>04d}.png'))
            figure_no += 1

        #텍스트 추출
        text_paragraphs = page.extract_words(y_tolerance=8.7, keep_blank_chars=True, use_text_flow=True)
        for text_paragraph in text_paragraphs:
            box = (text_paragraph['x0'], text_paragraph['top'], text_paragraph['x1'], text_paragraph['bottom'])
            text = text_paragraph['text']
            text_object = Object('text', box[0], box[1], box[2], box[3], "")
            try:
                # text_object.set_content(image2text.spell_checker(content.replace('\n', '')))
                text_object.set_content(text)
            except UnicodeDecodeError:
                print(text)
            page.append_object(text_object)

        page.save_json(os.path.join(json_page_path, f'{page.no:>04d}.json'))


path = "files/hwp2pdf.pdf"
parse_pdf(path, './')