from image2text import image2text, ocrModelConfig


def add_text_ocr_result(page: dict, sub_image_path):
    sub_image_dir = sub_image_path + '/' + str(page['page']).zfill(4)
    reader = ocrModelConfig.model(custom_model=False)

    for obj in page['objects']:
        if obj['type'] != 'text':
            continue
        sub_image_no = obj['id']
        sub_image_path = sub_image_dir + '/' + str(sub_image_no).zfill(4) + '.png'
        content, credibility = image2text.read_text_area(reader, input_file=sub_image_path, spell_check=True)
        obj['content'] = content
        #obj['credibility'] = credibility
