
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# =============================================================
# 🎯 Función: crear_variable_objetivo
# -------------------------------------------------------------
# ➤ Crea la variable binaria 'target' a partir de 'estado'
# ➤ Devuelve el DataFrame actualizado y la serie objetivo
# ➤ Incluye explicación detallada de qué categorías se consideran impago
# =============================================================
def crear_variable_objetivo(df: pd.DataFrame, col_estado: str = "estado") -> tuple:
    """
    Crea una variable binaria 'target' a partir de la columna 'estado'.

    Mapeo:
    - 1 = impago (alto riesgo): incluye casos como 'Charged Off', 'Default', etc.
    - 0 = no impago (cliente pagador): el resto de categorías.

    Args:
        df (pd.DataFrame): DataFrame de entrada con la columna 'estado'
        col_estado (str): Nombre de la columna que contiene el estado del préstamo

    Returns:
        df_actualizado (pd.DataFrame): DataFrame sin la columna original y con 'target'
        target (pd.Series): Serie con la variable objetivo binaria
    """

    df = df.copy()

    # Valores considerados como impago
    valores_impago = [
        "Charged Off",
        "Does not meet the credit policy. Status:Charged Off",
        "Default"
    ]

    # Mostrar resumen de categorías
    print("\n📊 Categorías únicas en columna de estado:")
    print(df[col_estado].value_counts(dropna=False))

    # Mostrar explicación del criterio
    print("\n📌 Categorización de 'estado' → 'target':")
    print("➡ Se asigna target = 1 (impago) a:")
    for v in valores_impago:
        print(f"  - {v}")
    print("➡ Todas las demás se consideran NO impago (target = 0)")

    # Crear columna target
    df["target"] = np.where(df[col_estado].isin(valores_impago), 1, 0)

    # Verificación de resultados
    print("\n✅ Distribución de 'target':")
    print(df["target"].value_counts().sort_index())
    print("Valores nulos:", df["target"].isna().sum())
    print(f"📌 Porcentaje de impagos: {df['target'].mean() * 100:.2f}%")

    # Eliminar columna original
    df.drop(columns=col_estado, inplace=True)

    # Mostrar el DataFrame resultante si se indica
    print("\n📋 Vista previa del DataFrame actualizado (sin 'estado', con 'target'):")
    display(df)

    return df, df["target"]


