from dotenv import load_dotenv
from openai import OpenAI
from IPython.display import Image
import json
import urllib
import os

load_dotenv()

# 환경변수에서 OpenAI API 키 불러오기
api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=api_key)


# DALL-E 3 모델을 사용하여 이미지를 생성합니다.
response = client.images.generate(
    model="dall-e-3",
    prompt="The prompt for these images will feature a day's journey, starting from a morning spent studying in a library, followed by a joyous meeting with friends where they share a meal and coffee. This narrative, capturing feelings of fulfillment, will be illustrated in the style of Picasso, known for his unique approach to form and color, emphasizing abstract and cubist interpretations of daily life.",
    size="1024x1024",
    quality="standard",
    n=1,
)

# 생성된 이미지의 URL을 저장합니다.
image_url = response.data[0].url
print(image_url)

Image(url=image_url)
urllib.request.urlretrieve(image_url, "generated_image.jpg")
