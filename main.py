import boto3
from fastapi import FastAPI, File, UploadFile
from io import BytesIO
from app.generate_pptx_from_csv import generate_pptx_from_csv
from app.s3_utils import generate_presigned_url

app = FastAPI()

s3_client = boto3.client('s3')
BUCKET_NAME = 'pitagoras-test'  # Cambia esto por el nombre de tu bucket


@app.get("/")
async def root():
    return {"message": "Hola Mundo"}


@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    content = await file.read()

    file_stream = BytesIO(content)

    try:
        s3_client.upload_fileobj(file_stream, BUCKET_NAME, file.filename)
        return {"status": "success",
                "filename": file.filename,
                "size": len(content)}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.post("/generate-pptx")
async def generate_pptx():
    try:
        key = generate_pptx_from_csv()
        url = generate_presigned_url(key, BUCKET_NAME)
        return {
            "status": "success",
            "message": "PPTX generado con éxito",
            "download_url": url
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
