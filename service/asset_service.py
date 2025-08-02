from model.label_model import TextRequest
from util import llm_util, s3_util
import asyncio

async def select(label_id : int , asset_request : TextRequest):
    text = asset_request.text
    assets = await llm_util.select_assets(label_id, text)
    tasks = [s3_util.get_public_urls_for_folder(folder) for folder in assets]
    results = await asyncio.gather(*tasks)
    all_urls = [url for sublist in results for url in sublist]
    response = await nest_file_structure(all_urls)
    return response

async def nest_file_structure(flat_list: list[dict]) -> dict:
    root = {}

    for item in flat_list:
        path_parts = item["file"].split("/")
        current = root

        for part in path_parts[:-1]:  # 디렉토리 부분만 순회
            current = current.setdefault(part, {})

        # 마지막 파일명을 URL로 연결
        current[path_parts[-1]] = item["url"]

    return root