# =============================================================
# 🎯 Función: agrupar_categorias
# -------------------------------------------------------------
# ➤ Verifica si hay valores nulos en la variable de entrada
# ➤ Agrupa categorías con frecuencia < criterio (%) bajo 'OTROS'
# ➤ Muestra gráfico de frecuencias absolutas y relativas
# ➤ Permite usar 'criterio' en porcentaje, más intuitivo (ej: 0.5 = 0.5%)
# =============================================================
def agrupar_categorias(variable: pd.Series, criterio: float = 5.0) -> pd.Series:
    """
    Agrupa las categorías poco frecuentes de una variable categórica bajo la etiqueta 'OTROS',
    y muestra un gráfico de barras con frecuencias absolutas y relativas.

    Parámetros:
    -----------
    variable : pd.Series
        Variable categórica a procesar.
    criterio : float
        Umbral mínimo de frecuencia en porcentaje. 
        Ej: criterio=0.5 agrupa las categorías con <0.5% frecuencia.
    
    Retorna:
    --------
    pd.Series
        Variable transformada con categorías raras agrupadas.
    """
    if variable.isnull().any():
        raise ValueError("La variable contiene valores nulos. Imputar antes de agrupar categorías.")
    else:
        print("✅ Valores nulos: 0")

    # Convertir criterio de porcentaje a proporción
    criterio_proporcion = criterio / 100

    frecuencias = variable.value_counts(normalize=True)
    categorias_raras = frecuencias[frecuencias < criterio_proporcion].index
    variable_agrupada = np.where(variable.isin(categorias_raras), 'OTROS', variable)
    variable_agrupada = pd.Series(variable_agrupada, index=variable.index)

    # Crear nuevo conteo tras agrupar
    conteo_abs = variable_agrupada.value_counts()
    conteo_rel = variable_agrupada.value_counts(normalize=True) * 100

    # Gráfico
    plt.figure(figsize=(10, 5))
    barras = plt.bar(conteo_abs.index, conteo_rel, alpha=0.7)

    # Etiquetas con valor absoluto y porcentaje
    for i, categoria in enumerate(conteo_abs.index):
        valor_abs = conteo_abs[categoria]
        valor_pct = conteo_rel[categoria]
        plt.text(i, valor_pct + 0.5, f"{valor_abs}\n({valor_pct:.1f}%)", ha='center', va='bottom', fontsize=9)

    plt.title(f"Distribución de categorías en variable '{variable.name}'", fontsize=14)
    plt.xlabel("Categorías")
    plt.ylabel("Frecuencia relativa (%)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.show()

    return variable_agrupada



# =============================================================
# 🎯 Función: reagrupar_categorias_existente
# -------------------------------------------------------------
# ➤ Verifica si hay valores nulos en la variable de entrada
# ➤ Agrupa categorías con frecuencia < criterio (%) dentro de una categoría ya existente
# ➤ Lanza error si la categoría destino no existe
# ➤ Muestra gráfico de barras con frecuencias absolutas y relativas tras la reagrupación
# =============================================================
def reagrupar_categorias_existente(variable: pd.Series, criterio: float, categoria_objetivo: str) -> pd.Series:
    """
    Reasigna las categorías con frecuencia menor a un umbral a una categoría ya existente.
    Muestra un gráfico de barras tras la transformación.

    Parámetros:
    -----------
    variable : pd.Series
        Variable categórica a procesar.
    criterio : float
        Umbral mínimo de frecuencia en porcentaje. 
        Ej: criterio=1 agrupa las categorías con <1% frecuencia.
    categoria_objetivo : str
        Categoría existente a la que se reasignarán las categorías poco frecuentes.

    Retorna:
    --------
    pd.Series
        Variable transformada con categorías raras reasignadas a la categoría objetivo.
    """
    if variable.isnull().any():
        raise ValueError("❌ La variable contiene valores nulos. Imputar antes de reagrupar.")
    else:
        print("✅ Valores nulos: 0")

    if categoria_objetivo not in variable.unique():
        raise ValueError(f"❌ La categoría objetivo '{categoria_objetivo}' no existe en la variable.")

    # Convertir criterio de porcentaje a proporción
    criterio_proporcion = criterio / 100

    # Identificar categorías poco frecuentes
    frecuencias = variable.value_counts(normalize=True)
    categorias_a_reagrupar = frecuencias[frecuencias < criterio_proporcion].index

    # Reagrupar en la categoría objetivo
    variable_reagrupada = variable.apply(lambda x: categoria_objetivo if x in categorias_a_reagrupar else x)
    variable_reagrupada = pd.Series(variable_reagrupada, index=variable.index)

    # Nuevo conteo
    conteo_abs = variable_reagrupada.value_counts()
    conteo_rel = variable_reagrupada.value_counts(normalize=True) * 100

    # Gráfico
    plt.figure(figsize=(10, 5))
    barras = plt.bar(conteo_abs.index, conteo_rel, alpha=0.7)

    for i, categoria in enumerate(conteo_abs.index):
        valor_abs = conteo_abs[categoria]
        valor_pct = conteo_rel[categoria]
        plt.text(i, valor_pct + 0.5, f"{valor_abs}\n({valor_pct:.1f}%)", ha='center', va='bottom', fontsize=9)

    plt.title(f"Distribución tras reagrupar en '{categoria_objetivo}'", fontsize=14)
    plt.xlabel("Categorías")
    plt.ylabel("Frecuencia relativa (%)")
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

    return variable_reagrupada



# =============================================================
# 🔷 Función: codificar_one_hot
# -------------------------------------------------------------
# ➤ Aplica One-Hot Encoding a variables nominales en el DataFrame `cat`
# ➤ Usa scikit-learn con drop=None (conserva todas las categorías)
# ➤ Compatible con regresión logística regularizada y modelos de árboles
# ➤ handle_unknown='ignore' evita errores si aparecen nuevas categorías en producción
# =============================================================

from sklearn.preprocessing import OneHotEncoder

def codificar_one_hot(cat: pd.DataFrame, variables: list) -> pd.DataFrame:
    """
    Aplica One-Hot Encoding a variables nominales sin eliminar columnas dummy.

    Args:
        cat (pd.DataFrame): DataFrame con variables categóricas y target.
        variables (list): Lista de columnas nominales a codificar.

    Returns:
        pd.DataFrame: DataFrame con variables codificadas y originales eliminadas.
    """
    cat = cat.copy()

    # Configurar codificador con scikit-learn
    ohe = OneHotEncoder(drop=None, handle_unknown='ignore', sparse_output=False)

    # Transformar y obtener nombres de columnas codificadas
    codificado = ohe.fit_transform(cat[variables])
    columnas_codificadas = ohe.get_feature_names_out(variables)

    # Crear DataFrame de las columnas codificadas
    df_codificado = pd.DataFrame(codificado, columns=columnas_codificadas, index=cat.index)

    # Reemplazar columnas originales por las codificadas
    cat.drop(columns=variables, inplace=True)
    cat = pd.concat([cat, df_codificado], axis=1)

    return cat



# =============================================================
# 🟢 Función: codificar_ordinal
# -------------------------------------------------------------
# ➤ Aplica codificación ordinal con scikit-learn a múltiples variables
# ➤ Usa el orden definido por el usuario (una lista por variable)
# ➤ Elimina las columnas originales y añade las columnas codificadas
# =============================================================

from sklearn.preprocessing import OrdinalEncoder

def codificar_ordinal(cat: pd.DataFrame, variables: list, categorias_ordenadas: list) -> pd.DataFrame:
    """
    Codifica múltiples variables ordinales en el DataFrame `cat` con orden explícito.

    Args:
        cat (pd.DataFrame): DataFrame con variables categóricas y target.
        variables (list): Lista de columnas ordinales a codificar.
        categorias_ordenadas (list): Lista de listas con el orden por variable.

    Returns:
        pd.DataFrame: DataFrame actualizado con columnas ordinales codificadas.
    """
    cat = cat.copy()

    # Validación
    if len(variables) != len(categorias_ordenadas):
        raise ValueError("❌ La cantidad de variables no coincide con la cantidad de listas de orden.")

    # Codificador ordinal con orden definido
    oe = OrdinalEncoder(categories=categorias_ordenadas)
    codificado = oe.fit_transform(cat[variables])

    columnas_codificadas = [f"{var}_ord" for var in variables]
    df_codificado = pd.DataFrame(codificado, columns=columnas_codificadas, index=cat.index)

    # Eliminar originales y añadir codificadas
    cat.drop(columns=variables, inplace=True)
    cat = pd.concat([cat, df_codificado], axis=1)

    return cat



# =============================================================
# ⚖️ Función: escalar_variables_numericas
# -------------------------------------------------------------
# ➤ Aplica MinMaxScaler solo a las variables seleccionadas
# ➤ Ignora las que no existan en el DataFrame
# ➤ Devuelve el DataFrame actualizado
# =============================================================

from sklearn.preprocessing import MinMaxScaler

def escalar_variables_numericas(num: pd.DataFrame, variables_a_escalar: list) -> pd.DataFrame:
    """
    Escala las variables numéricas seleccionadas usando MinMaxScaler.

    Args:
        num (pd.DataFrame): DataFrame numérico original
        variables_a_escalar (list): Lista de columnas a escalar

    Returns:
        pd.DataFrame: DataFrame con variables escaladas
    """
    num = num.copy()
    scaler = MinMaxScaler()

    columnas_presentes = [col for col in variables_a_escalar if col in num.columns]
    num[columnas_presentes] = scaler.fit_transform(num[columnas_presentes])

    return num


