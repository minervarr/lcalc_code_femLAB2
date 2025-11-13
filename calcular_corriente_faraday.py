"""
Script para calcular la corriente I(t) usando la Ley de Faraday
a partir del ajuste del campo magnético B_fit(t)

Ley de Faraday: ε_ind = -N·A·(dΦ/dt) = -N·A·(dB_fit/dt)
Ley de Ohm: I(t) = ε_ind / R

Laboratorio de Física - FEM
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Backend sin GUI
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# ============================================================================
# PARÁMETROS DEL EXPERIMENTO (Ajustar según su laboratorio)
# ============================================================================

# Parámetros de la bobina
N = 200              # Número de vueltas de la bobina
r_bobina = 0.025     # Radio de la bobina en metros (ejemplo: 2.5 cm)
A_bobina = np.pi * r_bobina**2  # Área de la bobina en m²

# Resistencia del circuito
R = 10.0             # Resistencia total en Ohmios (Ω)

print("="*70)
print("CÁLCULO DE CORRIENTE USANDO LA LEY DE FARADAY")
print("="*70)
print("\nParámetros del experimento:")
print(f"  Número de vueltas (N):        {N}")
print(f"  Radio de la bobina (r):       {r_bobina*100:.2f} cm = {r_bobina:.4f} m")
print(f"  Área de la bobina (A):        {A_bobina:.6f} m²")
print(f"  Resistencia del circuito (R): {R:.2f} Ω")
print("="*70)

# ============================================================================
# CARGAR DATOS EXPERIMENTALES
# ============================================================================

print("\nCargando datos experimentales...")
data = np.loadtxt('datafinal.txt', skiprows=7, delimiter='\t')

# Extraer columnas
t_all = data[:, 0]      # Tiempo en segundos
B_all = data[:, 1]      # Campo magnético experimental en mT
I_all = data[:, 2]      # Corriente experimental en A

# Filtrar datos entre 3 y 4 segundos
print("Filtrando datos entre 3.0 y 4.0 segundos...")
mask = (t_all >= 3.0) & (t_all <= 4.0)
t_exp = t_all[mask]
B_exp = B_all[mask]
I_exp = I_all[mask]

print(f"✓ Datos cargados y filtrados: {len(t_exp)} puntos en rango [3.0, 4.0] s")

# ============================================================================
# PARÁMETROS DEL AJUSTE B_fit(t) = A·sin(B·t + C) + D
# ============================================================================

# Parámetros obtenidos del ajuste de curva (ajuste_curva_B.py)
# Datos filtrados entre 3.0 y 4.0 segundos
A_fit = 0.974862       # Amplitud en mT
B_fit = 54.314376      # Frecuencia angular ω en rad/s
C_fit = 6.278328       # Fase inicial en rad
D_fit = 0.201169       # Offset en mT

print("\nParámetros del ajuste B_fit(t) = A·sin(B·t + C) + D:")
print(f"  A = {A_fit:.6f} mT")
print(f"  B = {B_fit:.6f} rad/s")
print(f"  C = {C_fit:.6f} rad")
print(f"  D = {D_fit:.6f} mT")

# ============================================================================
# FUNCIONES
# ============================================================================

def B_fit_func(t):
    """
    Función del campo magnético ajustado B_fit(t)
    Retorna B en mT
    """
    return A_fit * np.sin(B_fit * t + C_fit) + D_fit

def dB_fit_dt(t):
    """
    Derivada temporal del campo magnético dB_fit/dt
    dB_fit/dt = A·B·cos(B·t + C)
    Retorna dB/dt en mT/s
    """
    return A_fit * B_fit * np.cos(B_fit * t + C_fit)

def calcular_corriente_faraday(t):
    """
    Calcula la corriente I(t) usando la Ley de Faraday

    ε_ind = -N·A·(dB_fit/dt)
    I(t) = ε_ind / R

    Nota: dB_fit/dt está en mT/s, hay que convertir a T/s
    1 mT = 10^-3 T
    """
    # Convertir dB/dt de mT/s a T/s
    dB_dt_Tesla_s = dB_fit_dt(t) * 1e-3  # T/s

    # FEM inducida (Ley de Faraday)
    epsilon_ind = -N * A_bobina * dB_dt_Tesla_s  # Voltios

    # Corriente (Ley de Ohm)
    I_teorica = epsilon_ind / R  # Amperios

    return I_teorica

# ============================================================================
# CÁLCULO DE LA CORRIENTE TEÓRICA
# ============================================================================

print("\nCalculando corriente teórica I(t) usando la Ley de Faraday...")

# Calcular B_fit y dB_fit/dt para todos los tiempos
B_fit_vals = B_fit_func(t_exp)
dB_dt_vals = dB_fit_dt(t_exp)

# Calcular corriente teórica
I_teorica = calcular_corriente_faraday(t_exp)

print(f"✓ Corriente teórica calculada")

# Estadísticas
print("\nEstadísticas de I_teorica:")
print(f"  Valor máximo:    {I_teorica.max():.6f} A")
print(f"  Valor mínimo:    {I_teorica.min():.6f} A")
print(f"  Valor promedio:  {I_teorica.mean():.6f} A")
print(f"  Amplitud (pico): {(I_teorica.max() - I_teorica.min())/2:.6f} A")

print("\nEstadísticas de I_exp:")
print(f"  Valor máximo:    {I_exp.max():.6f} A")
print(f"  Valor mínimo:    {I_exp.min():.6f} A")
print(f"  Valor promedio:  {I_exp.mean():.6f} A")
print(f"  Amplitud (pico): {(I_exp.max() - I_exp.min())/2:.6f} A")

# ============================================================================
# GRAFICAR RESULTADOS
# ============================================================================

print("\nGenerando gráficas...")

# Gráfica 1: Comparación I(t) vs I_exp
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

# Subgráfica superior: Comparación de corrientes
ax1.plot(t_exp, I_exp * 1000, 'b-', linewidth=1.5, alpha=0.7, label='$I_{exp}(t)$ (Experimental)')
ax1.plot(t_exp, I_teorica * 1000, 'r-', linewidth=2, label='$I(t)$ (Ley de Faraday)')
ax1.set_xlabel('Tiempo (s)', fontsize=13, fontweight='bold')
ax1.set_ylabel('Corriente (mA)', fontsize=13, fontweight='bold')
ax1.set_title('Comparación: Corriente Experimental vs Corriente Teórica (Ley de Faraday)',
              fontsize=15, fontweight='bold', pad=15)
ax1.grid(True, alpha=0.3, linestyle='--')
ax1.legend(fontsize=12, loc='upper right')

# Cuadro de texto con ecuaciones
ecuacion_texto = (
    'Ley de Faraday:\n'
    r'$\varepsilon_{ind} = -N \cdot A \cdot \frac{d\Phi}{dt} = -N \cdot A \cdot \frac{dB_{fit}}{dt}$' + '\n'
    r'$I(t) = \frac{\varepsilon_{ind}}{R}$' + '\n\n'
    f'Parámetros:\n'
    f'$N = {N}$ vueltas\n'
    f'$A = {A_bobina:.6f}$ m²\n'
    f'$R = {R:.1f}$ Ω'
)

ax1.text(0.02, 0.97, ecuacion_texto, transform=ax1.transAxes,
         fontsize=10, verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9,
                  edgecolor='black', linewidth=1.5))

# Subgráfica inferior: Campo magnético B_fit(t)
ax2.plot(t_exp, B_exp, 'b.', markersize=1.5, alpha=0.4, label='$B_{exp}(t)$')
ax2.plot(t_exp, B_fit_vals, 'r-', linewidth=2, label='$B_{fit}(t)$')
ax2.set_xlabel('Tiempo (s)', fontsize=13, fontweight='bold')
ax2.set_ylabel('Campo Magnético (mT)', fontsize=13, fontweight='bold')
ax2.set_title('Campo Magnético: Datos Experimentales y Ajuste',
              fontsize=14, fontweight='bold', pad=10)
ax2.grid(True, alpha=0.3, linestyle='--')
ax2.legend(fontsize=12)

# Cuadro con la función B_fit
b_fit_texto = (
    f'$B_{{fit}}(t) = {A_fit:.4f} \\cdot \\sin({B_fit:.4f} \\cdot t {C_fit:+.4f}) {D_fit:+.4f}$ mT\n'
    f'$\\frac{{dB_{{fit}}}}{{dt}} = {A_fit*B_fit:.4f} \\cdot \\cos({B_fit:.4f} \\cdot t {C_fit:+.4f})$ mT/s'
)

ax2.text(0.98, 0.97, b_fit_texto, transform=ax2.transAxes,
         fontsize=10, verticalalignment='top', horizontalalignment='right',
         bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.9,
                  edgecolor='black', linewidth=1.5))

plt.tight_layout()

# Guardar figura
nombre_archivo1 = 'corriente_faraday_comparacion.png'
plt.savefig(nombre_archivo1, dpi=300, bbox_inches='tight')
print(f"✓ Gráfica guardada como '{nombre_archivo1}'")

# ============================================================================
# Gráfica 2: Figura con 3 subgráficas
# ============================================================================

fig2, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 12))

# Subgráfica 1: Corriente (comparación)
ax1.plot(t_exp, I_exp * 1000, 'b-', linewidth=1.5, alpha=0.7, label='$I_{exp}(t)$')
ax1.plot(t_exp, I_teorica * 1000, 'r-', linewidth=2, label='$I(t)$ Faraday')
ax1.set_xlabel('Tiempo (s)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Corriente (mA)', fontsize=12, fontweight='bold')
ax1.set_title('(a) Corriente: Experimental vs Ley de Faraday',
              fontsize=13, fontweight='bold')
ax1.grid(True, alpha=0.3, linestyle='--')
ax1.legend(fontsize=11, loc='upper right')

# Subgráfica 2: Campo magnético
ax2.plot(t_exp, B_fit_vals, 'g-', linewidth=2.5, label='$B_{fit}(t)$')
ax2.set_xlabel('Tiempo (s)', fontsize=12, fontweight='bold')
ax2.set_ylabel('Campo Magnético (mT)', fontsize=12, fontweight='bold')
ax2.set_title('(b) Campo Magnético Ajustado',
              fontsize=13, fontweight='bold')
ax2.grid(True, alpha=0.3, linestyle='--')
ax2.legend(fontsize=11)

# Subgráfica 3: Derivada del campo magnético
ax3.plot(t_exp, dB_dt_vals, 'm-', linewidth=2, label='$dB_{fit}/dt$')
ax3.set_xlabel('Tiempo (s)', fontsize=12, fontweight='bold')
ax3.set_ylabel('dB/dt (mT/s)', fontsize=12, fontweight='bold')
ax3.set_title('(c) Derivada Temporal del Campo Magnético',
              fontsize=13, fontweight='bold')
ax3.grid(True, alpha=0.3, linestyle='--')
ax3.legend(fontsize=11)
ax3.axhline(y=0, color='k', linestyle='-', linewidth=0.8)

plt.tight_layout()

nombre_archivo2 = 'analisis_faraday_completo.png'
plt.savefig(nombre_archivo2, dpi=300, bbox_inches='tight')
print(f"✓ Gráfica completa guardada como '{nombre_archivo2}'")

# ============================================================================
# Gráfica 3: Solo I(t) vs I_exp (versión simple para el informe)
# ============================================================================

fig3, ax = plt.subplots(1, 1, figsize=(12, 7))

ax.plot(t_exp, I_exp * 1000, 'b-', linewidth=2, alpha=0.8,
        label='$I_{exp}(t)$ - Corriente Experimental', zorder=1)
ax.plot(t_exp, I_teorica * 1000, 'r--', linewidth=2.5,
        label='$I(t)$ - Corriente Teórica (Ley de Faraday)', zorder=2)

ax.set_xlabel('Tiempo (s)', fontsize=14, fontweight='bold')
ax.set_ylabel('Corriente (mA)', fontsize=14, fontweight='bold')
ax.set_title('Corriente vs Tiempo: Experimental y Teórica (Ley de Faraday)',
             fontsize=16, fontweight='bold', pad=20)
ax.grid(True, alpha=0.3, linestyle='--')
ax.legend(fontsize=13, loc='upper right', framealpha=0.95)

# Cuadro de texto con las ecuaciones principales
texto_ecuaciones = (
    'Ley de Faraday:\n'
    r'$\Phi = B_{fit}(t) \cdot A$' + '\n'
    r'$\varepsilon_{ind} = -N \cdot A \cdot \frac{dB_{fit}}{dt}$' + '\n'
    r'$I(t) = \frac{\varepsilon_{ind}}{R}$' + '\n\n'
    f'Parámetros del experimento:\n'
    f'$N = {N}$ vueltas\n'
    f'$A = {A_bobina*1e4:.4f}$ cm² = ${A_bobina:.6f}$ m²\n'
    f'$R = {R:.1f}$ Ω\n\n'
    f'Campo magnético ajustado:\n'
    f'$B_{{fit}}(t) = {A_fit:.4f} \\sin({B_fit:.4f}t {C_fit:+.4f}) {D_fit:+.4f}$ mT'
)

ax.text(0.02, 0.98, texto_ecuaciones, transform=ax.transAxes,
        fontsize=10, verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.95,
                 edgecolor='black', linewidth=2))

plt.tight_layout()

nombre_archivo3 = 'I_vs_I_exp_faraday.png'
plt.savefig(nombre_archivo3, dpi=300, bbox_inches='tight')
print(f"✓ Gráfica simple guardada como '{nombre_archivo3}'")

# ============================================================================
# ANÁLISIS DE DIFERENCIAS
# ============================================================================

# Calcular diferencia entre teórica y experimental
diferencia = I_teorica - I_exp
error_relativo = np.abs(diferencia / I_exp) * 100  # Error porcentual

# Filtrar valores donde I_exp es muy pequeño para evitar divisiones por cero
mask = np.abs(I_exp) > 1e-6
error_relativo_filtrado = error_relativo[mask]

print("\nAnálisis de diferencias entre I_teorica e I_exp:")
print(f"  Diferencia máxima:     {diferencia.max()*1000:.6f} mA")
print(f"  Diferencia mínima:     {diferencia.min()*1000:.6f} mA")
print(f"  Diferencia promedio:   {diferencia.mean()*1000:.6f} mA")
print(f"  RMS de la diferencia:  {np.sqrt(np.mean(diferencia**2))*1000:.6f} mA")

if len(error_relativo_filtrado) > 0:
    print(f"\nError relativo (donde |I_exp| > 1 µA):")
    print(f"  Error promedio:        {error_relativo_filtrado.mean():.2f}%")
    print(f"  Error máximo:          {error_relativo_filtrado.max():.2f}%")

print("\n" + "="*70)
print("✓ PROCESO COMPLETADO EXITOSAMENTE")
print("="*70)
print("\nArchivos generados:")
print(f"  1. {nombre_archivo1}")
print(f"  2. {nombre_archivo2}")
print(f"  3. {nombre_archivo3}")
print("\nNOTA: Si las corrientes teórica y experimental no coinciden bien,")
print("      ajuste los parámetros N, A y R en la sección de parámetros del script.")
print("="*70)
