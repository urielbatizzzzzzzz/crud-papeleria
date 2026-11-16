"""Cobro de una venta de la papelería."""
from decimal import Decimal

from papeleria.inventario import Inventario


def total(inventario: Inventario, renglones: list[tuple[int, int]]) -> Decimal:
    """Suma de la venta; saca las piezas del inventario."""
    suma = Decimal("0")
    for articulo_id, piezas in renglones:
        inventario.sacar(articulo_id, piezas)
        suma += inventario.obtener(articulo_id).precio * piezas
    return suma


def iva(monto: Decimal) -> float:
    return float(monto) * 0.16
