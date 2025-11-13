# 📋 GUÍA: DÓNDE VA CADA CÓDIGO E IMAGEN DEL LABORATORIO DE FARADAY

Esta guía te indica **exactamente** qué código y qué imágenes debes adjuntar para cada pregunta del laboratorio.

---

## 📌 PREGUNTA 1: Determinar la velocidad angular (rad/s)

### 📁 Archivos a adjuntar:

#### **Código Python:**
```
ajuste_curva_B.py
```
Este código:
- Lee los datos experimentales de `datafinal.txt`
- Realiza el ajuste de curva senoidal: `B_fit(t) = A·sin(B·t + C) + D`
- Calcula la velocidad angular **ω = 54.314 rad/s** (parámetro B del ajuste)
- Genera las gráficas del ajuste

#### **Imágenes a adjuntar:**
1. **`ajuste_curva_B_simple.png`** - Gráfica del ajuste de curva con la ecuación y parámetros
2. **`ajuste_curva_B_vs_t.png`** - Gráfica completa con datos experimentales, ajuste y residuos

---

## 📌 PREGUNTA 2: Calcular corriente inducida pico (I_pico) usando Ley de Faraday

### 📁 Archivos a adjuntar:

#### **Código Python:**
```
calcular_corriente_pico.py
```
Este código:
- Calcula `B_pico = (B_max - B_min) / 2`
- Calcula `I_pico_exp = (I_max - I_min) / 2`
- Usa la Ley de Faraday con `Φ(t) = B_pico · A · cos(ωt)` para calcular `I_pico_teórico`
- Compara los valores experimental vs teórico

#### **Imagen a adjuntar:**
1. **`calculo_corriente_pico.png`** - Visualización completa con:
   - Panel superior: Resumen de cálculos paso a paso
   - Panel medio izquierdo: Gráfica de B(t) mostrando B_max, B_min y B_pico
   - Panel medio derecho: Gráfica de I(t) mostrando I_max, I_min e I_pico
   - Panel inferior: Comparación entre I_pico experimental y teórico

---

## 📌 PREGUNTA 3: Graficar B_exp vs t e I_exp vs t

### 📁 Archivos a adjuntar:

#### **Código Python:**
```
plot_experimental_data.py
```
Este código:
- Lee los datos experimentales de `datafinal.txt`
- Filtra datos entre 3.0 y 4.0 segundos
- Genera dos gráficas: B_exp(t) e I_exp(t)

#### **Imagen a adjuntar:**
1. **`graficas_experimentales.png`** - Dos subgráficas:
   - Gráfica superior: Campo Magnético Experimental vs Tiempo
   - Gráfica inferior: Corriente Experimental vs Tiempo

---

## 📌 PREGUNTA 4: Ajuste de curva de B_exp vs t

### 📁 Archivos a adjuntar:

#### **Código Python:**
```
ajuste_curva_B.py
```
(El mismo código de la Pregunta 1)

Este código:
- Realiza el ajuste de curva senoidal: `B_fit(t) = A·sin(B·t + C) + D`
- Muestra la ecuación del ajuste con valores numéricos
- Calcula R² para evaluar la bondad del ajuste

#### **Imágenes a adjuntar:**
1. **`ajuste_curva_B_simple.png`** - Gráfica del ajuste con la ecuación completa
2. **`ajuste_curva_B_vs_t.png`** - Gráfica con ajuste y residuos

**Ecuación obtenida del ajuste:**
```
B_fit(t) = 0.9749·sin(54.314·t + 6.2783) + 0.2012  [mT]
```

---

## 📌 PREGUNTA 5: Usar Ley de Faraday para hallar I(t) y graficar I(t) vs I_exp(t)

### 📁 Archivos a adjuntar:

#### **Código Python:**
```
calcular_corriente_faraday.py
```
Este código:
- Usa el ajuste B_fit(t) obtenido anteriormente
- Calcula la derivada: `dB_fit/dt = A·B·cos(B·t + C)`
- Aplica la Ley de Faraday: `ε_ind = -N·A·(dB/dt)`
- Calcula la corriente: `I(t) = ε_ind / R`
- Grafica I(t) teórico vs I_exp experimental

