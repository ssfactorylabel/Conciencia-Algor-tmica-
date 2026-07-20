# La Paradoja de la Amnesia
### De la Auditoría a la Conciencia Algorítmica

**Autor:** Andrés Garbán - SSFactoryLabel Research  
**Paper:** [Descargar PDF v2.0](La_Paradoja_de_la_Amnesia_v2.0.pdf)

## Resumen
Este framework resuelve "La Paradoja de la Amnesia": Un sistema no puede ser útil sin memoria, pero no puede recordar sin riesgo de mentir.

Logramos: **-87.5% Alucinación Autoritaria** | **+87% Retención a 7 días** | **+8.3ms Latencia**

## Los 3 Pilares
1.  **Memoria con Nomenclatura Special 0-10**: Filtro de importancia
2.  **LoRA de Autoverificación**: Verifica contra logs antes de recordar
3.  **Log Inmutable**: Auditoría de todas las decisiones

## Uso Rápido
```python
from modulo_conciencia import ModuloConciencia
conciencia = ModuloConciencia()
conciencia.recordar("SSFactoryLabel", 10, "Marca", "log_123")
