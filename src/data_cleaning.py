
import pandas as pd
from janitor import clean_names
from IPython.display import display

# -------------------------------------------------------------
# 🧹 Limpieza general de variables
# -------------------------------------------------------------
# ➤ Estándariza nombres, elimina columnas irrelevantes y transforma datos.
# -------------------------------------------------------------
def limpiar_variables_basicas(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # 1️⃣ Estandarizar nombres
    df = clean_names(df)

    # 2️⃣ Eliminar columnas irrelevantes
    columnas_eliminar = ['id_cliente', 'id_prestamo', 'descripcion']
    df = df.drop(columns=columnas_eliminar, errors='ignore')

    # 3️⃣ Convertir columnas con texto a numéricas (extraer dígitos)
    if 'antiguedad_empleo' in df.columns:
        df['antiguedad_empleo'] = (
            df['antiguedad_empleo']
            .astype(str)
            .str.extract(r'(\d+)')[0]
            .astype(float)
        )

    if 'num_cuotas' in df.columns:
        df['num_cuotas'] = (
            df['num_cuotas']
            .astype(str)
            .str.extract(r'(\d+)')[0]
            .astype(float)
        )

    return df


# -------------------------------------------------------------
# 🧹 Eliminación de registros duplicados
# -------------------------------------------------------------
# ➤ Elimina duplicados del DataFrame y muestra estadísticas antes y después.
# -------------------------------------------------------------
def eliminar_duplicados(df):
    """
    Elimina registros duplicados del DataFrame e imprime información resumen.
    """
    print("\n🧹 Eliminación de registros duplicados:")
    print(f"   ➤ Registros antes: {df.shape[0]}")
    print(f"   ➤ Duplicados detectados: {df.duplicated().sum()}")
    
    df = df.drop_duplicates().copy()
    
    print(f"   ➤ Registros después: {df.shape[0]}")
    return df


# =============================================================
# 🧩 Imputación de nulos en variables categóricas
# -------------------------------------------------------------
# ➤ Imputa los valores nulos en variables categóricas según
#    una lógica definida (por ejemplo, 'OTROS' para 'empleo').
# ➤ La imputación se realiza sobre el DataFrame `cat`.
# =============================================================
def imputar_nulos_categoricas(cat: pd.DataFrame) -> pd.DataFrame:
    cat = cat.copy()
    if 'empleo' in cat.columns:
        cat['empleo'] = cat['empleo'].fillna('OTROS')
    return cat


# =============================================================
# 📉 Imputación de nulos en variables numéricas
# -------------------------------------------------------------
# ➤ Aplica imputaciones personalizadas usando un diccionario
#   de lógica de negocio y estadísticas básicas.
# ➤ Cada variable tiene su propia estrategia definida.
# =============================================================
def imputar_nulos_numericas(num: pd.DataFrame) -> pd.DataFrame:
    num = num.copy()

    # Diccionario de imputación personalizada
    imputaciones = {
        'antiguedad_empleo': lambda x: x.fillna(x.median()),
        'dti': lambda x: x.fillna(x.median()),
        'num_hipotecas': lambda x: x.fillna(0),
        'porc_tarjetas_75p': lambda x: x.fillna(0),
        'porc_uso_revolving': lambda x: x.fillna(0),
        'num_meses_desde_ult_retraso': lambda x: x.fillna(0),
        'num_cancelaciones_12meses': lambda x: x.fillna(0),
        'num_lineas_credito': lambda x: x.fillna(0),
        'num_derogatorios': lambda x: x.fillna(0)
    }

    # Aplicar imputaciones si la columna está presente
    for col, func in imputaciones.items():
        if col in num.columns:
            num[col] = func(num[col])

    return num


# =============================================================
# 📉 Detección y agrupación de categorías poco representadas
# =============================================================

def detectar_atipicos_categoricos(df_cat: pd.DataFrame, umbral: float = 0.03) -> dict:
    """
    Devuelve un diccionario con categorías que tienen frecuencia relativa menor al umbral.
    """
    categorias_atipicas = {}
    for col in df_cat.columns:
        frecuencias = df_cat[col].value_counts(normalize=True)
        atipicos = frecuencias[frecuencias < umbral].index.tolist()
        if atipicos:
            categorias_atipicas[col] = atipicos
    return categorias_atipicas

def agrupar_categorias_poco_frecuentes(df_cat: pd.DataFrame, categorias_a_agrup: dict, etiqueta: str = "OTROS") -> pd.DataFrame:
    """
    Agrupa categorías poco frecuentes en cada variable del DataFrame bajo una etiqueta común.
    """
    df_cat = df_cat.copy()
    for col, categorias in categorias_a_agrup.items():
        df_cat[col] = df_cat[col].apply(lambda x: etiqueta if x in categorias else x)
    return df_cat


# =============================================================
# 🔍 Análisis de valores atípicos en variables categóricas
# =============================================================
def analizar_atipicos_categoricas(cat: pd.DataFrame, umbral_frecuencia: float = 0.03) -> None:
    """
    Analiza y muestra los valores atípicos en variables categóricas según un umbral de frecuencia relativa.

    Parámetros:
    ----------
    cat : pd.DataFrame
        Subconjunto del DataFrame original que contiene únicamente variables categóricas.
    umbral_frecuencia : float, opcional
        Umbral de frecuencia relativa para considerar una categoría como atípica (por defecto es 0.03).
    """
    print(f"\n📊 Análisis de valores atípicos en variables categóricas (frecuencia < {umbral_frecuencia * 100:.0f}%):")
    print(f"Variables analizadas: {', '.join(cat.columns)}")
    print("-" * 100)

    for col in cat.columns:
        print(f"\n📌 Variable: '{col}'")

        # Calcular frecuencias
        frecuencia_abs = cat[col].value_counts(dropna=False)
        frecuencia_rel = cat[col].value_counts(normalize=True, dropna=False)

        # Tabla completa
        resumen = pd.DataFrame({
            "valor": frecuencia_abs.index,
            "frecuencia": frecuencia_abs.values,
            "porcentaje": (frecuencia_rel * 100).round(2)
        }).reset_index(drop=True)

        # Detectar categorías atípicas
        categorias_atipicas = resumen[resumen["porcentaje"] < (umbral_frecuencia * 100)]

        print(f"- Total de categorías: {len(resumen)}")
        if not categorias_atipicas.empty:
            print(f"- Nº de categorías atípicas detectadas: {len(categorias_atipicas)}")
        else:
            print("- No se han detectado categorías atípicas en esta variable.")

        # Mostrar resumen completo
        print("\n📋 Tabla completa de frecuencias:")
        display(resumen)

        # Conclusión por variable
        print("📝 Conclusión:")
        match col:
            case 'empleo':
                print("• Presenta miles de categorías con muy baja frecuencia. Se sugiere agrupar en 'OTROS'.")
            case 'ingresos_verificados':
                print("• Tiene solo 3 categorías frecuentes. No requiere transformación.")
            case 'rating':
                print("• Las categorías 'F' y 'G' son poco frecuentes. Podrían agruparse como 'rating_bajo'.")
            case 'vivienda':
                print("• Tiene una categoría poco común ('OTROS'). Puede evaluarse su fusión con otra categoría.")
            case 'finalidad':
                print("• Presenta variedad moderada. Se evaluará si es necesario agrupar según frecuencia o semántica.")
            case 'estado':
                print("• Variable objetivo (target). No se modifica en esta etapa.")
            case _:
                print("• No se ha definido un criterio específico para esta variable.")

        print("\n" + "-" * 100)

    # NOTA FINAL
    print("\n================================================================================================")
    print("📌 El tratamiento de estas categorías atípicas se realizará en la fase de *Feature Engineering*.")
    print("================================================================================================")



# =============================================================
# 🔍 Análisis de valores atípicos en variables numericas
# =============================================================
def analizar_outliers_numericos(df: pd.DataFrame, num_desv_tip: int = 3) -> None:
    """
    Analiza y reporta los valores atípicos en variables numéricas del DataFrame.
    Se consideran atípicos los valores fuera de ±num_desv_tip desviaciones típicas.

    Args:
        df (pd.DataFrame): DataFrame con variables numéricas.
        num_desv_tip (int): Número de desviaciones típicas para considerar un valor como atípico.
    """
    print(f"\n\u27a4 Análisis de outliers usando ±{num_desv_tip} desviaciones típicas")
    print(f"Variables analizadas: {', '.join(df.select_dtypes(include='number').columns)}")
    print("-" * 100)

    total = df.shape[0]

    for col in df.select_dtypes(include='number').columns:
        media = df[col].mean()
        std = df[col].std()
        lim_inf = media - num_desv_tip * std
        lim_sup = media + num_desv_tip * std

        valor_max = df[col].max()
        valor_min = df[col].min()

        mask_valida = df[col].between(lim_inf, lim_sup)
        fuera_rango = (~mask_valida).sum()
        valor_max_valido = df.loc[mask_valida, col].max()

        print(f"\n📈 Variable: '{col}'")
        print(f"- Media: {media:,.2f}")
        print(f"- Desviación típica: {std:,.2f}")
        print(f"- Límite inferior: {lim_inf:,.2f}")
        print(f"- Límite superior: {lim_sup:,.2f}")
        print(f"- Valor mínimo: {valor_min:,.2f}")
        print(f"- Valor máximo: {valor_max:,.2f}")
        print(f"- Valor máximo válido: {valor_max_valido:,.2f}")
        print(f"- Registros fuera de rango: {fuera_rango:,} ({(fuera_rango / total) * 100:.2f}%)")
        print("-" * 100)

    print("\n\u2b50 RECOMENDACIONES GENERALES:")
    print("\u2022 Por defecto se recomienda usar ±3 desviaciones típicas para detectar outliers.")
    print("\u2022 Este criterio es apropiado para distribuciones normales.")
    print("\n\u26a0 Para distribuciones no normales, considerar:")
    print("  - IQR: valores fuera de Q1-1.5×IQR y Q3+1.5×IQR.")
    print("  - Boxplot, z-score robusto, percentiles.")
    print("\n📄 Recomendación para este proyecto:")
    print("  1. Empezar con ±3σ como criterio.")
    print("  2. Complementar con visualizaciones en el EDA (boxplots, histogramas).")