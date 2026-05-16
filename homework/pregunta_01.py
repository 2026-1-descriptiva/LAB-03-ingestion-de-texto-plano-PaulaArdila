"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel

import pandas as pd
import re

def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.


    """
    with open("files/input/clusters_report.txt", encoding="utf-8") as file:
        lines = file.readlines()

    # Eliminar líneas vacías y separadores
    lines = [
        line.rstrip()
        for line in lines
        if line.strip() != "" and not line.startswith("-")
    ]

    # Encabezados
    columns = [
        "cluster",
        "cantidad_de_palabras_clave",
        "porcentaje_de_palabras_clave",
        "principales_palabras_clave",
    ]

    rows = []
    current_row = None

    for line in lines[2:]:
        # Detecta inicio de un nuevo cluster
        match = re.match(r"\s*(\d+)\s+(\d+)\s+([\d,]+\s?%)\s+(.*)", line)

        if match:
            if current_row is not None:
                rows.append(current_row)

            current_row = [
                int(match.group(1)),
                int(match.group(2)),
                match.group(3),
                match.group(4).strip(),
            ]

        else:
            # Continuación de palabras clave
            if current_row is not None:
                current_row[3] += " " + line.strip()

    # Agregar última fila
    if current_row is not None:
        rows.append(current_row)

    # Crear dataframe
    df = pd.DataFrame(rows, columns=columns)

    # Normalizar espacios en keywords
    df["principales_palabras_clave"] = (
        df["principales_palabras_clave"]
        .str.replace(r"\s+", " ", regex=True)
        .str.replace(r"\s*,\s*", ", ", regex=True)
        .str.strip()
        .str.strip(".")
    )

    # Extraer porcentajes
    df.porcentaje_de_palabras_clave = df.porcentaje_de_palabras_clave.str.strip(" %").str.replace(",", ".").astype(float)

    return df


if __name__ == "__main__":
    df = pregunta_01()
    print(df)