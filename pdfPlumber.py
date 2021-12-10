import pdfplumber
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
      box = table.bbox
      table
      #im.draw_rect(box, stroke='red', stroke_width=2)

    images_in_page = page.images
    ph = page.height
    for image in images_in_page:
      image
      box = (image['x0'], ph - image['y1'], image['x1'], ph - image['y0'])
      #im.draw_rect(box, stroke='blue', stroke_width=2)

    text_paragraphs = page.extract_words(y_tolerance = 8.7, keep_blank_chars= True, use_text_flow=True)
    for text_paragraph in text_paragraphs:
      box = (text_paragraph['x0'], text_paragraph['top'], text_paragraph['x1'], text_paragraph['bottom'])
      text = text_paragraph['text']
      print(box, text)
    #im.draw_rects(page.extract_words(y_tolerance = 8.7, keep_blank_chars= True, use_text_flow=True), stroke='green', stroke_width=2)
    #im.save(f'{k}.PNG')
    k +=1

path = "files/psycology.pdf"
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


