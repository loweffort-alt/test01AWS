# import pandas as pd
import numpy as np
# import math
# from shapely.geometry import Point, Polygon, LineString
from shapely.geometry import Point, Polygon, LineString
import geopandas as gpd
import os
from uuid import uuid4
# from collections import defaultdict
# import xml.etree.ElementTree as ET
# import xml.dom.minidom as minidom
import plotly.graph_objects as go
import argparse


def SelectPolygon(fuente):
    #########################################################
    # 3.1 identifica los lados de la fuente original
    # Editable entre
    # ["interfase | F-3a", "interfase | F-4a","interfase | F-5a.1",
    # "intraplaca | F-3b", "intraplaca | F-3c", "intraplaca | F-4b",
    # "intraplaca | F-4c.1","intraplaca | F-4c.2","intraplaca | F-5b.1",
    # "intraplaca | F-5c.1",
    # "corteza | PSw-3","corteza | PSw-4","corteza | PSe-3","corteza | PSe-5",
    # "corteza | PSw-5","corteza | PSe-4", "corteza | PSe-6"]

    polys_interfase = gpd.GeoSeries({
        'F-1a': Polygon([(-81.558, -2.43), (-80.041, -2.07), (-80.042, -1.344), (-79.998, -1.147), (-79.841, -0.492), (-79.495, 0.323), (-79.212, 0.79), (-78.914, 1.227), (-78.597, 1.648), (-78.266, 2.016), (-77.579, 2.914), (-78.664, 3.318), (-79.388, 2.507), (-79.924, 1.898), (-80.16, 1.622), (-80.418, 1.226), (-80.669, 0.71), (-80.997, -0.056), (-81.295, -0.649), (-81.367, -1.006), (-81.477, -1.506), (-81.552, -1.885)]),
        'F-2a': Polygon([(-81.933, -6.015), (-80.25, -5.459), (-80.281, -4.844), (-80.251, -4.406), (-80.145, -3.833), (-80.088, -3.369), (-80.047, -2.808), (-80.041, -2.07), (-81.558, -2.43), (-81.608, -2.799), (-81.695, -3.158), (-81.859, -3.852), (-81.94, -4.411), (-81.954, -5.315)]),
        'F-3a': Polygon([(-81.933, -6.015), (-80.25, -5.459), (-80.145, -5.943), (-79.388, -7.934), (-79.159, -8.475), (-78.675, -9.455), (-80.008, -10.191), (-80.008, -10.191), (-80.011, -10.19), (-80.201, -9.878), (-80.404, -9.527), (-80.908, -8.651), (-81.249, -7.952), (-81.576, -7.21), (-81.776, -6.65)]),
        'F-4a': Polygon([(-78.675, -9.455), (-80.008, -10.191), (-79.608, -10.917), (-79.306, -11.371), (-78.927, -11.912), (-78.611, -12.403), (-78.291, -12.906), (-78.011, -13.27), (-77.529, -13.899), (-76.822, -14.736), (-75.614, -13.801), (-76.655, -12.426), (-76.877, -12.116), (-77.518, -11.333)]),
        'F-5a.1': Polygon([(-74.27, -16.889), (-74.418, -16.775), (-74.879, -16.53), (-75.356, -16.122), (-75.916, -15.558), (-76.822, -14.736), (-75.614, -13.801), (-75.329, -14.226), (-74.939, -14.755), (-74.146, -15.475), (-73.572, -15.869)]),
        'F-5a.2': Polygon([(-73.572, -15.869), (-73.28, -16.069), (-72.758, -16.439), (-72.409, -16.721), (-71.036, -17.812), (-70.564, -18.332), (-71.567, -19.373), (-71.85, -18.968), (-72.27, -18.562), (-73.064, -17.847), (-73.508, -17.475), (-74.27, -16.889)]),
        'F-6a': Polygon([(-71.567, -19.373), (-70.564, -18.332), (-70.267, -18.804), (-69.93, -19.6), (-69.829, -19.972), (-69.615, -21.516), (-69.579, -22.694), (-69.622, -23.548), (-69.86, -25.014), (-71.45, -24.976), (-71.18, -21.528), (-71.279, -20.484)]),
    })
    polys_intraplaca = gpd.GeoSeries({
        'F-1b.1': Polygon([(-79.841, -0.492), (-78.663, -0.755), (-77.544, -0.893), (-76.908, -0.862), (-76.732, 0.216), (-76.706, 0.378), (-76.519, 0.979), (-76.272, 1.514), (-75.942, 2.383), (-77.579, 2.914), (-78.266, 2.016), (-78.597, 1.648), (-78.914, 1.227), (-79.212, 0.79), (-79.495, 0.323)]),
        'F-1b.2': Polygon([(-80.041, -2.07), (-80.042, -1.344), (-79.998, -1.147), (-79.998, -1.147), (-79.841, -0.492), (-78.663, -0.755), (-78.625, -1.406), (-78.505, -1.731), (-78.369, -2.142), (-78.198, -2.869), (-78.641, -2.871), (-79.424, -2.858), (-80.047, -2.808)]),
        'F-1c': Polygon([(-78.663, -0.755), (-77.544, -0.893), (-76.908, -0.862), (-76.713, -1.176), (-76.536, -1.482), (-76.475, -1.559), (-76.246, -1.756), (-75.91, -2.085), (-76.734, -2.549), (-77.598, -2.819), (-78.198, -2.869), (-78.369, -2.142), (-78.505, -1.731), (-78.625, -1.406)]),
        'F-2b': Polygon([(-80.25, -5.459), (-80.281, -4.844), (-80.251, -4.406), (-80.145, -3.833), (-80.088, -3.369), (-80.047, -2.808), (-79.424, -2.858), (-78.641, -2.871), (-78.198, -2.869), (-78.193, -3.708), (-78.193, -3.708), (-78.237, -4.191), (-78.243, -4.779)]),
        'F-2c': Polygon([(-78.243, -4.779), (-78.237, -4.191), (-78.193, -3.708), (-78.198, -2.869), (-77.598, -2.819), (-76.734, -2.549), (-75.91, -2.085), (-75.634, -2.367), (-75.396, -2.718), (-75.268, -2.987), (-75.178, -3.352), (-75.149, -3.741)]),
        'F-3b': Polygon([(-80.25, -5.459), (-78.243, -4.779), (-78.162, -5.322), (-78.005, -6.071), (-77.68, -6.613), (-77.36, -7.335), (-76.796, -8.414), (-78.675, -9.455), (-79.159, -8.475), (-79.388, -7.934), (-80.145, -5.943)]),
        'F-3c': Polygon([(-76.796, -8.414), (-77.36, -7.335), (-77.68, -6.613), (-78.005, -6.071), (-78.162, -5.322), (-78.243, -4.779), (-75.149, -3.741), (-75.131, -4.172), (-75.075, -4.643), (-75.005, -4.969), (-74.846, -5.366), (-74.643, -5.751), (-74.407, -6.146), (-74.254, -6.4), (-74.024, -6.868)]),
        'F-4b': Polygon([(-78.675, -9.455), (-76.796, -8.414), (-76.407, -9.295), (-76.111, -10.173), (-75.916, -10.622), (-75.685, -10.98), (-75.218, -11.387), (-74.846, -11.919), (-74.206, -12.707), (-75.614, -13.801), (-76.655, -12.426), (-76.877, -12.116), (-77.518, -11.333)]),
        'F-4c.1': Polygon([(-76.796, -8.414), (-74.024, -6.868), (-73.939, -7.066), (-73.844, -7.325), (-73.833, -7.885), (-73.868, -8.461), (-73.878, -8.633), (-73.835, -8.928), (-76.111, -10.173), (-76.407, -9.295)]),
        'F-4c.2': Polygon([(-76.111, -10.173), (-73.835, -8.928), (-73.74, -9.177), (-73.601, -9.417), (-73.479, -9.625), (-73.313, -9.833), (-72.891, -10.22), (-72.527, -10.613), (-72.105, -11.046), (-72.414, -11.309), (-72.417, -11.312), (-74.206, -12.707), (-74.846, -11.919), (-75.218, -11.387), (-75.685, -10.98), (-75.916, -10.622)]),
        'F-5b.1': Polygon([(-75.614, -13.801), (-74.206, -12.707), (-73.153, -13.949), (-72.397, -14.832), (-72.771, -15.217), (-73.28, -16.069), (-74.146, -15.475), (-74.939, -14.755), (-75.329, -14.226)]),
        'F-5c.1': Polygon([(-74.206, -12.707), (-72.417, -11.312), (-72.154, -11.668), (-72.015, -11.869), (-71.8, -12.331), (-71.597, -12.978), (-71.414, -13.524), (-71.309, -13.924), (-71.258, -14.171), (-72.013, -14.496), (-72.013, -14.496), (-72.397, -14.832), (-73.153, -13.949)]),
        'F-5b.2': Polygon([(-73.28, -16.069), (-72.771, -15.217), (-72.397, -14.832), (-72.013, -14.496), (-71.258, -14.171), (-71.262, -15.193), (-71.108, -15.856), (-70.707, -16.219), (-69.516, -16.97), (-70.564, -18.332), (-71.036, -17.812), (-72.409, -16.721), (-72.758, -16.439)]),
        'F-5c.2': Polygon([(-71.258, -14.171), (-70.245, -13.738), (-69.935, -14.35), (-69.813, -14.577), (-69.666, -14.714), (-69.438, -14.934), (-69.411, -14.998), (-69.067, -15.227), (-68.482, -15.613), (-68.847, -16.123), (-69.167, -16.538), (-69.516, -16.97), (-70.707, -16.219), (-71.108, -15.856), (-71.262, -15.193)]),
        'F-6b': Polygon([(-70.564, -18.332), (-69.516, -16.97), (-68.971, -17.922), (-68.575, -18.821), (-67.921, -20.595), (-67.459, -22.83), (-67.289, -24.263), (-67.256, -25.019), (-69.86, -25.014), (-69.622, -23.548), (-69.579, -22.694), (-69.615, -21.516), (-69.829, -19.972), (-69.93, -19.6), (-70.267, -18.804)]),
    })
    polys_corteza = gpd.GeoSeries({
        'PSe-1': Polygon([(-79.219, -2.417), (-79.256, -2.168), (-79.52, -0.082), (-78.021, 1.689), (-76.925, 1.172), (-77.245, -1.571)]),
        'PSe-2': Polygon([(-77.245, -1.571), (-76.847, -2.864), (-76.402, -4.64), (-78.28, -5.361), (-78.717, -4.458), (-79.219, -2.417)]),
        'PSe-3': Polygon([(-78.28, -5.361), (-76.402, -4.64), (-75.889, -5.555), (-75.516, -6.27), (-75.227, -7.379), (-76.926, -8.542), (-77.49, -7.004)]),
        'PSe-4': Polygon([(-76.402, -4.64), (-75.361, -4.599), (-73.763, -6.213), (-73.228, -8.298), (-74.063, -10.05), (-75.045, -8.717), (-75.227, -7.379), (-75.516, -6.27), (-75.889, -5.555)]),
        'PSe-5': Polygon([(-76.926, -8.542), (-75.227, -7.379), (-75.045, -8.717), (-74.063, -10.05), (-73.711, -10.545), (-72.31, -11.63), (-73.381, -12.815), (-73.861, -13.316), (-74.474, -12.821), (-75.381, -12.024)]),
        'PSe-6': Polygon([(-73.381, -12.815), (-72.31, -11.63), (-71.215, -12.137), (-70.327, -12.512), (-69.429, -12.963), (-69.81, -13.944), (-70.287, -15.166), (-70.76, -13.942), (-71.243, -13.211), (-71.969, -13.001), (-72.507, -12.871)]),
        'PSw-1': Polygon([(-78.717, -4.458), (-79.219, -2.417), (-79.256, -2.168), (-80.53, -2.897), (-80.559, -3.785), (-80.604, -4.337), (-80.572, -5.268), (-80.525, -5.589)]),
        'PSw-2': Polygon([(-78.717, -4.458), (-80.525, -5.589), (-80.121, -6.381), (-79.699, -7.211), (-79.34, -7.91), (-77.49, -7.004), (-78.28, -5.361)]),
        'PSw-3': Polygon([(-77.49, -7.004), (-76.926, -8.542), (-75.381, -12.024), (-74.474, -12.821), (-75.717, -13.738), (-76.29, -13.054), (-77.041, -11.976), (-77.373, -11.519), (-77.564, -11.212), (-78.409, -9.646), (-79.03, -8.452), (-79.34, -7.91)]),
        'PSw-4': Polygon([(-75.717, -13.738), (-74.474, -12.821), (-73.861, -13.316), (-72.13, -14.95), (-73.102, -16.274), (-73.515, -16.001), (-74.793, -14.7)]),
        'PSw-5': Polygon([(-73.861, -13.316), (-73.381, -12.815), (-72.507, -12.871), (-71.969, -13.001), (-71.243, -13.211), (-70.76, -13.942), (-70.287, -15.166), (-70.479, -15.744), (-72.13, -14.95)]),
        'PSw-6': Polygon([(-73.102, -16.274), (-72.13, -14.95), (-70.479, -15.744), (-69.175, -17.883), (-69.901, -18.512)]),
    })

    fuente_name_orig = fuente.split(" | ")[1]

    if fuente.split(" | ")[0] == "interfase":
        poly = polys_interfase
    elif fuente.split(" | ")[0] == "intraplaca":
        poly = polys_intraplaca
    elif fuente.split(" | ")[0] == "corteza":
        poly = polys_corteza

    polygon_fuente_orig = poly[fuente_name_orig]
    return polygon_fuente_orig


