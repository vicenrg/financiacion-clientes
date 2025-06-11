# =============================================================
# 📦 src/utils.py — Funciones auxiliares para todo el proyecto
# Autor: Vicente Rueda
# =============================================================

from pathlib import Path
import joblib
import yaml
import pandas as pd
import sys

# -------------------------------------------------------------
# 📁 Obtener la raíz del proyecto
# -------------------------------------------------------------
# Detecta la raíz del proyecto buscando el archivo config/config.yaml
# desde cualquier notebook o script, útil para construir rutas absolutas.
# -------------------------------------------------------------
def get_project_root():
    try:
        current = Path(__file__).resolve()
    except NameError:
        current = Path.cwd().resolve()

    for parent in current.parents:
        if (parent / "config" / "config.yaml").exists():
            return parent
    raise FileNotFoundError("❌ No se encontró config/config.yaml")

# -------------------------------------------------------------
# ⚙️ Configurar entorno desde notebooks
# -------------------------------------------------------------
# Añade al sys.path la ruta al directorio 'src' para permitir
# importaciones de módulos personalizados desde notebooks.
# -------------------------------------------------------------
def configurar_entorno():
    project_root = Path.cwd().resolve().parents[0]
    src_path = project_root / "src"
    if src_path.exists() and str(src_path) not in sys.path:
        sys.path.append(str(src_path))


# -------------------------------------------------------------
# 📄 Cargar archivo de configuración
# -------------------------------------------------------------
# Carga el archivo config.yaml con rutas y parámetros del proyecto.
# -------------------------------------------------------------
def load_config():
    config_path = get_project_root() / "config" / "config.yaml"
    with open(config_path, "r") as f:
        return yaml.safe_load(f)
    

# -------------------------------------------------------------
# 📂 Obtener ruta absoluta de un archivo de datos
# -------------------------------------------------------------
# Construye la ruta absoluta al archivo usando la clave del folder (raw, processed...) y el nombre del archivo.
# -------------------------------------------------------------
def get_file_path(folder_key, filename):
    config = load_config()
    folder_path = get_project_root() / config["paths"][folder_key]
    return folder_path / filename


# -------------------------------------------------------------
# 📄 Cargar archivos de datos en formatos comunes
# -------------------------------------------------------------
# Carga archivos CSV, Excel, JSON, Parquet, Feather según extensión desde la ruta construida.
# -------------------------------------------------------------
def load_data(folder_key, filename):
    file_path = get_file_path(folder_key, filename)
    ext = file_path.suffix.lower()

    if ext == ".csv":
        return pd.read_csv(file_path)
    elif ext in [".xlsx", ".xls"]:
        return pd.read_excel(file_path)
    elif ext == ".json":
        return pd.read_json(file_path)
    elif ext == ".parquet":
        return pd.read_parquet(file_path)
    elif ext == ".feather":
        return pd.read_feather(file_path)
    elif ext == ".pkl":
        return pd.read_pickle(file_path)
    elif ext == ".joblib":
        return joblib.load(file_path)
    else:
        raise ValueError(f"❌ Formato no soportado: {ext}")
    

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
    

# -------------------------------------------------------------
# 💾 Guardar archivo individual (PKL, CSV, JOBLIB)
# -------------------------------------------------------------
def guardar_archivo(obj, folder_key, filename, format="pkl"):
    """
    Guarda un archivo en la carpeta indicada y formato especificado.
    - obj: objeto a guardar (DataFrame, modelo, etc.)
    - folder_key: clave ('cache', 'processed', etc.)
    - filename: nombre del archivo con extensión (sin ruta)
    - format: 'pkl', 'csv' o 'joblib'
    """
    path = get_file_path(folder_key, filename)
    path.parent.mkdir(parents=True, exist_ok=True)

    if format == "pkl":
        pd.to_pickle(obj, path)
    elif format == "joblib":
        joblib.dump(obj, path)
    elif format == "csv":
        obj.to_csv(path, index=False)
    else:
        raise ValueError("❌ Formato no soportado. Usa 'pkl', 'joblib' o 'csv'.")

    print(f"✅ Archivo guardado en: {path.relative_to(Path.cwd().resolve().parents[0])}")



# -----------------------------------------------------------------
# 💾 Guardar múltiples DataFrames en pkl y csv de forma profesional
# -----------------------------------------------------------------
def guardar_multiples_archivos(dataframes: dict):
    """
    Guarda múltiples DataFrames en formato .pkl y .csv en carpetas
    'data/cache' y 'data/processed' respectivamente.
    - dataframes: dict con estructura {'nombre': df}
    """
    for nombre_df, df_obj in dataframes.items():
        for formato, carpeta in zip(['pkl', 'csv'], ['cache', 'processed']):
            nombre_archivo = f"{nombre_df}.{formato}"
            guardar_archivo(df_obj, carpeta, nombre_archivo, format=formato)





















# -------------------------------------------------------------
# 💾 Guardar objetos serializados en cache
# -------------------------------------------------------------
# 📌 Aquí define que hace la función:
# Guarda un objeto Python en la carpeta cache con formato .pkl o .joblib
# -------------------------------------------------------------
def save_object(obj, filename, format="pkl"):
    from pathlib import Path

    cache_dir = get_project_root() / "data" / "cache"
    cache_dir.mkdir(parents=True, exist_ok=True)

    path = cache_dir / filename

    if format == "pkl":
        pd.to_pickle(obj, path)
    elif format == "joblib":
        joblib.dump(obj, path)
    else:
        raise ValueError("❌ Formato no soportado. Usa 'pkl' o 'joblib'.")

    print(f"✅ Objeto guardado en: {path}")







    


