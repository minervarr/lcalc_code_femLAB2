"""
Script para graficar datos experimentales de Campo Magnético e Intensidad de Corriente vs Tiempo
Laboratorio de Física - FEM
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')  # Backend sin GUI
import matplotlib.pyplot as plt

# Configurar estilo de gráficas
plt.style.use('seaborn-v0_8-darkgrid')

# Leer datos del archivo datafinal.txt
data = np.loadtxt('datafinal.txt', skiprows=7, delimiter='\t')

# Extraer columnas
t_all = data[:, 0]      # Tiempo en segundos
B_all = data[:, 1]      # Campo magnético en mT
I_all = data[:, 2]      # Corriente en A

# Filtrar datos entre 3 y 4 segundos
mask = (t_all >= 3.0) & (t_all <= 4.0)
t_exp = t_all[mask]
B_exp = B_all[mask]
I_exp = I_all[mask]

# Crear figura con dos subgráficas
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

# Gráfica 1: Campo Magnético vs Tiempo
ax1.plot(t_exp, B_exp, 'b-', linewidth=2, label='$B_{exp}(t)$')
ax1.scatter(t_exp[::10], B_exp[::10], c='blue', s=30, alpha=0.6, zorder=5)
ax1.set_xlabel('Tiempo (s)', fontsize=12, fontweight='bold')
ax1.set_ylabel('Campo Magnético (mT)', fontsize=12, fontweight='bold')
ax1.set_title('Campo Magnético Experimental vs Tiempo', fontsize=14, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.legend(fontsize=11)

# Gráfica 2: Corriente vs Tiempo
ax2.plot(t_exp, I_exp, 'r-', linewidth=2, label='$I_{exp}(t)$')
ax2.scatter(t_exp[::10], I_exp[::10], c='red', s=30, alpha=0.6, zorder=5)
ax2.set_xlabel('Tiempo (s)', fontsize=12, fontweight='bold')
ax2.set_ylabel('Corriente (A)', fontsize=12, fontweight='bold')
ax2.set_title('Corriente Experimental vs Tiempo', fontsize=14, fontweight='bold')
ax2.grid(True, alpha=0.3)
ax2.legend(fontsize=11)

# Ajustar espaciado entre subgráficas
plt.tight_layout()

# Guardar la figura
plt.savefig('graficas_experimentales.png', dpi=300, bbox_inches='tight')
print("✓ Gráfica guardada como 'graficas_experimentales.png'")

# Mostrar estadísticas de los datos
print("\n" + "="*60)
print("ESTADÍSTICAS DE LOS DATOS EXPERIMENTALES")
print("="*60)
print(f"\nTiempo de medición:")
print(f"  - Duración total: {t_exp[-1]:.3f} s")
print(f"  - Número de puntos: {len(t_exp)}")
print(f"  - Intervalo de muestreo: {t_exp[1] - t_exp[0]:.4f} s")

print(f"\nCampo Magnético (B):")
print(f"  - Valor inicial: {B_exp[0]:.4f} mT")
print(f"  - Valor final: {B_exp[-1]:.4f} mT")
print(f"  - Valor máximo: {B_exp.max():.4f} mT")
print(f"  - Valor mínimo: {B_exp.min():.4f} mT")
print(f"  - Valor promedio: {B_exp.mean():.4f} mT")

print(f"\nCorriente (I):")
print(f"  - Valor inicial: {I_exp[0]:.6f} A")
print(f"  - Valor final: {I_exp[-1]:.6f} A")
print(f"  - Valor máximo: {I_exp.max():.6f} A")
print(f"  - Valor mínimo: {I_exp.min():.6f} A")
print(f"  - Valor promedio: {I_exp.mean():.6f} A")
print("="*60)

# Gráfica guardada, no se muestra en pantalla (modo sin GUI)
print("\n✓ Proceso completado exitosamente")