def SlabToNrmlConverter(fuente: str, upper: int, bottom: int):
    """
    Convierte un shapefile de slab a un formato normalizado.
    """
    project_root = os.path.abspath(os.path.join(
        os.path.dirname(__file__), "..", ".."))

    shape_file_path = os.path.join(project_root,
                                   "public",
                                   "slab2.0 - subduction",
                                   "sam_depth_5km.shp")

    if not os.path.exists(shape_file_path):
        raise FileNotFoundError(
            f"El archivo {shape_file_path} no existe. Asegúrate de que la ruta sea correcta.")

    gdf_5km = gpd.read_file(shape_file_path)

    fuente_name_orig = fuente.split(" | ")[1]

# Graficamos la fuente con el slab cortado
#########################################################
    polygon_fuente_orig = SelectPolygon(fuente)

    coords = list(polygon_fuente_orig.exterior.coords)
    segmentos_este = []

    for i in range(len(coords) - 1):
        p1 = coords[i]
        p2 = coords[i + 1]
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]

        # Condición: seno > 0 y coseno > 0 (ángulo entre 0° y 90°)
        if dy > 0 and dx < 0:
            segmentos_este.append((p1, p2))

# Construir LineString continuo
    if not segmentos_este:
        raise ValueError(
            "No se encontraron segmentos con seno positivo y coseno negativo.")

