from easyocr import easyocr
from image2table import img2table


def add_table_ocr_result(page: dict, sub_image_path):
    # sub_image_dir = sub_image_path + '/' + str(page['page']).zfill(4)
    # reader = easyocr.Reader(['ko', 'en'], gpu=True)
    # for obj in page['objects']:
    #     if obj['type'] != 'table':
    #         continue
    #     sub_image_no = obj['id']
    #     sub_image_path = sub_image_dir + '/' + str(sub_image_no).zfill(4) + '.png'
    #     content = img2table.convert(reader, img_file=sub_image_path)
    #     obj['content'] = content
    pass
