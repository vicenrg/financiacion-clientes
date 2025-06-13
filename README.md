# 💰 Sistema de Pricing Ajustado al Riesgo para PYMEs

Este proyecto desarrolla una herramienta que permite a pequeñas y medianas empresas calcular un tipo de interés personalizado en función del riesgo de impago del cliente. Se trata de un MVP funcional creado como entrega final para un Máster en Data Science.

---

## 🎯 Objetivo del Proyecto

Ofrecer una alternativa práctica al scoring bancario tradicional mediante:

- Modelado de la **probabilidad de impago (PD)** con datos accesibles por una pyme.
- Cálculo del **interés mínimo recomendado** ajustado al riesgo individual.
- Interfaz interactiva (opcional) para simular distintos perfiles de cliente.

---

## 📁 Estructura del Proyecto

```bash

📦 Financiacion Clientes/                      # Carpeta raíz con el nombre del proyecto
│
├── config/                            # Configuración general del proyecto
│   └── config.yaml                    # Parámetros como rutas, variables, hiperparámetros, etc.
│
├── data/                              # Conjunto de datos organizados por etapa
│   ├── raw/                           # Datos originales sin procesar
│   ├── processed/                     # Datos limpios y listos para análisis/modelo
│   ├── validation/                    # Datos de validación externos o separados
│   └── cache/                         # Transformaciones intermedias, temporales
│
├── docs/                              # Documentación técnica y de decisiones
│   ├── architecture.md                # Descripción de la arquitectura del proyecto
│   ├── decisions.md                   # Registro de decisiones tomadas
│   └── report.md                      # Informe final del proyecto
│
├── notebooks/                         # Jupyter Notebooks para desarrollo y pruebas
│   ├── 01_data.ipynb                  # Carga inicial de datos
│   ├── 02_cleaning.ipynb              # Limpieza y tratamiento de valores anómalos
│   ├── 03_eda.ipynb                   # Análisis exploratorio de datos
│   ├── 04_transformation.ipynb        # Generación y transformación de variables
│   └── 05_modeling.ipynb              # Entrenamiento y evaluación de modelos
│
├── outputs/                           # Resultados generados por el modelo
│   ├── models/                        # Archivos de modelos entrenados (.pkl, .joblib, etc.)
│   ├── metrics/                       # Métricas y scores de evaluación
│   ├── figures/                       # Gráficos, visualizaciones exportadas
│   └── dashboard/                     # Informes visuales (Streamlit, Power BI, etc.)
│
├── src/                               # Código fuente del proyecto, modular y reutilizable
│   ├── __init__.py                    # Define src como paquete Python
│   ├── data.py                        # Funciones para cargar datos
│   ├── cleaning.py                    # Funciones de limpieza de datos
│   ├── eda.py                         # Funciones de análisis y visualización
│   ├── transformation.py              # Funciones de transformación y selección de variables
│   ├── modeling.py                    # Entrenamiento, evaluación y serialización de modelos
│   └── utils.py                       # Funciones auxiliares (logs, métricas, formateo, etc.)
│
├── main.py                            # Script principal que ejecuta el pipeline completo
├── README.md                          # Descripción general y guía del proyecto
└── .gitignore                         # Archivos y carpetas a excluir del control de versiones
```

---

## 📁 src/ - Código Fuente Modular

Estructura principal del código organizado por responsabilidades:

### 📁 setup/
- **`carga_datos.py`**: funciones para cargar y guardar datasets (`cargar_csv`, `guardar_csv`).
- **(rutas.py)**: [ELIMINADO] reemplazado por el uso directo de `Path`.

### 📁 limpieza/
- **`limpieza_general.py`**: funciones de limpieza como manejo de nulos, duplicados, outliers, etc.

### 📁 eda/
- **`graficos.py`**: funciones para visualizaciones estéticas y reutilizables (Seaborn, Matplotlib).
- **`estadisticas.py`**: métricas descriptivas, correlaciones, agrupaciones estadísticas.

### 📁 transformacion/
- **`engineering.py`**: creación de variables, normalización, codificación, binning, etc.

### 📁 modelado/
- **`entrenamiento.py`**: entrenamiento de modelos de ML (sklearn, XGBoost...).
- **`evaluacion.py`**: evaluación de modelos con métricas, validaciones cruzadas, ROC, etc.

### 📁 utils/
- **`helpers.py`**: funciones auxiliares genéricas: mostrar líneas de un archivo, verificar dimensionalidad, cargar/guardar CSV.

---

## 📁 Notebooks/

Estructura y diseño del proceso

- **`01_Setup.ipynb`**: carga inicial de datos, verificación de estructura y guardado.
- **`02_Limpieza.ipynb`**: limpieza de datos y validaciones.
- **`03_EDA.ipynb`**: análisis exploratorio de variables y patrones.
- **`04_Transformacion.ipynb`**: generación de nuevas variables para modelado.
- **`05_modeling.ipynb`**: entrenamiento, evaluación y serialización de modelos.

---

## 📁 Datos/

Organización clara por tipo y uso:

- **Originales/**: datos sin procesar (raw)
- **Validacion/**: conjunto separado para evaluación del modelo
- **Trabajo/**: datos procesados para modelado
- **Caches/**: transformaciones temporales, preprocesamiento intermedio

---

## 🚀 Flujo de Ejecución Típico

1. **01_Setup.ipynb**:
    - Muestra líneas del CSV
    - Carga datos
    - Verifica calidad y dimensionalidad
    - Guarda `df_trabajo.csv`

2. **02_Limpieza.ipynb**:
    - Carga datos de trabajo
    - Aplica funciones de limpieza
    - Guarda datos limpios

3. **03_EDA.ipynb**:
    - Visualiza variables numéricas/categóricas
    - Obtiene estadísticas agrupadas

4. **04_Transformacion.ipynb**:
    - Genera nuevas variables
    - Prepara datos para modelado

5. **main.py**:
    - Ejecuta el pipeline completo en orden si se desea automatizar

---

## ✅ Buenas prácticas aplicadas

- Modularización por fase
- Uso de `Path` en lugar de rutas hardcodeadas
- Centralización de utilidades en `helpers.py`
- Separación clara de datos, resultados, modelos y dashboards

---

## ⚙️ Instalación y Ejecución

1. Clonar el repositorio:

```bash
git clone https://github.com/tuusuario/financiacion-clientes.git
cd financiacion-clientes
```

2. Crear entorno:

```bash
conda env create -f docs/financiacion-clientes.yml
conda activate financiacion-clientes
```

---

## 🧪 Tecnologías utilizadas

- Python 3.11+

'''bash
conda update -n base -c defaults conda -y
conda clean -y --all
ENTORNO="data11"
conda deactivate 
conda env remove -y -n $ENTORNO
conda create -y -n $ENTORNO python numpy pandas matplotlib seaborn statsmodels scikit-learn scipy sqlalchemy jupyter jupyter_client xgboost
conda activate $ENTORNO
conda install -y -c conda-forge plotly pyjanitor scikit-plot yellowbrick imbalanced-learn jupyter_contrib_nbextensions cloudpickle streamlit
conda install -y -c districtdatalabs yellowbrick
pip install category_encoders streamlit-echarts pipreqs
python -m ipykernel install --sys-prefix --name $ENTORNO --display-name "Python ($ENTORNO)"
jupyter kernelspec list
'''

---

## 👤 Autor

**Vicente Rueda**  
Proyecto Final - Máster en Data Science  
[LinkedIn](https://linkedin.com/in/vicenterueda/)  
📧 [vicenteruedag@gmail.com](mailto:vicenteruedag@gmail.com)

---