# Aplanar en secuencia sin repetir nodos
    puntos_este = [segmentos_este[0][0]] + [seg[1] for seg in segmentos_este]
    lado_este = LineString(puntos_este)

#####################
    segmentos_oeste = []
    for i in range(len(coords) - 1):
        p1 = coords[i]
        p2 = coords[i + 1]
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]

        # Condición: seno > 0 y coseno > 0 (ángulo entre 0° y 90°)
        if dy < 0 and dx > 0:
            segmentos_oeste.append((p1, p2))

# Construir LineString continuo
    if not segmentos_oeste:
        raise ValueError(
            "No se encontraron segmentos con seno negativo y coseno positivo.")

# Aplanar en secuencia sin repetir nodos
    puntos_oeste = [segmentos_oeste[0][0]] + [seg[1]
                                              for seg in segmentos_oeste]
    lado_oeste = LineString(puntos_oeste)

############
    segmentos_sur = []
    for i in range(len(coords) - 1):
        p1 = coords[i]
        p2 = coords[i + 1]
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]

        # Condición: seno > 0 y coseno > 0 (ángulo entre 0° y 90°)
        if dy > 0 and dx > 0:
            segmentos_sur.append((p1, p2))
# Construir LineString continuo
    if not segmentos_sur:
        raise ValueError(
            "No se encontraron segmentos con seno y coseno positvos.")

