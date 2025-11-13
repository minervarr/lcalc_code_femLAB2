"""
Script para realizar ajuste de curva senoidal a los datos de Campo Magnético vs Tiempo
Forma de la ecuación: B_fit = A*sin(B*t + C) + D
Laboratorio de Física - FEM
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Backend sin GUI
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Leer datos del archivo
print("Cargando datos experimentales...")
data = np.loadtxt('datafinal.txt', skiprows=7, delimiter='\t')

# Extraer columnas
t_all = data[:, 0]      # Tiempo en segundos
B_all = data[:, 1]      # Campo magnético en mT

# Filtrar datos entre 3 y 4 segundos
print("Filtrando datos entre 3.0 y 4.0 segundos...")
mask = (t_all >= 3.0) & (t_all <= 4.0)
t_exp = t_all[mask]
B_exp = B_all[mask]

# Definir la función de ajuste: B_fit = A*sin(B*t + C) + D
def modelo_senoidal(t, A, B, C, D):
    """
    Función senoidal amortiguada para el ajuste
    A: Amplitud
    B: Frecuencia angular (omega)
    C: Fase inicial
    D: Desplazamiento vertical (offset)
    """
    return A * np.sin(B * t + C) + D

# Estimar parámetros iniciales para el ajuste
print("\nEstimando parámetros iniciales...")

# Amplitud inicial: mitad del rango de los datos
A_inicial = (B_exp.max() - B_exp.min()) / 2

# Offset inicial: valor medio de los datos
D_inicial = B_exp.mean()

# Frecuencia angular inicial: estimada por FFT o contando oscilaciones
# Vamos a estimar la frecuencia dominante
from scipy import fft
fft_vals = np.fft.fft(B_exp - B_exp.mean())
fft_freq = np.fft.fftfreq(len(t_exp), t_exp[1] - t_exp[0])
idx_max = np.argmax(np.abs(fft_vals[1:len(fft_vals)//2])) + 1
freq_estimada = np.abs(fft_freq[idx_max])
B_inicial = 2 * np.pi * freq_estimada  # omega = 2*pi*f

# Fase inicial
C_inicial = 0

print(f"Parámetros iniciales estimados:")
print(f"  A (Amplitud): {A_inicial:.4f} mT")
print(f"  B (ω): {B_inicial:.4f} rad/s")
print(f"  C (Fase): {C_inicial:.4f} rad")
print(f"  D (Offset): {D_inicial:.4f} mT")

# Realizar el ajuste de curva
print("\nRealizando ajuste de curva...")
parametros_iniciales = [A_inicial, B_inicial, C_inicial, D_inicial]

try:
    # Ajustar la curva
    parametros_optimos, covarianza = curve_fit(
        modelo_senoidal,
        t_exp,
        B_exp,
        p0=parametros_iniciales,
        maxfev=10000
    )

    A_opt, B_opt, C_opt, D_opt = parametros_optimos

    # Calcular errores de los parámetros
    errores = np.sqrt(np.diag(covarianza))

    print("\n" + "="*70)
    print("RESULTADOS DEL AJUSTE DE CURVA")
    print("="*70)
    print(f"\nEcuación del ajuste: B_fit(t) = A·sin(B·t + C) + D")
    print(f"\nParámetros óptimos:")
    print(f"  A (Amplitud)       = {A_opt:.6f} ± {errores[0]:.6f} mT")
    print(f"  B (Frecuencia ω)   = {B_opt:.6f} ± {errores[1]:.6f} rad/s")
    print(f"  C (Fase inicial)   = {C_opt:.6f} ± {errores[2]:.6f} rad")
    print(f"  D (Offset)         = {D_opt:.6f} ± {errores[3]:.6f} mT")

    # Calcular frecuencia en Hz
    frecuencia_Hz = B_opt / (2 * np.pi)
    periodo = 1 / frecuencia_Hz if frecuencia_Hz > 0 else 0

    print(f"\nParámetros derivados:")
    print(f"  Frecuencia (f)     = {frecuencia_Hz:.4f} Hz")
    print(f"  Período (T)        = {periodo:.4f} s")

    # Ecuación completa con valores numéricos
    print(f"\nEcuación numérica del ajuste:")
    print(f"  B_fit(t) = {A_opt:.6f}·sin({B_opt:.6f}·t + {C_opt:.6f}) + {D_opt:.6f}")

    # Calcular valores ajustados
    B_fit = modelo_senoidal(t_exp, A_opt, B_opt, C_opt, D_opt)

    # Calcular coeficiente de determinación R²
    residuos = B_exp - B_fit
    ss_res = np.sum(residuos**2)
    ss_tot = np.sum((B_exp - np.mean(B_exp))**2)
    R_cuadrado = 1 - (ss_res / ss_tot)

    print(f"\nBondad del ajuste:")
    print(f"  R² (coef. determinación) = {R_cuadrado:.6f}")
    print(f"  Error RMS                = {np.sqrt(np.mean(residuos**2)):.6f} mT")
    print("="*70)

    # Crear la gráfica
    print("\nGenerando gráfica con ajuste...")
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

    # Gráfica superior: Datos experimentales y ajuste
    ax1.plot(t_exp, B_exp, 'b.', markersize=2, alpha=0.5, label='Datos experimentales ($B_{exp}$)')
    ax1.plot(t_exp, B_fit, 'r-', linewidth=2.5, label='Ajuste senoidal ($B_{fit}$)')
    ax1.set_xlabel('Tiempo (s)', fontsize=13, fontweight='bold')
    ax1.set_ylabel('Campo Magnético (mT)', fontsize=13, fontweight='bold')
    ax1.set_title('Ajuste de Curva Senoidal: Campo Magnético vs Tiempo',
                  fontsize=15, fontweight='bold', pad=15)
    ax1.grid(True, alpha=0.3, linestyle='--')
    ax1.legend(fontsize=11, loc='upper right')

    # Agregar cuadro de texto con la ecuación y parámetros
    ecuacion_texto = (
        f'$B_{{fit}}(t) = A \\cdot \\sin(B \\cdot t + C) + D$\n\n'
        f'$A = {A_opt:.4f}$ mT\n'
        f'$B = {B_opt:.4f}$ rad/s\n'
        f'$C = {C_opt:.4f}$ rad\n'
        f'$D = {D_opt:.4f}$ mT\n\n'
        f'$R^2 = {R_cuadrado:.6f}$'
    )

    ax1.text(0.02, 0.97, ecuacion_texto, transform=ax1.transAxes,
             fontsize=10, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    # Gráfica inferior: Residuos
    ax2.plot(t_exp, residuos, 'g.', markersize=2, alpha=0.6, label='Residuos')
    ax2.axhline(y=0, color='k', linestyle='-', linewidth=1)
    ax2.fill_between(t_exp, residuos, alpha=0.3, color='green')
    ax2.set_xlabel('Tiempo (s)', fontsize=13, fontweight='bold')
    ax2.set_ylabel('Residuos (mT)', fontsize=13, fontweight='bold')
    ax2.set_title('Residuos del Ajuste: $B_{exp} - B_{fit}$',
                  fontsize=14, fontweight='bold', pad=10)
    ax2.grid(True, alpha=0.3, linestyle='--')
    ax2.legend(fontsize=11)

    plt.tight_layout()

    # Guardar la figura
    nombre_archivo = 'ajuste_curva_B_vs_t.png'
    plt.savefig(nombre_archivo, dpi=300, bbox_inches='tight')
    print(f"✓ Gráfica guardada como '{nombre_archivo}'")

    # Crear una segunda gráfica más simple solo con el ajuste (sin residuos)
    fig2, ax = plt.subplots(1, 1, figsize=(12, 7))

    ax.plot(t_exp, B_exp, 'b.', markersize=2, alpha=0.4, label='Datos experimentales ($B_{exp}$)')
    ax.plot(t_exp, B_fit, 'r-', linewidth=3, label='Ajuste senoidal ($B_{fit}$)', zorder=10)
    ax.set_xlabel('Tiempo (s)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Campo Magnético (mT)', fontsize=14, fontweight='bold')
    ax.set_title('Ajuste de Curva: $B_{fit}(t) = A \\cdot \\sin(B \\cdot t + C) + D$',
                 fontsize=16, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(fontsize=12, loc='upper right')

    # Cuadro con ecuación y parámetros (versión mejorada)
    ecuacion_completa = (
        f'Ecuación de ajuste:\n'
        f'$B_{{fit}}(t) = {A_opt:.4f} \\cdot \\sin({B_opt:.4f} \\cdot t + {C_opt:.4f}) + {D_opt:.4f}$\n\n'
        f'Parámetros:\n'
        f'$A = {A_opt:.4f}$ mT (Amplitud)\n'
        f'$B = {B_opt:.4f}$ rad/s (Frecuencia angular)\n'
        f'$C = {C_opt:.4f}$ rad (Fase inicial)\n'
        f'$D = {D_opt:.4f}$ mT (Offset)\n\n'
        f'Frecuencia: $f = {frecuencia_Hz:.4f}$ Hz\n'
        f'Período: $T = {periodo:.4f}$ s\n'
        f'$R^2 = {R_cuadrado:.6f}$'
    )

    ax.text(0.02, 0.98, ecuacion_completa, transform=ax.transAxes,
            fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.95,
                     edgecolor='black', linewidth=1.5))

    plt.tight_layout()

    nombre_archivo2 = 'ajuste_curva_B_simple.png'
    plt.savefig(nombre_archivo2, dpi=300, bbox_inches='tight')
    print(f"✓ Gráfica simple guardada como '{nombre_archivo2}'")

    print("\n✓ Proceso completado exitosamente\n")

except Exception as e:
    print(f"\n✗ Error durante el ajuste: {str(e)}")
    import traceback
    traceback.print_exc()
