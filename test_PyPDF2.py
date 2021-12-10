import PyPDF2

pdf_obj = open("files/unityTextbook.pdf", 'rb')

fileReader = PyPDF2.PdfFileReader(pdf_obj)

# 문서의 정보를 읽어드린다
fileReader.documentInfo

# 전체 페이지수를 출력한다
print(fileReader.numPages)

# 첫 번째 페이지 정보를 가져온다
pageObj = fileReader.getPage(0)
print(pageObj)

# 페이지 정보의 텍스트를 가져온다
text = pageObj.extractText()
print(text)