# Aplanar en secuencia sin repetir nodos
    puntos_sur = [segmentos_sur[0][0]] + [seg[1] for seg in segmentos_sur]
    lado_sur = LineString(puntos_sur)
# lado_sur = LineString(np.array([(-76.111, -10.173),(-73.835, -8.928)]))
############
    segmentos_norte = []
    for i in range(len(coords) - 1):
        p1 = coords[i]
        p2 = coords[i + 1]
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]

        # Condición: seno > 0 y coseno > 0 (ángulo entre 0° y 90°)
        if dy < 0 and dx < 0:
            segmentos_norte.append((p1, p2))
# Construir LineString continuo
    if not segmentos_norte:
        raise ValueError(
            "No se encontraron segmentos con seno y coseno negativos.")

# Aplanar en secuencia sin repetir nodos
    puntos_norte = [segmentos_norte[0][0]] + [seg[1]
                                              for seg in segmentos_norte]
    lado_norte = LineString(puntos_norte)
# lado_norte = LineString(np.array([(-76.111, -10.173),(-73.835, -8.928)]))
#########################################################
#########################################################
#########################################################
#########################################################
# 3.2 extiende los lados norte y sur

    def extender_linea_misma_pendiente(linea: LineString, extension: float = 0.5) -> LineString:
        coords = np.array(linea.coords)

        # Extremos
        p_start = coords[0]
        p_end = coords[-1]

        # Vector dirección (de start a end)
        vector = p_end - p_start
        vector_unit = vector / np.linalg.norm(vector)

        # Extensión hacia afuera
        p_start_ext = p_start - extension * vector_unit
        p_end_ext = p_end + extension * vector_unit

        # Construir nueva secuencia de puntos
        new_coords = [tuple(p_start_ext)] + coords[1:-
                                                   1].tolist() + [tuple(p_end_ext)]
        return LineString(new_coords)


