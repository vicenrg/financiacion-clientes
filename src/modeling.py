# =============================================================
# 🎯 Función: dividir_dataset_escalonado
# -------------------------------------------------------------
# ➤ Divide un DataFrame en tres subconjuntos: train, test y validación
# ➤ Se reserva un % fijo para validación directamente del total
# ➤ Del resto, se divide en train y test según proporción deseada
# ➤ Mantiene la proporción de clases (stratify)
# ➤ Devuelve los 6 subconjuntos: X_train, X_test, X_val, y_train, y_test, y_val
# =============================================================

import pandas as pd
from sklearn.model_selection import train_test_split

def dividir_dataset_escalonado(
    df: pd.DataFrame,
    target: str,
    val_size: float = 0.2,
    test_size: float = 0.2,
    random_state: int = 42
):
    """
    Divide un dataset en entrenamiento, validación y test de forma escalonada.

    Args:
        df (pd.DataFrame): DataFrame original.
        target (str): Nombre de la variable objetivo.
        val_size (float): Proporción de validación (sobre el total).
        test_size (float): Proporción de test (sobre el restante tras validación).
        random_state (int): Semilla para reproducibilidad.

    Returns:
        Tuple: X_train, X_test, X_val, y_train, y_test, y_val
    """
    X = df.drop(columns=target)
    y = df[target]

    # 1. Separar validación
    X_temp, X_val, y_temp, y_val = train_test_split(
        X, y, test_size=val_size, random_state=random_state, stratify=y
    )

    # 2. Separar entrenamiento y test del resto
    X_train, X_test, y_train, y_test = train_test_split(
        X_temp, y_temp, test_size=test_size, random_state=random_state, stratify=y_temp
    )

    return X_train, X_test, X_val, y_train, y_test, y_val
