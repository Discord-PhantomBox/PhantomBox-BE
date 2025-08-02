import os
import time
import openai
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI as LangOpenAI  # 이름 충돌 피하려고 alias

openai.api_key = os.environ["OPENAI_API_KEY"]

start = time.time()

response = openai.images.generate(
    model="dall-e-3",
    prompt="고릴라 만들어줘.",
    size="1024x1024"
)

image_url = response.data[0].url

end = time.time()
print(f"Image URL: {image_url}")
print(f"총 소요 시간: {end - start:.2f}초")
