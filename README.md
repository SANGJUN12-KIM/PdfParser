# Pdf_Parser for NIA-solution_for_social_issue

***
<img width="1728" alt="image" src="https://user-images.githubusercontent.com/81279383/145682674-7c17e4fc-1d54-4f00-bf0d-1f4d25cfe3a6.png">

### pdf파일의 메타데이터중 표, 이미지, 텍스트 정보를 읽어와 문서객체 구분, json 파일을 생성합니다.  

## 설치
- python 개발환경은 3.9입니다.
```python
git clone https://github.com/SANGJUN12-KIM/PdfParser.git
```
```python
pip install -r requirements.txt
```
## 사용법

```python
import pdf_parser

path = "semple_files/psycology.pdf"
pdf_parser.parse_pdf(pdf_path=path, output_path='./result')

# pdf_path ='str'       -> 파싱할 pdf파일의 경로
# output_path = 'str'   -> 파싱된 결과물이 저장될 경로
 ```
