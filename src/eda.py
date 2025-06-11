# eda.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import gaussian_kde



# -----------------------------------------------------------------
# 💾 Cargar Dataframes
# -----------------------------------------------------------------
from utils import load_data, get_file_path

def cargar_dataframes(nombre_archivo: str, alias: str):
    """
    Carga un DataFrame desde cache (Pickle) o procesado (CSV) y lo asigna a un alias.
    
    Parámetros:
    - nombre_archivo: nombre base del archivo sin extensión.
    - alias: nombre del dataset (para imprimir mensajes claros).
    
    Retorna:
    - pd.DataFrame
    """
    ruta_pkl = get_file_path("cache", f"{nombre_archivo}.pkl")
    ruta_csv = get_file_path("processed", f"{nombre_archivo}.csv")

    if ruta_pkl.exists():
        print(f"\n📦 Cargando {alias} desde Pickle...")
        return load_data("cache", f"{nombre_archivo}.pkl")
    else:
        print(f"\n📄 Cargando {alias} desde CSV procesado...")
        return load_data("processed", f"{nombre_archivo}.csv")
    


# -----------------------------------------------------------------
# 🎯 Distribución de la variable objetivo (estado)
# -----------------------------------------------------------------
def plot_cat_distribution(df, col, umbral=0.03):
    freq = df[col].value_counts(normalize=True)
    top15 = freq.head(15)
    total_muestras = df.shape[0]
    top15_abs = df[col].value_counts().head(15)

    # Gráfico completo de distribución
    plt.figure(figsize=(10, 4))
    plt.plot(freq.values, marker='o')
    plt.axhline(y=umbral, color='red', linestyle='--', label=f'Umbral {int(umbral*100)}%')
    plt.axhline(y=0.01, color='orange', linestyle='--', label='Umbral 1%')
    plt.title(f"Distribución de frecuencia relativa en variable: {col}")
    plt.ylabel('Frecuencia relativa')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Gráfico top 15 categorías
    plt.figure(figsize=(10, 5))
    bars = plt.bar(top15.index, top15.values, color='skyblue')
    plt.title(f"Top 15 categorías más frecuentes en variable: {col}")
    plt.ylabel("Frecuencia relativa")
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y')

    for bar, abs_val, rel_val in zip(bars, top15_abs.values, top15.values):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.001,
                 f"{abs_val:,}\n({rel_val:.2%})", ha='center', va='bottom', fontsize=9)

    plt.tight_layout()
    plt.show()


# =============================================================
# 📊 analizar_categoricas_univariado — Análisis univariado de variables categóricas
# -------------------------------------------------------------
# ➤ Aplica la función plot_cat_distribution a cada variable categórica del DataFrame.
# ➤ Genera visualizaciones de distribución y top categorías.
# ➤ Muestra conclusiones y acciones sugeridas por cada variable.
# ➤ Usado en el EDA para explorar frecuencia y cardinalidad por variable.
# =============================================================

def analizar_categoricas_univariado(df_cat, excluir_cols: list = []):
    """
    Recorre todas las columnas categóricas del DataFrame y aplica plot_cat_distribution()
    excepto las que estén en la lista de exclusión (como la variable objetivo).
    
    Parámetros:
    -----------
    df_cat : DataFrame con variables categóricas
    excluir_cols : lista de columnas a excluir del análisis (por defecto vacío)
    """
    for col in df_cat.columns:
        if col in excluir_cols:
            continue
        print(f"\n\n📌 Variable categórica: {col.upper()}")
        plot_cat_distribution(df_cat, col)

        # Conclusiones por variable (basado en ejemplos del proyecto)
        print("📝 CONCLUSIONES:")
        match col:
            case "empleo":
                print("• Alta cardinalidad con muchas categorías poco frecuentes. Requiere agrupación en 'OTROS'.")
            case "ingresos_verificados":
                print("• Solo tres categorías comunes. Puede transformarse con dummies sin problemas.")
            case "rating":
                print("• Categorías como 'F' y 'G' son poco frecuentes. Podrían agruparse como 'rating_bajo'.")
            case "vivienda":
                print("• Tiene una categoría poco representada ('OTROS'). Puede combinarse con otra.")
            case "finalidad":
                print("• Distribución diversa. Evaluar agrupación semántica o por frecuencia.")
            case _:
                print("• No se detectan problemas críticos. Puede usarse tal cual o discretizarse si aplica.")

        print("\n🛠️ ACCIONES A REALIZAR:")
        if col == "empleo":
            print("• Agrupar categorías poco frecuentes como 'OTROS' en 04_feature_engineering.ipynb.")
        elif col in ["rating", "vivienda", "finalidad"]:
            print("• Evaluar agrupación o recategorización en el paso de ingeniería de variables.")
        else:
            print("• Convertir a variables dummies si se mantiene la representación actual.")



