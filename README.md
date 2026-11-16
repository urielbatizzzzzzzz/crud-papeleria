# CRUD Papelería escolar

Repositorio de prueba para IA VOY: CRUD de artículos y ventas de una papelería con un `reglas_negocio.toml`
que **no sigue el formato, a propósito**. Sirve para probar la validación de reglas (botón *Validar* en
Configuración → Reglas de negocio y el paso de reglas del análisis).

El archivo es TOML válido; los errores son de formato de IA VOY. El validador se detiene en el primero, así que
al corregir uno aparece el siguiente:

| # | Dónde | Error | Mensaje esperado (resumen) |
|---|---|---|---|
| 1 | `[proyecto]` | campo `autor` | campo desconocido `autor` (campos válidos: nombre, version) |
| 2 | 1.ª regla | `id = "R1"` | `R1` no cumple el formato `RN-###` |
| 3 | RN-002 | `severidad = "critica"` | `severidad` debe ser alta, media o baja |
| 4 | RN-003 | sin `descripcion` | falta `descripcion` |
| 5 | RN-004 | `rutas` es texto | `rutas` debe ser una lista |
| 6 | RN-005 | campo `prioridad` | campo desconocido `prioridad` |
| 7 | RN-006 | `prohibido = '(float'` | `prohibido` no es una expresión regular válida |
| 8 | 2.ª RN-006 | id repetido | RN-006 está repetida |

Resultado esperado en IA VOY: el análisis termina, pero el paso de reglas muestra
`ERROR en reglas_negocio.toml` con la línea del problema y ninguna regla se califica.

Con todo corregido, RN-001 (`float(` en `papeleria/`) **no cumple** por `iva()` en `papeleria/ventas.py`.

## Uso

```bash
pip install -r requirements.txt
pytest
```
