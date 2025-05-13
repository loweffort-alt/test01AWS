import boto3
from io import StringIO

# Configuración de AWS S3
s3_client = boto3.client('s3')
BUCKET_NAME = 'pitagoras-test'  # Cambia esto por el nombre de tu bucket


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


def download_csv_from_s3(file_key):
    """
    Descarga un archivo CSV de un bucket S3 y lo guarda localmente.
    """
    csv_obj = s3_client.get_object(Bucket=BUCKET_NAME, Key=file_key)
    # Asigna el contenido CSV a una variable en forma de string
    csv_content = csv_obj['Body'].read().decode('utf-8')

    return StringIO(csv_content)


def upload_pptx_to_s3(file_path, s3_key):
    """
    Sube un archivo a un bucket S3.
    """
    with open(file_path, 'rb') as file:
        s3_client.upload_fileobj(file, BUCKET_NAME, s3_key)
    print(f"Archivo {file_path} subido a S3 como {s3_key}")