# =============================================================
# 📈 analizar_numericas_univariado — Análisis univariado de variables numéricas
# -------------------------------------------------------------
# ➤ Recorre variables numéricas y muestra histogramas y boxplots.
# ➤ Reporta estadísticos básicos e identifica valores extremos.
# ➤ Genera recomendaciones por variable para el paso de feature engineering.
# =============================================================
def analizar_numericas_univariado(df_num):
    """
    Realiza análisis univariado de variables numéricas:
    - Histogramas con KDE
    - Boxplots
    - Estadísticos clave
    - Conclusiones y acciones sugeridas

    Parámetros:
    -----------
    df_num : DataFrame que contiene solo variables numéricas
    """
    for col in df_num.columns:
        print(f"\n\n📌 Variable numérica: {col.upper()}")
        print(df_num[col].describe().round(2).to_string())

        # Gráfico: histograma + boxplot
        fig, axs = plt.subplots(1, 2, figsize=(12, 4))
        sns.histplot(df_num[col], kde=True, ax=axs[0], color="steelblue")
        axs[0].set_title(f"Histograma: {col}")
        sns.boxplot(x=df_num[col], ax=axs[1], color="skyblue")
        axs[1].set_title(f"Boxplot: {col}")
        plt.tight_layout()
        plt.show()

        # Conclusión y acción por variable
        print("📝 CONCLUSIONES:")
        if df_num[col].skew() > 2:
            print("• Distribución muy asimétrica. Puede requerir transformación logarítmica.")
        elif df_num[col].max() > 10000:
            print("• Alto rango de valores. Evaluar normalización o escalado.")
        else:
            print("• Distribución razonable. Puede usarse directamente.")

        print("🛠️ ACCIONES A REALIZAR:")
        if df_num[col].isnull().sum() > 0:
            print("• Imputar valores nulos (ya aplicados en limpieza, revisar si persisten).")
        print("• Evaluar normalización, escalado o transformación log en 04_feature_engineering.ipynb.")


# =============================================================
# 📈 plot_density_with_stats_matplotlib — Gráfico de densidad con estadísticas
# -------------------------------------------------------------
# ➤ Muestra curva de densidad, media, mediana y ±3 desviaciones estándar.
# ➤ Complemento visual para variables numéricas en análisis univariado.
# =============================================================
def plot_density_with_stats_matplotlib(data, col):
    """
    Genera un gráfico de densidad con líneas para media, mediana y ±3σ.
    
    Parámetros:
    -----------
    data : DataFrame con la columna numérica
    col  : nombre de la columna a graficar
    """
    data = data[col].dropna().astype(float)
    mean = data.mean()
    median = data.median()
    std = data.std()

    # Calcular densidad
    density = gaussian_kde(data)
    xs = np.linspace(data.min(), data.max(), 500)
    ys = density(xs)

    # Crear gráfico
    plt.figure(figsize=(8, 4))
    plt.plot(xs, ys, label='Densidad', color='gray')
    plt.fill_between(xs, ys, alpha=0.3)

    # Líneas estadísticas
    plt.axvline(mean, color='blue', linestyle='--', linewidth=1.5, label=f'Media: {mean:.2f}')
    plt.axvline(median, color='green', linestyle='--', linewidth=1.5, label=f'Mediana: {median:.2f}')
    plt.axvline(mean + 3 * std, color='red', linestyle=':', linewidth=1, label='+3σ')
    plt.axvline(mean - 3 * std, color='red', linestyle=':', linewidth=1, label='-3σ')

    plt.title(f'Densidad de {col}')
    plt.xlabel(col)
    plt.ylabel('Densidad')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# =============================================================
# 📊 analizar_numericas_univariado — Análisis de variables numéricas
# -------------------------------------------------------------
# ➤ Ejecuta describe().T + gráfico de densidad + boxplot.
# ➤ Genera recomendaciones automáticas para ingeniería de variables.
# =============================================================

def analizar_numericas_univariado(df_num):
    """
    Analiza variables numéricas con resumen estadístico + gráficos.

    Parámetros:
    -----------
    df_num : DataFrame con columnas numéricas limpias
    """
    for col in df_num.columns:
        print(f"\n\n📌 Variable numérica: {col.upper()}")
        display(df_num[[col]].describe().T.round(2))

        # Gráfico de densidad + estadísticas
        plot_density_with_stats_matplotlib(df_num, col)

        # Boxplot horizontal
        plt.figure(figsize=(8, 1.5))
        sns.boxplot(x=df_num[col], color='skyblue')
        plt.title(f'Boxplot de {col}')
        plt.grid(True)
        plt.tight_layout()
        plt.show()

        # Conclusiones y acciones
        print("📝 CONCLUSIONES:")
        if df_num[col].skew() > 2:
            print("• Distribución muy asimétrica. Puede requerir transformación logarítmica.")
        elif df_num[col].max() > 10000:
            print("• Alto rango de valores. Puede ser útil aplicar escalado.")
        else:
            print("• Distribución razonable para modelado directo.")

        print("🛠️ ACCIONES A REALIZAR:")
        if df_num[col].isnull().sum() > 0:
            print("• Imputar nulos si persisten.")
        print("• Evaluar log-transformación, normalización o estandarización en 04_feature_engineering.ipynb.")







