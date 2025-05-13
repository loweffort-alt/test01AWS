from app.generate_pptx.canvas import crear_canvas
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


def csv_to_png(file_obj, img_dir):
    # Leer el archivo CSV
    df = pd.read_csv(file_obj)

    # Directorio donde guardar las imágenes
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
