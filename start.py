import pdf_parser

path = "semple_files/psycology.pdf"
pdf_parser.parse_pdf(pdf_path=path, output_path='./result')

# pdf_path ='str'       -> 파싱할 pdf파일의 경로
# output_path = 'str'   -> 파싱된 결과물이 저장될 경로