# Aplicar a los lados norte y sur
    lado_norte_ext = extender_linea_misma_pendiente(lado_norte, extension=0.8)
    lado_sur_ext = extender_linea_misma_pendiente(lado_sur, extension=0.8)

    def ordenar_coords_en_direccion(linea: LineString, sentido: str = "asc") -> list:
        coords = list(linea.coords)
        # Ordenar por longitud (x) ascendente o descendente
        if (sentido == "asc" and coords[0][0] > coords[-1][0]) or (sentido == "desc" and coords[0][0] < coords[-1][0]):
            coords = coords[::-1]
        return coords


# Asegurar direcciones
    coords_norte = ordenar_coords_en_direccion(lado_norte_ext, sentido="asc")
    coords_sur = ordenar_coords_en_direccion(lado_sur_ext, sentido="desc")

# Concatenar y cerrar
    coords_fuente = coords_norte + coords_sur
    if coords_fuente[0] != coords_fuente[-1]:
        coords_fuente.append(coords_fuente[0])

# Crear polígono final ordenado antihorario
    nueva_fuente = Polygon(coords_fuente)

#########################################################
#########################################################
#########################################################
#########################################################
# 3.3 corta la fuente extendida con el slab y grafíca

    polygon_fuente = nueva_fuente

    dgpd_shape_cropped = gpd.clip(gdf_5km, polygon_fuente)
    min_lon, min_lat, max_lon, max_lat = polygon_fuente.bounds

# -----------------------------------
# Inicializar estructura de datos
# -----------------------------------
    points_within_source = {}
    depths_by_line = {}

# Extraer coordenadas de líneas dentro del polígono
    for index, row in dgpd_shape_cropped.iterrows():
        geometry = row.geometry
        depth = row['level']

        if geometry.geom_type == 'MultiLineString':
            for i, linestring in enumerate(geometry.geoms):
                line_id = f"{index}-{i}"
                points_within_source[line_id] = []
                depths_by_line[line_id] = depth

                for point in linestring.coords:
                    if polygon_fuente.contains(Point(point)):
                        points_within_source[line_id].append(point)
        else:
            line_id = str(index)
            points_within_source[line_id] = []
            depths_by_line[line_id] = depth

            for point in geometry.coords:
                if polygon_fuente.contains(Point(point)):
                    points_within_source[line_id].append(point)

# -----------------------------------
# Construcción de la estructura `data`
# -----------------------------------
    sorted_lines = sorted(depths_by_line.items(), key=lambda item: item[1])
    data = []

    for i, (line_id, depth) in enumerate(sorted_lines):
        edge_type = (
            "faultBottomEdge" if i == 0 else
            "faultTopEdge" if i == len(sorted_lines) - 1 else
            "intermediateEdge"
        )

        coords = [
            (round(point[0], 3), round(point[1], 3), -1 * depth)
            for point in points_within_source[line_id]
        ]

        data.append({
            "id": "1",
            "name": fuente_name_orig,
            "Edge": edge_type,
            "coords": coords
        })

