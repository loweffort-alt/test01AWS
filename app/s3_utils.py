import boto3

s3_client = boto3.client("s3")


def generate_presigned_url(key: str,
                           bucket: str,
                           expiration: int = 3600) -> str:
    """
    Generates a presigned URL to download a file from S3.
    """
    try:
        url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket, "Key": key},
            ExpiresIn=expiration
        )
        return url
    except Exception as e:
        raise RuntimeError(f"Failed to generate presigned URL: {e}")
