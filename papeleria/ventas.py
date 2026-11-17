"""Cobro de una venta de la papelería."""
from decimal import ROUND_HALF_UP, Decimal

from papeleria.inventario import Inventario

PIEZAS_MAYOREO = 12
DESCUENTO_MAYOREO = Decimal("0.10")
CENTAVO = Decimal("0.01")


def total(inventario: Inventario, renglones: list[tuple[int, int]]) -> Decimal:
    """Suma de la venta, con 10 % de mayoreo desde 12 piezas del mismo artículo (RN-005); saca las piezas del inventario."""
    suma = Decimal("0")
    for articulo_id, piezas in renglones:
        inventario.sacar(articulo_id, piezas)
        importe = inventario.obtener(articulo_id).precio * piezas
        if piezas >= PIEZAS_MAYOREO:
            importe *= 1 - DESCUENTO_MAYOREO
        suma += importe
    return suma.quantize(CENTAVO, rounding=ROUND_HALF_UP)


def iva(monto: Decimal) -> float:
    # Incumple a propósito RN-001 (float pierde centavos) y RN-004 (la tasa escrita a mano en lugar de TASA_IVA).
    # Correcto: (monto * TASA_IVA).quantize(CENTAVO, rounding=ROUND_HALF_UP)
    return float(monto) * 0.16
