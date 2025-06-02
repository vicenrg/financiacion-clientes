
# =============================================================
# 📦 src/data_loading.py — Funciones auxiliares para carga inicial
# Autor: Vicente Rueda
# Usa rutas absolutas robustas con pathlib.
# =============================================================

from pathlib import Path
import pandas as pd
from utils import get_file_path

# -------------------------------------------------------------
# 📁 Mostrar primeras líneas de un archivo de texto plano
# -------------------------------------------------------------
# 📌 Aquí define qué hace la función:
# Muestra por consola las primeras líneas del archivo como texto plano (formato CSV).
# -------------------------------------------------------------
def mostrar_primeras_lineas(folder_key, filename, n=5, ancho_max=400):
    ruta = get_file_path(folder_key, filename)
    print(f"\n📑 Primeras {n} líneas de: {ruta}\n")
    try:
        with ruta.open('r', encoding='utf-8') as archivo:
            for i, linea in enumerate(archivo):
                print(linea.strip()[:ancho_max])
                if i + 1 == n:
                    break
    except FileNotFoundError:
        print(f"❌ Archivo no encontrado: {ruta}")
    except Exception as e:
        print(f"❌ Error al leer archivo: {e}")


# -------------------------------------------------------------
# 📊 Verificar si hay riesgo de sobreajuste por dimensionalidad
# -------------------------------------------------------------
# Evalúa si la relación registros/variables es adecuada para evitar sobreajuste.
# -------------------------------------------------------------
def verificar_dimensionalidad(df, umbral=100):
    n_registros, n_variables = df.shape
    print("\n📊 Verificación de la dimensionalidad:")
    if n_registros >= n_variables * umbral:
        print(f"✅ Adecuado: {n_registros} registros ≥ {n_variables} variables x {umbral}")
        print("   No se detectan problemas de sobreajuste por alta dimensionalidad.")
    else:
        print(f"⚠️ Posible sobreajuste: {n_registros} < {n_variables} x {umbral}")
    print(f"📈 Ratio registros/variable: {n_registros / n_variables:.2f}\n")







