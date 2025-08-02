import os

import boto3



s3 = boto3.client(
    's3',
    region_name='ap-northeast-2',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

BUCKET_NAME = "hitons"
REGION = "ap-northeast-2"

async def get_public_urls_for_folder(folder_prefix: str) -> list[dict]:
    """
    퍼블릭 S3 버킷에서 특정 폴더(prefix)의 파일들에 대해 퍼블릭 URL을 반환합니다.
    """
    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=f"{folder_prefix}/")
    if "Contents" not in response:
        return []

    urls = []
    for obj in response["Contents"]:
        key = obj["Key"]
        print(key)

        # 퍼블릭 URL 생성
        url = f"https://{BUCKET_NAME}.s3.{REGION}.amazonaws.com/{key}"
        print(url)

        urls.append({
            "file": key,
            "url": url
        })

    return urls

if __name__ == "__main__":
    import asyncio
    result = asyncio.run(get_public_urls_for_folder("mirror_a"))
    print(result)
