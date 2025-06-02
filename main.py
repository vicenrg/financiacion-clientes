
# =============================================================
# 🚀 main.py — Fase 01: Carga de datos
# -------------------------------------------------------------
# Este script:
# 1. Muestra las primeras líneas del archivo CSV sin cargarlo.
# 2. Carga el archivo como DataFrame.
# 3. Verifica la dimensionalidad del dataset.
# 4. Genera una tabla descriptiva de las variables.
# 5. Guarda el DataFrame en .pkl y .csv.
# =============================================================

import sys
from pathlib import Path

# -------------------------------------------------------------
# 📁 Configurar rutas
# -------------------------------------------------------------
# Detectar raíz del proyecto y añadir src al sys.path
project_root = Path(__file__).resolve().parent
src_path = project_root / "src"
if str(src_path) not in sys.path:
    sys.path.append(str(src_path))

# -------------------------------------------------------------
# 📥 Importar funciones personalizadas
# -------------------------------------------------------------
from utils import configurar_entorno
configurar_entorno()

from utils import load_data, guardar_archivo
from data_loading import mostrar_primeras_lineas, verificar_dimensionalidad

# -------------------------------------------------------------
# 📑 Paso 1: Mostrar primeras líneas sin cargar
# -------------------------------------------------------------
mostrar_primeras_lineas("raw", "prestamos.csv")
print("\n" + "-" * 100)

# -------------------------------------------------------------
# 📂 Paso 2: Cargar archivo como DataFrame
# -------------------------------------------------------------
print("\n📄 Cargando desde CSV original...")
df = load_data("raw", "prestamos.csv")
print("\n✅ Vista previa del DataFrame:\n", df.head())
print("-" * 100)

# -------------------------------------------------------------
# 📊 Paso 3: Verificar dimensionalidad
# -------------------------------------------------------------
verificar_dimensionalidad(df)
print("-" * 100)

# -------------------------------------------------------------
# 📋 Paso 4: Resumen de estructura del DataFrame
# -------------------------------------------------------------

print("\n📋 Estructura del DataFrame:")
df.info()
print("-" * 100)

# -------------------------------------------------------------
# 💾 Paso 5: Guardar como .pkl y .csv
# -------------------------------------------------------------
guardar_archivo(df, "cache", "trabajo.pkl", format="pkl")
guardar_archivo(df, "processed", "trabajo.csv", format="csv")