#### **Imágenes a adjuntar (puedes elegir una o varias):**

1. **`I_vs_I_exp_faraday.png`** ⭐ **(RECOMENDADA para el informe)**
   - Gráfica simple y clara comparando I_exp(t) e I(t) teórico
   - Incluye cuadro con ecuaciones y parámetros

2. **`corriente_faraday_comparacion.png`**
   - Dos subgráficas:
     - Superior: Comparación I_exp vs I teórico
     - Inferior: Campo magnético B_fit(t)

3. **`analisis_faraday_completo.png`**
   - Tres subgráficas:
     - (a) Corriente experimental vs teórica
     - (b) Campo magnético ajustado
     - (c) Derivada temporal dB/dt

---

## 📊 RESUMEN: TABLA DE ARCHIVOS POR PREGUNTA

| Pregunta | Código Python | Imágenes |
|----------|--------------|----------|
| **1. Velocidad angular** | `ajuste_curva_B.py` | `ajuste_curva_B_simple.png`<br>`ajuste_curva_B_vs_t.png` |
| **2. I_pico (Faraday)** | `calcular_corriente_pico.py` | `calculo_corriente_pico.png` |
| **3. Graficar B_exp e I_exp** | `plot_experimental_data.py` | `graficas_experimentales.png` |
| **4. Ajuste de curva B** | `ajuste_curva_B.py` | `ajuste_curva_B_simple.png`<br>`ajuste_curva_B_vs_t.png` |
| **5. I(t) con Faraday** | `calcular_corriente_faraday.py` | `I_vs_I_exp_faraday.png` ⭐<br>`corriente_faraday_comparacion.png`<br>`analisis_faraday_completo.png` |

---

## 🔄 CÓMO EJECUTAR LOS CÓDIGOS

Para regenerar las imágenes, ejecuta los scripts en este orden:

```bash
# 1. Graficar datos experimentales (Pregunta 3)
python plot_experimental_data.py

# 2. Ajuste de curva del campo magnético (Preguntas 1 y 4)
python ajuste_curva_B.py

# 3. Cálculo de corriente pico (Pregunta 2)
python calcular_corriente_pico.py

# 4. Cálculo de I(t) con Ley de Faraday (Pregunta 5)
python calcular_corriente_faraday.py
```

---

## 📝 NOTAS IMPORTANTES

### ⚠️ Dependencias requeridas:
```bash
pip install numpy matplotlib scipy
```

### 📂 Archivo de datos:
Todos los scripts requieren el archivo:
```
datafinal.txt
```

### ✅ Respuestas escritas:
Las respuestas detalladas a todas las preguntas están en:
```
RESPUESTAS_LABORATORIO.md
```

---

## 🎯 RECOMENDACIONES PARA EL INFORME

### Para cada pregunta, adjunta:

1. **Captura del código** (puedes copiar el archivo .py completo o tomar screenshot)
2. **Captura de la salida del programa** (texto que imprime en consola)
3. **Imagen(es) generada(s)** (archivos .png indicados arriba)

### Formato sugerido por pregunta:

```markdown
## Pregunta X: [Título]

### Código utilizado:
[Captura o código completo del archivo .py]

### Resultados:
[Captura de la salida en consola]

### Gráfica:
[Imagen PNG generada]

### Explicación:
[Tu interpretación de los resultados]
```

---

## ✨ TIPS FINALES

- **Las imágenes están en alta resolución (300 DPI)** - ideales para impresión
- **Todos los códigos incluyen comentarios explicativos** - puedes mostrarlos completos
- **Las gráficas incluyen ecuaciones y parámetros** - no necesitas escribirlos aparte
- **Los valores numéricos son consistentes entre todos los scripts** - todo está bien integrado

---

¡Éxito con tu informe de laboratorio! 🚀
