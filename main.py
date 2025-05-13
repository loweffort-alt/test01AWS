import boto3
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from io import BytesIO
import os
from app.generate_pptx.generate_pptx_from_csv import generate_pptx_from_csv
from app.generate_pptx.s3_utils import generate_presigned_url
from fastapi.staticfiles import StaticFiles

app = FastAPI()

s3_client = boto3.client('s3')
BUCKET_NAME = 'pitagoras-test'  # Cambia esto por el nombre de tu bucket


app.mount("/assets",
          StaticFiles(directory="client/dist/assets"),
          name="assets")


@app.get("/")
async def root():
    file_path = os.path.join("client", "dist", "index.html")
    return FileResponse(file_path, media_type="text/html")


# @app.get("/slab-to-nrml")
# async def slab_to_nrml():
#     file_path = os.path.join("public", "mapa_sismos.html")
#     return FileResponse(file_path, media_type="text/html")


@app.get("/mapas_sismos")
async def client_index():
    file_path = os.path.join("public", "mapa_sismos.html")
    return FileResponse(file_path, media_type="text/html")


@app.get("/my-plot")
async def show_plot():
    file_path = os.path.join("public", "my_plot.html")
    return FileResponse(file_path, media_type="text/html")


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


@app.get("/generate-pptx")
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
