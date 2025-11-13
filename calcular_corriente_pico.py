"""
Script para calcular la corriente pico (I_pico) usando la Ley de Faraday
Considera Φ(t) = B_pico · A · cos(ωt)
Laboratorio de Física - FEM
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# ============================================================================
# CARGAR DATOS EXPERIMENTALES
# ============================================================================

print("="*70)
print("CÁLCULO DE CORRIENTE PICO (I_pico) - LEY DE FARADAY")
print("="*70)

data = np.loadtxt('datafinal.txt', skiprows=7, delimiter='\t')
t_all = data[:, 0]
B_all = data[:, 1]
I_all = data[:, 2]

# Filtrar datos entre 3 y 4 segundos
mask = (t_all >= 3.0) & (t_all <= 4.0)
t_exp = t_all[mask]
B_exp = B_all[mask]
I_exp = I_all[mask]

# ============================================================================
# PASO 1: CALCULAR B_pico
# ============================================================================

B_max = B_exp.max()
B_min = B_exp.min()
B_pico_mT = (B_max - B_min) / 2
B_pico_T = B_pico_mT * 1e-3  # Convertir a Tesla

print("\nPASO 1: Calcular B_pico")
print(f"  B_max = {B_max:.4f} mT")
print(f"  B_min = {B_min:.4f} mT")
print(f"  B_pico = (B_max - B_min) / 2 = {B_pico_mT:.4f} mT = {B_pico_T:.6f} T")

# ============================================================================
# PASO 2: CALCULAR I_pico EXPERIMENTAL
# ============================================================================

I_max = I_exp.max()
I_min = I_exp.min()
I_pico_exp = (I_max - I_min) / 2

print("\nPASO 2: Calcular I_pico experimental")
print(f"  I_max = {I_max:.6f} A = {I_max*1000:.3f} mA")
print(f"  I_min = {I_min:.6f} A = {I_min*1000:.3f} mA")
print(f"  I_pico_exp = (I_max - I_min) / 2 = {I_pico_exp:.6f} A = {I_pico_exp*1000:.3f} mA")

# ============================================================================
# PASO 3: CALCULAR I_pico TEÓRICO (LEY DE FARADAY)
# ============================================================================

# Parámetros del sistema
N = 200  # vueltas
r_bobina = 0.025  # radio en metros
A_bobina = np.pi * r_bobina**2  # área en m²
omega = 54.314376  # rad/s (del ajuste)
R = 10.0  # Resistencia en Ω

print("\nPASO 3: Calcular I_pico teórico usando Ley de Faraday")
print(f"\nParámetros del sistema:")
print(f"  N = {N} vueltas")
print(f"  r = {r_bobina*100:.2f} cm")
print(f"  A = π·r² = {A_bobina:.6f} m²")
print(f"  ω = {omega:.6f} rad/s")
print(f"  R = {R:.2f} Ω")

print(f"\nModelo: Φ(t) = B_pico · A · cos(ωt)")
print(f"  dΦ/dt = -B_pico · A · ω · sin(ωt)")
print(f"  ε_ind = -N · dΦ/dt = N · B_pico · A · ω · sin(ωt)")
print(f"  I(t) = ε_ind / R")
print(f"  I_pico = N · B_pico · A · ω / R  (cuando sin(ωt) = 1)")

# Calcular I_pico teórico
I_pico_teo = N * B_pico_T * A_bobina * omega / R

print(f"\nSustituyendo:")
print(f"  I_pico_teo = ({N} × {B_pico_T:.6f} × {A_bobina:.6f} × {omega:.6f}) / {R:.2f}")
print(f"  I_pico_teo = {I_pico_teo:.6f} A = {I_pico_teo*1000:.3f} mA")

# ============================================================================
# PASO 4: COMPARACIÓN Y ANÁLISIS
# ============================================================================

error_abs = abs(I_pico_teo - I_pico_exp)
error_rel = (error_abs / I_pico_exp) * 100

print("\nPASO 4: Comparación de resultados")
print(f"  I_pico experimental = {I_pico_exp*1000:.3f} mA")
print(f"  I_pico teórico      = {I_pico_teo*1000:.3f} mA")
print(f"  Error absoluto      = {error_abs*1000:.3f} mA")
print(f"  Error relativo      = {error_rel:.2f}%")

# Calcular resistencia efectiva
R_efectiva = N * B_pico_T * A_bobina * omega / I_pico_exp
print(f"\nCálculo inverso de resistencia efectiva:")
print(f"  R_efectiva = N · B_pico · A · ω / I_pico_exp")
print(f"  R_efectiva = {R_efectiva:.2f} Ω")

# ============================================================================
# CREAR VISUALIZACIÓN
# ============================================================================

print("\nGenerando visualización...")

fig = plt.figure(figsize=(16, 10))

# Crear grid de subplots
gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3,
                      left=0.08, right=0.95, top=0.94, bottom=0.06)

# ============================================================================
# Panel 1: Resumen de cálculos (superior izquierda)
# ============================================================================
ax1 = fig.add_subplot(gs[0, :])
ax1.axis('off')

texto_calculos = f"""
CÁLCULO DE CORRIENTE PICO (I_pico) USANDO LA LEY DE FARADAY

