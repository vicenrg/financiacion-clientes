# 🧠 Estructura Técnica del Proyecto

Este documento detalla la arquitectura modular del proyecto de análisis de riesgo para financiación a clientes. La estructura está diseñada para ser escalable, mantenible y fácil de comprender por futuros desarrolladores o revisores académicos.

---

## 📦 Estructura General

```
Financiacion Clientes/
│
├── Documentos/           → Documentación técnica y entorno
├── Datos/                → Organización por tipo: raw, processed, validación
├── Notebooks/            → Desarrollo iterativo en Jupyter
├── src/                  → Código modular: ETL, EDA, modelado, utils
├── Modelos/              → Modelos entrenados y serializados
├── Resultados/           → Métricas, visualizaciones y logs
├── Dashboard/            → Visualización interactiva (Streamlit)
├── Imagenes/             → Recursos gráficos
├── main.py               → Pipeline principal
└── .gitignore
```

---

## 📁 src/ - Código Modular

- `setup/`: carga y verificación de estructura de datos
- `limpieza/`: funciones para limpieza de variables, nulos y duplicados
- `eda/`: visualizaciones y análisis exploratorio
- `transformacion/`: ingeniería de variables
- `modelado/`: entrenamiento y evaluación de modelos
- `utils/`: utilidades generales (rutas, guardado, logs)

---

## 📁 Notebooks/

- `01_Setup.ipynb`: carga y exploración inicial
- `02_Limpieza.ipynb`: limpieza profunda
- `03_EDA.ipynb`: análisis de variables
- `04_Transformacion.ipynb`: feature engineering
- `05_Modeling.ipynb`: modelado y validación

---

## 🚀 Flujo de trabajo

1. Carga y validación inicial
2. Limpieza y preprocesamiento
3. EDA y visualización
4. Transformación de variables
5. Modelado
6. Cálculo de pricing ajustado al riesgo
7. App interactiva (opcional)

---
