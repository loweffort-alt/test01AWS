import os
import boto3
from app.canvas import crear_canvas
from app.csv_reader import leer_csv
from app.generate_pptx import crear_pptx
import matplotlib.pyplot as plt
import numpy as np
from io import StringIO

# Configuración de AWS S3
s3_client = boto3.client('s3')
BUCKET_NAME = 'pitagoras-test'  # Cambia esto por el nombre de tu bucket


def download_csv_from_s3(file_key):
    """
    Descarga un archivo CSV de un bucket S3 y lo guarda localmente.
    """
    csv_obj = s3_client.get_object(Bucket=BUCKET_NAME, Key=file_key)
    csv_content = csv_obj['Body'].read().decode('utf-8')

    return StringIO(csv_content)


def upload_file_to_s3(file_path, s3_key):
    """
    Sube un archivo a un bucket S3.
    """
    with open(file_path, 'rb') as file:
        s3_client.upload_fileobj(file, BUCKET_NAME, s3_key)
    print(f"Archivo {file_path} subido a S3 como {s3_key}")


def generate_pptx_from_csv(
        img_dir="./images",
        name_pptx="triangles.pptx"
):
    s3_key = "triangles.csv"
    csv_file = download_csv_from_s3(s3_key)

    # Leer los datos del CSV
    df = leer_csv(csv_file)

    # Directorio donde guardar las imágenes
    img_dir = './images'  # Cambia este directorio si es necesario
    os.makedirs(img_dir, exist_ok=True)

    # Generar y guardar los gráficos
    for index, row in df.iterrows():
        fig, ax = crear_canvas()

        # Crear puntos
        A = (row['Ax'], row['Ay'])
        B = (row['Bx'], row['By'])
        C = (row['Cx'], row['Cy'])

        triangle = [A, B, C, A]
        triangle_np = np.array(triangle)

        # Dibujar triángulo
        ax.plot(triangle_np[:, 0], triangle_np[:, 1], 'bo-')

        # Etiquetas
        plt.text(*A, f'A{A}', fontsize=12, ha='right')
        plt.text(*B, f'B{B}', fontsize=12, ha='left')
        plt.text(*C, f'C{C}', fontsize=12, ha='right')

        # Título y guardado
        plt.title(f'Triángulo {row["triangulo"]}')
        img_name = f'triangulo_{row["triangulo"]}.png'
        img_path = os.path.join(img_dir, img_name)
        plt.savefig(img_path)
        plt.close()

    # Crear la presentación PowerPoint con las imágenes generadas
    images = [f for f in os.listdir(img_dir) if f.endswith('.png')]
    pptx_path = os.path.join(img_dir, name_pptx)
    crear_pptx(images, img_dir, pptx_path)

    # Subir la presentación a s3
    s3_pptx_key = f"presentaciones/{name_pptx}"
    upload_file_to_s3(pptx_path, s3_pptx_key)

    # Limpiar imágenes locales
    os.remove(pptx_path)
    for img in images:
        os.remove(os.path.join(img_dir, img))

    print("¡Presentación generada con éxito!")

    return s3_pptx_key


def run():
    generate_pptx_from_csv()
