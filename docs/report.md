# 📊 Simulador de Financiación para PYMEs

Este proyecto es una aplicación interactiva desarrollada con **Streamlit** que permite a pequeñas empresas y autónomos estimar:

- La **probabilidad de impago (PD)** de un cliente.
- El **interés mínimo recomendado** en función del riesgo.
- La **cuota mensual estimada** según el perfil ingresado.

---

## 🎯 Objetivo

Facilitar a PYMEs una herramienta accesible para calcular un tipo de interés personalizado, usando modelos de machine learning entrenados sobre datos históricos de financiación. 

Ideal para inmobiliarias, concesionarios, clínicas, academias o cualquier pyme que ofrezca financiación directa.

---

## 🧠 Modelo

- Modelo de clasificación: **HistGradientBoostingClassifier** (`sklearn`)
- Variables de entrada reducidas y prácticas para pymes:
  - Ingresos mensuales
  - Importe solicitado
  - Duración (36 o 60 meses)
  - Antigüedad en el empleo
  - Rating crediticio (0–10)
  - Finalidad del préstamo
  - Categoría profesional
- Escalado y preprocesamiento embebido en el modelo (`modelo_hist_gradient_boosting_ligero.pkl`)

---

## 🚀 Funcionalidades

- Formulario en la barra lateral con variables clave.
- Visualización de resultados mediante **velocímetros interactivos**:
  - **PD (%)**
  - **Interés sugerido (%)**
  - **Cuota mensual estimada (€)**
- Cálculo adicional de:
  - **Pérdida esperada**
  - **Comisión sugerida**
- Interfaz clara y usable para usuarios no técnicos.

---

## 📦 Requisitos

Crea un entorno virtual e instala las dependencias:

```bash
conda env create -f financiacion-clientes.yml
```

Ejemplo mínimo de `requirements.txt`:

```text
streamlit
streamlit-echarts
scikit-learn
pandas
numpy==1.24.4
joblib
```

> ⚠️ Asegúrate de usar `numpy<2.0` para evitar conflictos con `pyarrow` y `streamlit-echarts`.

---

## ▶️ Cómo ejecutar la app

Desde el terminal:

```bash
cd outputs/dashboard
streamlit run app_ligero.py
```

---

## 📂 Estructura del proyecto

```
Financiacion Clientes/
│
├── outputs/
│   ├── data/
│   │   └── df_modelo.csv
│   ├── models/
│   │   ├── modelo_hist_gradient_boosting_ligero.pkl
│   │   └── scaler.pkl
│   └── dashboard/
│       ├── app_ligero.py
│       └── risk_score.webp
│
├── notebooks/
│   └── 05_modeling.ipynb
└── README.md
```

---

## 📌 Notas

- El modelo fue entrenado para evitar variables de difícil acceso como historial crediticio completo o score externo.
- El campo `dti` ha sido eliminado de la interfaz, pero internamente se fija como `0.0` para compatibilidad.

---

## 🧑‍💼 Autor

Desarrollado como parte del proyecto final de Máster en Data Science.  
Autor: **Vicente Rueda**

---

## 📃 Licencia

Uso académico y profesional bajo acuerdo con el autor.  
Contacto para personalización o despliegue empresarial.