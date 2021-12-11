import pdfplumber
import os
import json
from collections import OrderedDict
from numpyencoder import NumpyEncoder
import pandas as pd

from app.definitions import LIBS_DIR
from app.core.page import Page, Object
#brew install imagemagick / sudo apt-get install libmagickwand-dev


def get_text(page):
  text = page.extract_text()
  return text

def parse_pdf(pdf_dir):
  pdf = pdfplumber.open(pdf_dir, laparams = {"line_margin": 2})
  pages = pdf.pages
  k=1
  for page in pages:
    print(page)
    im = page.to_image()

    tables_in_page = page.find_tables( table_settings = {"vertical_strategy": "lines", "horizontal_strategy": "lines_strict", "intersection_x_tolerance": 13})
    for table in tables_in_page:
      table_area = table.bbox
      table_content = table.extract()
      table_df = pd.DataFrame(table_content)
      table_html = table_df.to_html()
      print(table_html)
      #table_obj = Object('table', table.bbox[0], table.bbox[1], table.bbox[2], table.bbox[3], ]
      print('table', table_area, table_html)
      im.draw_rect(box, stroke='red', stroke_width=2)

    images_in_page = page.images
    ph = page.height
    for image in images_in_page:
      box = (image['x0'], ph - image['y1'], image['x1'], ph - image['y0'])
      print('image', box, image)
      im.draw_rect(box, stroke='blue', stroke_width=2)

    text_paragraphs = page.extract_words(y_tolerance = 8.7, keep_blank_chars= True, use_text_flow=True)
    for text_paragraph in text_paragraphs:
      box = (text_paragraph['x0'], text_paragraph['top'], text_paragraph['x1'], text_paragraph['bottom'])
      text = text_paragraph['text']
      print('text', box, text)
      im.draw_rects(page.extract_words(y_tolerance = 8.7, keep_blank_chars= True, use_text_flow=True), stroke='green', stroke_width=2)
      im.save(f'{k}.PNG')
    k +=1

def output(extracted_data, pages_num, image_name, width, height, output_path):
    file_name = os.path.splitext(image_name)[0]
    file_data = OrderedDict()
    file_data['page'] = pages_num
    file_data['width'] = width
    file_data['height'] = height
    item_list = []

    if output_path != None:
      for id, (area, text, credibility) in enumerate(extracted_data):
        item = {}
        item['id'] = id + 1
        item['order'] = id + 1
        item['type'] = 'text'

        area_2points = area[0], area[2]
        item['area'] = area_2points

        text = text
        item['content'] = text

        item['credibility'] = credibility
        item['url'] = ''
        item_list.append(item)

      file_data['object'] = item_list

      root_dir = output_path
      if os.path.isdir(root_dir) == False:
        os.mkdir(root_dir)
      os.chdir(root_dir)
      with open(file_name + '.json', 'w', encoding="utf-8") as make_file:
        json.dump(file_data, make_file, ensure_ascii=False, cls=NumpyEncoder, indent="\t")
      os.chdir(os.path.join(os.pardir))

path = "files/hwp2pdf.pdf"
parse_pdf(path)

# pdf_obj = pdfplumber.open(path)
# page = pdf_obj.pages[page_no]
# images_in_page = page.images
# page_height = page.height
# image_bbox = (image['x0'], page_height - image['y1'], image['x1'], page_height - image['y0'])
# cropped_page = page.crop(image_bbox)
# image_obj = cropped_page.to_image(resolution=400)
# image_obj.save(path_to_save_image)

# with pdfplumber.open(path, laparams = {"line_margin": 2}) as temp:
#   first_page = temp.pages[0]
#   img = temp.to_image()
#   img.draw_rects(temp.extract_words())
#   print(first_page.extract_text())


