
import pandas as pd
from janitor import clean_names
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------------------------------------------
# 🧼 Limpieza básica del DataFrame
# -------------------------------------------------------------
# ➤ Renombra columnas con snake_case
# ➤ Elimina columnas irrelevantes
# ➤ Convierte columnas a tipo numérico
# -------------------------------------------------------------
def limpieza_basica(df):
    df = clean_names(df)
    df.drop(columns=["id_cliente", "id_prestamo", "descripcion"], inplace=True)
    df["antiguedad_empleo"] = df["antiguedad_empleo"].str.extract(r'(\d+)').astype(float)
    df["num_cuotas"] = df["num_cuotas"].str.extract(r'(\d+)').astype(float)
    return df

# -------------------------------------------------------------
# 🧩 Separar variables por tipo
# -------------------------------------------------------------
# ➤ Devuelve dos DataFrames: categóricas y numéricas
# -------------------------------------------------------------
def separar_variables(df):
    cat = df.select_dtypes(include=["object", "category"]).copy()
    num = df.select_dtypes(include="number").copy()
    return cat, num

# -------------------------------------------------------------
# 🔍 Visualizar distribución de nulos por registro
# -------------------------------------------------------------
# ➤ Muestra tabla y gráfico con número de nulos por fila
# -------------------------------------------------------------
def visualizar_nulos_por_registro(df):
    nulos_por_fila = df.isnull().sum(axis=1)
    conteo_nulos = nulos_por_fila.value_counts().sort_index()
    df_nulos = pd.DataFrame({'nº de nulos': conteo_nulos.index, 'registros': conteo_nulos.values})
    print(df_nulos.to_string(index=False))
    plt.figure(figsize=(8, 4))
    ax = sns.barplot(data=df_nulos, x='nº de nulos', y='registros', hue='nº de nulos', palette='Blues_d', legend=False)
    ax.set_title('Distribución de registros según cantidad de valores nulos')
    ax.set_xlabel('Nº de nulos por registro')
    ax.set_ylabel('Cantidad de registros')
    for container in ax.containers:
        ax.bar_label(container, fmt='%.0f', label_type='edge', fontsize=9, padding=2)
    plt.tight_layout()
    return df_nulos

# -------------------------------------------------------------
# 🧩 Tratamiento de nulos en variables categóricas
# -------------------------------------------------------------
# ➤ Rellena con 'otros'
# -------------------------------------------------------------
def tratar_nulos_categoricos(cat_df):
    cat_df.fillna("otros", inplace=True)
    return cat_df
