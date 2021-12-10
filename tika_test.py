from tika import parser

path = "files/fulltext.pdf"

raw_pdf = parser.from_file(path)
contents = raw_pdf['content']
#contents = contents.strip()
print(contents)

data = raw_pdf
print(data)

print(raw_pdf['metadata'])

# <class 'dict'>
print(type(raw_pdf['metadata']))