# -----------------------------------
# Gráfico Plotly combinado
# -----------------------------------
    fig = go.Figure()

# Shapefile sin cortar (negro)
    for _, row in gdf_5km.iterrows():
        geom = row.geometry
        depth = row['level']
        if geom.geom_type == 'MultiLineString':
            for line in geom.geoms:
                x, y = list(line.xy[0]), list(line.xy[1])
                fig.add_trace(go.Scattergeo(
                    lon=x, lat=y, mode='lines',
                    line=dict(width=1, color='black'),
                    name=f" {depth} km"
                ))
        else:
            x, y = list(geom.xy[0]), list(geom.xy[1])
            fig.add_trace(go.Scattergeo(
                lon=x, lat=y, mode='lines',
                line=dict(width=1, color='black'),
                name=f" {depth} km"
            ))

# Shapefile recortado (azul)
    for _, row in dgpd_shape_cropped.iterrows():
        geom = row.geometry
        depth = row['level']
        if geom.geom_type == 'MultiLineString':
            for line in geom.geoms:
                x, y = list(line.xy[0]), list(line.xy[1])
                fig.add_trace(go.Scattergeo(
                    lon=x, lat=y, mode='lines',
                    line=dict(width=2.5, color='blue'),
                    name=f" {depth} km"
                ))
        else:
            x, y = list(geom.xy[0]), list(geom.xy[1])
            fig.add_trace(go.Scattergeo(
                lon=x, lat=y, mode='lines',
                line=dict(width=2.5, color='blue'),
                name=f"{depth} km"
            ))

# Polígono fuente (rojo)
    x_poly, y_poly = list(polygon_fuente.exterior.xy[0]), list(
        polygon_fuente.exterior.xy[1])
    fig.add_trace(go.Scattergeo(
        lon=x_poly, lat=y_poly, mode='lines',
        line=dict(width=3, color='red'),
        name='Fuente sísmica'
    ))

# 2. original fuente construida (yellow)

    x_poly, y_poly = list(polygon_fuente_orig.exterior.xy[0]), list(
        polygon_fuente_orig.exterior.xy[1])
    fig.add_trace(go.Scattergeo(
        lon=x_poly, lat=y_poly, mode='lines',
        line=dict(width=3, color='yellow'),
        name='Fuente sísmica'
    ))

# Layout
    fig.update_layout(
        title=f"Slab completo (negro), recortado (azul), y fuente ({
            fuente_name_orig})",
        geo=dict(
            resolution=50,
            showland=True,
            landcolor='lightgray',
            showocean=True,
            oceancolor='lightblue',
            lonaxis=dict(range=[min_lon - 1, max_lon + 1]),
            lataxis=dict(range=[min_lat - 1, max_lat + 1])
        ),
        height=800
    )

    html_name = uuid4().hex
    fig.write_html(f"public/htmls-generados/{html_name}.html")
    return {"url": f"http://localhost:8000/public/htmls-generados/{html_name}.html"}

# -----------------------------------
# Mostrar estructura `data`
# -----------------------------------
    for item in data:
        print(item)
        print()  # Línea en blanco entre elementos
#########################################################
#########################################################
#########################################################
#########################################################
# 3.4 visualmente escojes un bottom
# Editable variables: bottom, upper
    data = [d for d in data if all(z <= bottom for _, _, z in d['coords'])]
    data = [d for d in data if all(z >= upper for _, _, z in d['coords'])]

# -------------------------------------------------------


if __name__ == "__main__":
    # Ejemplo de uso
    parser = argparse.ArgumentParser(
        description='Convert slab to normalized format.')
    parser.add_argument('fuente', type=str, help='Nombre de la fuente')
    parser.add_argument('upper', type=int, help='Profundidad superior')
    parser.add_argument('bottom', type=int, help='Profundidad inferior')
    args = parser.parse_args()

    SlabToNrmlConverter(args.fuente, args.upper, args.bottom)
