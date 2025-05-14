# aws
import boto3
# fastapi
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
# python
from io import BytesIO
import os
from uuid import uuid4
# local
from app.generate_pptx.main import generate_pptx_from_csv
from app.aws.s3_utils import generate_presigned_url
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


@app.post("/csv-to-pptx")
async def csv_to_pptx(file: UploadFile = File(...)):
    content = await file.read()
    file_stream = BytesIO(content)
    img_dir = "./images"
    name_pptx = f"triangles_{uuid4()}.pptx"

    try:
        key = generate_pptx_from_csv(file_stream, img_dir, name_pptx)
        url = generate_presigned_url(key)
        return {
            "status": "success",
            "message": "PPTX generado con éxito",
            "pptx_name": name_pptx,
            "download_url": url
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
