import boto3

s3 = boto3.client("s3")
BUCKET_NAME = "hitons"

async def get_presigned_urls_for_folder(folder_prefix: str, expires_in: int = 3600) -> list[str]:
    """
    S3 버킷에서 특정 폴더(prefix)의 파일들에 대해 presigned URL을 반환합니다.
    """
    response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=f"{folder_prefix}")
    if "Contents" not in response:
        return []

    urls = []
    for obj in response["Contents"]:
        key = obj["Key"]
        url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": BUCKET_NAME, "Key": key},
            ExpiresIn=expires_in
        )
        urls.append({
            "file": key,
            "url": url
        })
    return urls
