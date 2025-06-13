# 📈 Modelado de Riesgo e Interés Personalizado

Este documento resume el enfoque técnico utilizado para modelar la probabilidad de impago (PD) y calcular el tipo de interés mínimo ajustado al riesgo.

---

## 🧠 Modelos Utilizados

- **Regresión Logística**: modelo base, interpretable
- **Árbol de Decisión**: validación alternativa
- (Opcional) Random Forest para benchmark

---

## 🎯 Variable Objetivo

`estado`: indica si el préstamo fue impagado (`1`) o no (`0`).

---

## 🔍 Variables Predictoras

- `edad`
- `ingresos`
- `importe_prestamo`
- `duracion_meses`
- `tipo_contrato`

Solo se utilizan variables disponibles para una pyme.

---

## 📊 Evaluación del Modelo

- Métrica principal: **AUC**
- Visualización: curva ROC
- Umbral ajustable para sensibilidad/especificidad

---

## 💰 Cálculo del Interés Ajustado

Fórmula:
```
interes_minimo = tipo_base + (coef_riesgo * PD)
```

Ejemplo:
- Tipo base: 5%
- Coeficiente de riesgo: 10%
- PD estimada: 0.30
- Resultado: 5% + (10% * 0.30) = 8%

---

## 📁 Resultados exportados

- `modelo_logistico.pkl`
- `probabilidades.csv`
- `roc_curve.png`

---
