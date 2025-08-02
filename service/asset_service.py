import json

from pathlib import Path

from model.label_model import TextRequest
from util import llm_util, s3_util
import asyncio
file_path = Path(__file__).resolve().parent.parent / "assets.json"
with open(file_path, "r", encoding="utf-8") as f:
    ASSET_METADATA = json.load(f)


async def select(label_id : int , asset_request : TextRequest):
    text = asset_request.text
    assets = await llm_util.select_assets(label_id, text)
    tasks = [s3_util.get_public_urls_for_folder(folder) for folder in assets]
    results = await asyncio.gather(*tasks)

    all_urls = [url for sublist in results for url in sublist]
    structured_by_asset = await nest_file_structure(all_urls)

    final_response = {}
    for asset in assets:
        final_response[asset] = {
            "title": ASSET_METADATA.get(asset, {}).get("title", ""),
            "description": ASSET_METADATA.get(asset, {}).get("description", ""),
            "files": structured_by_asset.get(asset, {})
        }

    return final_response


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
