# import os
# import asyncio
# from langchain.llms import OpenAI
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain
#
# llm = OpenAI(temperature=0)
#
# asset_dir = "./asset"
# asset_files = os.listdir(asset_dir)
# asset_list_str = "\n".join(f"- {f}" for f in asset_files)
#
# prompt_template = """
# 너는 3D 에셋 추천 어시스턴트야.
# 아래는 3D 에셋 리스트야:
# {asset_list}
#
# 사용자 문장:
# {text}
#
# 위 에셋들 중 가장 적절한 에셋 파일명들을 골라서,
# 쉼표로 구분된 파일명 리스트 형태로 출력해줘.
# 예) asset1.glb, asset2.glb
# """
#
# prompt = PromptTemplate(
#     input_variables=["asset_list", "text"],
#     template=prompt_template,
# )
#
# llm_chain = LLMChain(llm=llm, prompt=prompt)
# #
# # async def select_assets(label_id: int, text: str) -> list[str]:
# #     result = await asyncio.to_thread(llm_chain.run, asset_list=asset_list_str, text=text)
# #     # 쉼표 기준 분리 후 트림
# #     assets = [a.strip() for a in result.split(",") if a.strip()]
# #     # 실제 있는 파일만 필터링
# #     assets = [a for a in assets if a in asset_files]
# #     return assets
