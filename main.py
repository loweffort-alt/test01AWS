# aws
import boto3
# fastapi
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
# python
from io import BytesIO
import os
from uuid import uuid4
# local
from app.generate_pptx.generate_pptx_from_csv import generate_pptx_from_csv
from app.generate_pptx.s3_utils import generate_presigned_url
from app.SlabToNrmlConverter.first import SlabToNrmlConverter

app = FastAPI()
# origins = [
#     "http://localhost:5173",
#     "http://localhost:8000",
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

s3_client = boto3.client('s3')
BUCKET_NAME = 'pitagoras-test'  # Cambia esto por el nombre de tu bucket


app.mount("/public", StaticFiles(directory="public"), name="public")

app.mount("/assets",
          StaticFiles(directory="client/dist/assets"),
          name="assets")


@app.get("/")
async def root():
    file_path = os.path.join("client", "dist", "index.html")
    return FileResponse(file_path, media_type="text/html")


@app.post("/generate-seismic-fonts")
async def generate_seismic_fonts(fuente: str = Form(...),
                                 upper: int = Form(...),
                                 bottom: int = Form(...)
                                 ):
    res = SlabToNrmlConverter(fuente, upper, bottom)
    return res


@app.get("/mapas/1")
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
