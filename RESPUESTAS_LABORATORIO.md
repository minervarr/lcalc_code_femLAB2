# Respuestas al Laboratorio de Ley de Faraday

## Pregunta 1: ¿Por qué al hacer girar el imán se produce una corriente?

**Respuesta (80 palabras):**

Al hacer girar el imán cerca de una bobina, el campo magnético que atraviesa la bobina varía con el tiempo, cambiando el flujo magnético Φ = B·A. Según la **Ley de Faraday**, esta variación temporal del flujo induce una fuerza electromotriz (FEM): **ε_ind = -N·dΦ/dt**. Esta FEM genera una corriente eléctrica en la bobina cuando el circuito está cerrado. El signo negativo (Ley de Lenz) indica que la corriente inducida se opone al cambio de flujo magnético que la produce.

### Diagrama Explicativo

```
    Imán giratorio          Bobina (N vueltas)
         N                    ╔═══╗
      ↻  │  ↺   →→→    →→→   ║   ║ → Circuito cerrado
         S                    ╚═══╝

    Φ(t) = B(t)·A  →  dΦ/dt ≠ 0  →  ε_ind = -N·dΦ/dt  →  I(t) = ε_ind/R
```

**Principio físico:**
- **Campo magnético variable** → **Flujo magnético variable** → **FEM inducida** → **Corriente eléctrica**

---

## Pregunta 2: Determine la velocidad angular (rad/s) usando los datos experimentales

### Cálculos Paso a Paso

#### **Paso 1: Ajuste de curva senoidal al campo magnético B(t)**

A partir de los datos experimentales de campo magnético vs tiempo (intervalo 3.0-4.0 s), se realizó un ajuste de curva usando el modelo:

```
B_fit(t) = A·sin(ω·t + C) + D
```

Donde:
- **A**: Amplitud del campo magnético
- **ω**: Frecuencia angular (velocidad angular) [rad/s]
- **C**: Fase inicial
- **D**: Offset (desplazamiento vertical)

#### **Paso 2: Resultados del ajuste de curva**

Usando el método de mínimos cuadrados no lineales (`scipy.optimize.curve_fit`), se obtuvieron los siguientes parámetros óptimos:

| Parámetro | Valor | Error | Descripción |
|-----------|-------|-------|-------------|
| **A** | 0.974862 mT | ± 0.005104 mT | Amplitud |
| **ω** | **54.314376 rad/s** | ± 0.017578 rad/s | **Frecuencia angular** |
| **C** | 6.278328 rad | ± 0.061743 rad | Fase inicial |
| **D** | 0.201169 mT | ± 0.003585 mT | Offset |

**Bondad del ajuste:**
- **R² = 0.9734** (ajuste excelente)
- **Error RMS = 0.113 mT**

#### **Paso 3: Ecuación final del campo magnético**

```
B_fit(t) = 0.9749·sin(54.314·t + 6.2783) + 0.2012  [mT]
```

#### **Paso 4: Cálculo de la frecuencia y período**

A partir de la velocidad angular **ω = 54.314376 rad/s**:

**Frecuencia:**
```
f = ω / (2π) = 54.314376 / (2π) = 8.6444 Hz
```

**Período:**
```
T = 1/f = 1/8.6444 = 0.1157 s
```

---

## Resultado Final

### **Velocidad Angular del Imán:**

```
ω = 54.314 ± 0.018 rad/s
```

**Equivalente a:**
- Frecuencia: **f = 8.64 Hz**
- Período: **T = 0.116 s**
- Revoluciones por minuto: **RPM = 518.5 rpm**

---

## Capturas de Pantalla

### 1. Ajuste de curva del campo magnético B(t)

![Ajuste de curva B(t)](ajuste_curva_B_simple.png)

*Figura 1: Ajuste senoidal del campo magnético experimental. El parámetro B = 54.314 rad/s representa la velocidad angular ω del imán.*

---

### 2. Código del ajuste de curva

```python
# Función del modelo senoidal
def modelo_senoidal(t, A, B, C, D):
    return A * np.sin(B * t + C) + D

# Realizar ajuste de curva
parametros_optimos, covarianza = curve_fit(
    modelo_senoidal,
    t_exp,
    B_exp,
    p0=parametros_iniciales,
    maxfev=10000
)

A_opt, B_opt, C_opt, D_opt = parametros_optimos
```

**Salida del programa:**
```
======================================================================
RESULTADOS DEL AJUSTE DE CURVA
======================================================================

Ecuación del ajuste: B_fit(t) = A·sin(B·t + C) + D

Parámetros óptimos:
  A (Amplitud)       = 0.974862 ± 0.005104 mT
  B (Frecuencia ω)   = 54.314376 ± 0.017578 rad/s
  C (Fase inicial)   = 6.278328 ± 0.061743 rad
  D (Offset)         = 0.201169 ± 0.003585 mT

Parámetros derivados:
  Frecuencia (f)     = 8.6444 Hz
  Período (T)        = 0.1157 s

Bondad del ajuste:
  R² (coef. determinación) = 0.973400
  Error RMS                = 0.112968 mT
======================================================================
```

---

### 3. Corriente calculada usando la Ley de Faraday

![Corriente vs Tiempo](I_vs_I_exp_faraday.png)

*Figura 2: Comparación entre la corriente experimental y la corriente teórica calculada usando la Ley de Faraday con ω = 54.314 rad/s.*

---

### 4. Análisis completo: B(t), dB/dt e I(t)

![Análisis completo](analisis_faraday_completo.png)

*Figura 3: (a) Corriente experimental vs teórica, (b) Campo magnético ajustado, (c) Derivada temporal del campo magnético (dB/dt) proporcional a la corriente inducida.*

---

## Conclusión

La **velocidad angular experimental del imán** es **ω = 54.31 rad/s**, determinada mediante el ajuste de curva senoidal al campo magnético medido. Este valor permite calcular teóricamente la corriente inducida usando la Ley de Faraday, confirmando la relación directa entre la velocidad de rotación del imán y la corriente generada en la bobina.
