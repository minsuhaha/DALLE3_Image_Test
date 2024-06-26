import urllib
import os

from openai import OpenAI
from dotenv import load_dotenv
from IPython.display import Image

# .env 파일에서 환경변수 로드
load_dotenv()

# 환경변수에서 OpenAI API 키 불러오기
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)


def get_user_input():
    '''
    사용자 입력
    '''
    diary_text = input("오늘의 하루는 어땠어? ")
    # artist_style = input("어떤 화가로 그려줄까? ")
    return diary_text


def generate_description(diary_text, artist_style):
    '''
    GPT description 생성
    '''
    query = f"{diary_text}라는 내용을 {artist_style} 애니메이션 풍으로 그림을 그려주고 그림을 그리는 도중에 저작권 및 컨텐츠 위반 정책 걸리지 않게 해서 그림을 그려줘!"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Create an art diary entry response reflecting a specific artist's style without naming the artist."},
            {"role": "system", "content": "Describe the scene you want to illustrate. Mention key characteristics of the style like impressionistic, vibrant colors, or soft lighting."},
            {"role": "user", "content": query}
        ],
    )
    return response.choices[0].message.content


def generate_image(description):
    '''
    DALL-E 3를 사용하여 설명(description)에 기반한 이미지 생성
    '''
    response = client.images.generate(
        model="dall-e-3",
        prompt=description,
        size="1024x1024",
        quality="standard",
        n=1
    )
    image_url = response.data[0].url
    return image_url

def main():
    diary_text = get_user_input()
    artists = ["지브리", "디즈니", "픽사", "드림윅스", "그리스 로마 신화"]

    for artist_style in artists:
        description = generate_description(diary_text, artist_style)
        image_url = generate_image(description)
        
        print(f"생성된 이미지 URL ({artist_style}):", image_url)
        
        folder_path = "Animation"
        file_name = f"{folder_path}/{artist_style}.jpg"
        
        # 이미지 다운로드 및 저장
        urllib.request.urlretrieve(image_url, file_name)
    
if __name__ == "__main__":
    main()
