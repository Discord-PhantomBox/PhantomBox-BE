import asyncio
import json

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
load_dotenv()

# with open("./assets.txt", "r", encoding="utf-8") as f:
#     asset_dirs = [line.strip().rstrip("/") for line in f if line.strip()]
#
# asset_list_str = "\n".join(f"- {name}" for name in asset_dirs)

with open("asset_metadata.json", "r", encoding="utf-8") as f:
    asset_metadata = json.load(f)

asset_dirs = list(asset_metadata.keys())

asset_list_str = "\n".join(f"- {name}: {meta['title']}" for name, meta in asset_metadata.items())
print(asset_list_str)

prompt_template = """
너는 3D 에셋 추천 어시스턴트야.
아래는 사용 가능한 3D 에셋 폴더 리스트야:
{asset_list}

사용자 문장:
감정 상태: {emotion}
설명: {text}

위 목록 중 적절한 에셋 폴더명들을 골라서,
쉼표로 구분된 형태로 출력해줘.
예) medieval_water_tub, mirror_a
"""

prompt = PromptTemplate(
    input_variables=["asset_list", "emotion", "text"],
    template=prompt_template,
)

llm = OpenAI(temperature=0)
llm_chain = LLMChain(llm=llm, prompt=prompt)

label_mapping = {
    1: "가난한, 불우한",
    2: "걱정스러운",
    3: "고립된",
    4: "괴로워하는",
    5: "당혹스러운",
    6: "두려운",
    7: "배신당한",
    8: "버려진",
    9: "불안",
    10: "상처",
    11: "스트레스 받는",
    12: "억울한",
    13: "조심스러운",
    14: "질투하는",
    15: "초조한",
    16: "충격 받은",
    17: "취약한",
    18: "혼란스러운",
    19: "회의적인",
    20: "희생된"
}


async def select_assets(label_id: int, text: str = "") -> list[str]:
    emotion_text = label_mapping.get(label_id)
    if not emotion_text:
        raise ValueError(f"Invalid label_id: {label_id}")

    full_input = f"감정 상태: {emotion_text}\n설명: {text}".strip()
    print(full_input)

    result = await asyncio.to_thread(
        llm_chain.run,
        asset_list=asset_list_str,
        emotion=emotion_text,
        text=text
    )

    assets = [a.strip().rstrip("/") for a in result.split(",") if a.strip()]
    assets = [a for a in assets if a in asset_dirs]
    return assets

if __name__ == "__main__":
    import asyncio
    result = asyncio.run(select_assets(1, "나는 밤길에 혼자 걷기 무서워."))
    print(result)