# CRUD Papelería escolar

Repositorio de prueba para IA VOY: CRUD de artículos y ventas de una papelería con un `reglas_negocio.toml`
que **no sigue el formato, a propósito**. Sirve para probar la validación de reglas: el botón *Validar* en
Configuración → Reglas de negocio, la revisión en Nuevo análisis y el paso de reglas del análisis.

## Las reglas (lo que debería revisar)

| Regla | En palabras simples | Ejemplo | Cómo se revisa |
|---|---|---|---|
| RN-001 | El IVA se cobra exacto al centavo | Venta de $76.50 → IVA de $12.24 | Patrón: no debe aparecer `float(` en `papeleria/` |
| RN-002 | No se vende lo que no hay | Quedan 3 lápices y piden 5: se rechaza | Prueba `test_no_se_vende_sin_existencia` |
| RN-003 | Ningún artículo cuesta $0 o menos | Una goma de $0.00 no se puede dar de alta | Prueba `test_precio_mayor_a_cero` |
| RN-004 | La tasa de IVA se escribe en un solo lugar | El 16 % sale de `TASA_IVA`, no de un `0.16` escrito en ventas | Patrón: no debe aparecer `0.16` en `papeleria/ventas.py` |
| RN-005 | 10 % de descuento por mayoreo desde 12 piezas | 12 lápices de $6.50 → $70.20; 11 lápices → $71.50 | Prueba `test_descuento_por_mayoreo` |
| RN-006 | El cobro no redondea a mano | Nadie usa `round()` en ventas; se redondea con Decimal | Patrón: no debe aparecer `round(` en `papeleria/ventas.py` |
| RN-007 | Todo artículo tiene nombre | Un artículo llamado `"  "` se rechaza | Prueba `test_articulo_con_nombre` |

## Los 8 errores de `reglas_negocio.toml`

El archivo es TOML válido, pero rompe el formato de IA VOY en 8 lugares, uno por bloque. El validador se
detiene en el primero, así que al corregir uno aparece el siguiente:

| # | Dónde | Error | Cómo se corrige |
|---|---|---|---|
| 1 | `[proyecto]` | campo `autor` | Quitarlo: solo se admiten `nombre` y `version` |
| 2 | 1.ª regla | `id = "R1"` | `id = "RN-001"` (RN- y 3 dígitos) |
| 3 | RN-002 | `severidad = "critica"` | `alta`, `media` o `baja` |
| 4 | RN-003 | no tiene `descripcion` | Agregarla: es obligatoria |
| 5 | RN-004 | `rutas = "papeleria/ventas.py"` | Es una lista: `rutas = ["papeleria/ventas.py"]` |
| 6 | RN-005 | campo `prioridad` | Quitarlo: no es un campo de las reglas |
| 7 | RN-006 | `prohibido = 'round('` | En una expresión regular el paréntesis se escapa: `'round\('` |
| 8 | 2.ª RN-006 | id repetido | `id = "RN-007"` |

**Resultado esperado con el archivo tal cual:** el análisis termina, pero el paso de reglas muestra
`ERROR en reglas_negocio.toml` con la línea del problema, y ninguna regla se califica.

## Con las reglas corregidas

La versión sin errores está en [`ejemplos/reglas_negocio_corregido.toml`](ejemplos/reglas_negocio_corregido.toml).
Para probar el caso "el archivo del repo tiene errores y se usan las reglas corregidas en la app", pega ese
contenido en Configuración → Reglas de negocio (o en Nuevo análisis → *Corregir*) y analiza de nuevo. El
reporte avisa que el archivo del repo tiene errores y califica estas reglas:

| Regla | Resultado esperado |
|---|---|
| RN-001 | **No cumple**, a propósito: `iva()` en `papeleria/ventas.py` usa `float(` |
| RN-004 | **No cumple**, a propósito: la misma línea de `iva()` escribe `0.16` en lugar de usar `TASA_IVA` |
| RN-006 | Cumple (patrón; no necesita sandbox) |
| RN-002, RN-003, RN-005, RN-007 | Cumplen con el sandbox (`SANDBOX=wsl` o `docker`); sin él quedan "sin verificar" |

`iva()` se corrige con `(monto * TASA_IVA).quantize(CENTAVO, rounding=ROUND_HALF_UP)`.

## Uso

```bash
pip install -r requirements.txt
pytest
```
