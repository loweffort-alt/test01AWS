import os
from app.generate_pptx.csv_to_png import csv_to_png
from app.generate_pptx.generate_pptx import crear_pptx
from app.aws.s3_utils import upload_pptx_to_s3


def generate_pptx_from_csv(
        csv_file,
        img_dir,
        name_pptx
):
    """
    CSV a PNG a PPTX por cada línea del CSV.
    """
    # Genera las imágenes en un archivo ./images
    csv_to_png(csv_file, img_dir)

    # Crear la presentación PowerPoint con las imágenes generadas
    # images es un array con los nombres de los pngs en ./images
    images = [f for f in os.listdir(img_dir) if f.endswith('.png')]
    # Asigno la ruta de salida del pptx
    pptx_path = os.path.join(img_dir, name_pptx)
    crear_pptx(images, img_dir, pptx_path)

    # Subir la presentación a s3
    s3_pptx_key = f"presentaciones/{name_pptx}"
    upload_pptx_to_s3(pptx_path, s3_pptx_key)

    # Limpiar imágenes locales
    os.remove(pptx_path)
    for img in images:
        os.remove(os.path.join(img_dir, img))

    print("¡Presentación generada con éxito!")

    return s3_pptx_key


def run():
    generate_pptx_from_csv()
