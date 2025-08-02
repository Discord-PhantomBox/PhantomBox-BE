from model.label_model import TextRequest
from util import llm_util, s3_util
import asyncio

async def select(label_id : int , asset_request : TextRequest):
    text = asset_request.text
    assets = await llm_util.select_assets(label_id, text)
    tasks = [s3_util.get_public_urls_for_folder(folder) for folder in assets]
    results = await asyncio.gather(*tasks)
    all_urls = [url for sublist in results for url in sublist]
    return all_urls
