import inspect

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.converter import HTMLConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.high_level import extract_pages
from io import StringIO


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams(line_margin=2)
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)
        text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text


# extracted_text = convert_pdf_to_txt(path)
# print(extracted_text)


path = "files/psycology.pdf"
laparams = LAParams(line_margin=2)


for page_layout in extract_pages(path, laparams=laparams):
    for element in page_layout:
        print(element)
        if element.__class__.__name__ == 'LTTextBoxHorizontal':
            bbox = element.bbox
            text = element.get_text()
        if element.__class__.__name__ == 'LTFigure':
            bbox = element.bbox
            image = element


"""
rsrcmgr = PDFResourceManager()
retstr = StringIO()
codec = 'utf-8'
laparams = LAParams()

f = open('./out.html', 'wb')
device = HTMLConverter(rsrcmgr, f, codec=codec, laparams=laparams)

fp = open(path, 'rb')
interpreter = PDFPageInterpreter(rsrcmgr, device)
password = ""
maxpages = 0  # is for all
caching = True
pagenos = set()
for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching,
                              check_extractable=True):
    interpreter.process_page(page)
fp.close()
device.close()
str = retstr.getvalue()
retstr.close()
f.close()
"""