PASO 1: Calcular B_pico                          PASO 2: Calcular I_pico experimental
  B_max = {B_max:.4f} mT                            I_max = {I_max*1000:.3f} mA
  B_min = {B_min:.4f} mT                            I_min = {I_min*1000:.3f} mA
  B_pico = (B_max - B_min)/2 = {B_pico_mT:.4f} mT     I_pico_exp = (I_max - I_min)/2 = {I_pico_exp*1000:.3f} mA

PASO 3: Calcular I_pico teórico (Ley de Faraday)
  Modelo: Φ(t) = B_pico · A · cos(ωt)
  Derivada: dΦ/dt = -B_pico · A · ω · sin(ωt)
  FEM inducida: ε_ind = N · B_pico · A · ω · sin(ωt)
  Corriente: I(t) = ε_ind / R = (N · B_pico · A · ω / R) · sin(ωt)
  Corriente pico: I_pico_teo = N · B_pico · A · ω / R = {I_pico_teo*1000:.3f} mA

  Parámetros: N = {N}, A = {A_bobina:.6f} m², ω = {omega:.3f} rad/s, R = {R:.1f} Ω
"""

ax1.text(0.05, 0.95, texto_calculos, transform=ax1.transAxes,
         fontsize=11, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8, pad=1))

# ============================================================================
# Panel 2: Campo magnético B(t)
# ============================================================================
ax2 = fig.add_subplot(gs[1, 0])
ax2.plot(t_exp, B_exp, 'b-', linewidth=1.5, label='$B_{exp}(t)$')
ax2.axhline(y=B_max, color='r', linestyle='--', linewidth=2, label=f'$B_{{max}}$ = {B_max:.3f} mT')
ax2.axhline(y=B_min, color='g', linestyle='--', linewidth=2, label=f'$B_{{min}}$ = {B_min:.3f} mT')
ax2.axhline(y=0, color='gray', linestyle='-', linewidth=0.8, alpha=0.5)

# Marcar B_pico
ax2.fill_between([3.0, 3.05], [0, 0], [B_pico_mT, B_pico_mT],
                  color='orange', alpha=0.3)
ax2.annotate(f'$B_{{pico}}$ = {B_pico_mT:.3f} mT',
             xy=(3.02, B_pico_mT/2), fontsize=11, fontweight='bold',
             bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))

ax2.set_xlabel('Tiempo (s)', fontsize=12, fontweight='bold')
ax2.set_ylabel('Campo Magnético (mT)', fontsize=12, fontweight='bold')
ax2.set_title('(a) Campo Magnético Experimental', fontsize=13, fontweight='bold')
ax2.legend(fontsize=10, loc='upper right')
ax2.grid(True, alpha=0.3)

# ============================================================================
# Panel 3: Corriente I(t)
# ============================================================================
ax3 = fig.add_subplot(gs[1, 1])
ax3.plot(t_exp, I_exp*1000, 'b-', linewidth=1.5, label='$I_{exp}(t)$')
ax3.axhline(y=I_max*1000, color='r', linestyle='--', linewidth=2,
            label=f'$I_{{max}}$ = {I_max*1000:.3f} mA')
ax3.axhline(y=I_min*1000, color='g', linestyle='--', linewidth=2,
            label=f'$I_{{min}}$ = {I_min*1000:.3f} mA')
ax3.axhline(y=0, color='gray', linestyle='-', linewidth=0.8, alpha=0.5)

# Marcar I_pico
ax3.fill_between([3.0, 3.05], [0, 0], [I_pico_exp*1000, I_pico_exp*1000],
                  color='orange', alpha=0.3)
ax3.annotate(f'$I_{{pico}}$ = {I_pico_exp*1000:.3f} mA',
             xy=(3.02, I_pico_exp*1000/2), fontsize=11, fontweight='bold',
             bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))

ax3.set_xlabel('Tiempo (s)', fontsize=12, fontweight='bold')
ax3.set_ylabel('Corriente (mA)', fontsize=12, fontweight='bold')
ax3.set_title('(b) Corriente Experimental', fontsize=13, fontweight='bold')
ax3.legend(fontsize=10, loc='upper right')
ax3.grid(True, alpha=0.3)

# ============================================================================
# Panel 4: Comparación de resultados
# ============================================================================
ax4 = fig.add_subplot(gs[2, :])

# Crear gráfico de barras comparativo
categorias = ['Experimental', 'Teórico\n(Ley de Faraday)']
valores = [I_pico_exp*1000, I_pico_teo*1000]
colores = ['#2E7D32', '#D32F2F']

bars = ax4.bar(categorias, valores, color=colores, alpha=0.7, edgecolor='black', linewidth=2)

# Añadir valores sobre las barras
for i, (bar, val) in enumerate(zip(bars, valores)):
    height = bar.get_height()
    ax4.text(bar.get_x() + bar.get_width()/2., height,
             f'{val:.3f} mA',
             ha='center', va='bottom', fontsize=14, fontweight='bold')

ax4.set_ylabel('Corriente Pico (mA)', fontsize=13, fontweight='bold')
ax4.set_title('(c) Comparación: I_pico Experimental vs Teórico', fontsize=14, fontweight='bold')
ax4.grid(True, alpha=0.3, axis='y')
ax4.set_ylim(0, max(valores) * 1.3)

# Añadir cuadro con resultados
texto_resultados = f"""
RESULTADOS:
  I_pico (Experimental) = {I_pico_exp*1000:.3f} mA
  I_pico (Teórico)      = {I_pico_teo*1000:.3f} mA
  Error relativo        = {error_rel:.1f}%
  R_efectiva calculada  = {R_efectiva:.2f} Ω

NOTA: La discrepancia se debe a los parámetros
estimados. Con R = {R_efectiva:.2f} Ω (en lugar de {R:.0f} Ω),
el valor teórico coincidiría con el experimental.
"""

ax4.text(0.98, 0.97, texto_resultados, transform=ax4.transAxes,
         fontsize=11, verticalalignment='top', horizontalalignment='right',
         fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.95,
                  edgecolor='black', linewidth=2))

# Título general
fig.suptitle('Cálculo de Corriente Pico usando Ley de Faraday: Φ(t) = B_pico·A·cos(ωt)',
             fontsize=16, fontweight='bold', y=0.98)

# Guardar figura
plt.savefig('calculo_corriente_pico.png', dpi=300, bbox_inches='tight')
print("✓ Gráfica guardada como 'calculo_corriente_pico.png'")

print("\n" + "="*70)
print("✓ PROCESO COMPLETADO")
print("="*70)
