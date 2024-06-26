from openai import OpenAI
from dotenv import load_dotenv
from IPython.display import Image, display
import requests
import os

# .env 파일에서 환경변수 로드
load_dotenv()

# 환경변수에서 OpenAI API 키 불러오기
openai_api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=openai_api_key)

# 환경변수에서 Stability API 키 불러오기
stability_api_key = os.getenv('STABLE_DIFFUSION_API_KEY')

def get_user_input():
    '''
    사용자 입력
    '''
    diary_text = input("오늘의 하루는 어땠어? ")
    artist_style = input("어떤 화가로 그려줄까? ")
    return diary_text, artist_style


def generate_description(diary_text, artist_style):
    '''
    GPT description 생성
    '''
    query = f"{diary_text}라는 내용을 {artist_style}의 화풍으로 그려줘"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "The user will provide diary entries in Korean. Translate these entries into English and adapt them into the style of a specified artist."},
            {"role": "system", "content": "Describe the scene you want to illustrate. Mention key characteristics of the style like impressionistic, vibrant colors, or soft lighting."},
            {"role": "user", "content": query}
        ],
    )
    return response.choices[0].message.content


def generate_image_with_stablediffusion(english_prompt):
    """
    Stable Diffusion API를 사용하여 주어진 영어 프롬프트로 이미지를 생성합
    """
    url = "https://api.stability.ai/v2beta/stable-image/generate/core"
    headers = {
        'authorization': f'Bearer {stability_api_key}',
        'accept': 'image/*'
    }
    # 멀티파트 폼 데이터 형식으로 `files` 매개변수 사용
    files = {
        'prompt': (None, english_prompt),
        'output_format': (None, 'png')
    }
    response = requests.post(url, headers=headers, files=files)
    if response.status_code == 200:
        with open("generated_image.png", "wb") as file:
            file.write(response.content)
        print("이미지가 성공적으로 생성되었습니다.")
        return Image("generated_image.png")  # 파일 확장자를 맞춤
    else:
        raise Exception(f"Failed to generate image: {response.text}")


def main():
    diary_text, artist_style = get_user_input()
    english_prompt = generate_description(diary_text, artist_style)
    image = generate_image_with_stablediffusion(english_prompt)
    display(image)

if __name__ == "__main__":
    main()
