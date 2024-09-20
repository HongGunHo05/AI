import requests
from bs4 import BeautifulSoup
import re

class NewsContent: 

    def news_crawling(url):

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        response = requests.get(url, headers=headers)
        crawling = BeautifulSoup(response.text, 'html.parser')

        # 기사 제목 추출
        title_element = crawling.find('h2', class_='media_end_head_headline')
        title = title_element.text.strip() if title_element else "제목 없음"

        # "[오은영의 부모마음 아이마음]" 부분 제거
        title = title.replace("[오은영의 ‘토닥토닥’]", "").strip()

        # 본문 추출 (줄바꿈 유지)
        content_element = crawling.find('article', id='dic_area')
        content = content_element.get_text(separator='\n', strip=True) if content_element else "내용 없음"
        content = content.replace("[아이가 행복입니다]", "").strip()
        content = content.replace("오은영 소아청소년정신과 전문의", "").strip()

        # ※ 이후의 문장 제거
        content = re.split(r'※', content)[0].strip()

        # 불필요한 부분 제거
        content = re.sub(r'편집자주.*?코너입니다\.?', '', content, flags=re.DOTALL)
        content = re.sub(r'일러스트=.*?기자', '', content)
        content = re.sub(r'게티이미지뱅크', '', content)

        # 연속된 빈 줄 제거
        content = re.sub(r'\n\s*\n', '\n\n', content)

        return title, content