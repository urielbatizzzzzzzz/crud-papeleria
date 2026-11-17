from decimal import Decimal

import pytest

from papeleria import ventas
from papeleria.inventario import ArticuloInvalido, Inventario, SinExistencia


@pytest.fixture
def inventario():
    inv = Inventario()
    inv.crear("Cuaderno", "35.00", piezas=10)
    inv.crear("Lápiz", "6.50", piezas=30)
    return inv


@pytest.mark.regla("RN-001")
def test_total_de_venta(inventario):
    assert ventas.total(inventario, [(1, 2), (2, 1)]) == Decimal("76.50")


@pytest.mark.regla("RN-002")
def test_no_se_vende_sin_existencia(inventario):
    with pytest.raises(SinExistencia):
        ventas.total(inventario, [(1, 11)])


@pytest.mark.regla("RN-003")
def test_precio_mayor_a_cero(inventario):
    with pytest.raises(ArticuloInvalido):
        inventario.crear("Goma", "0.00")
    with pytest.raises(ArticuloInvalido):
        inventario.actualizar_precio(1, "-5.00")
    assert inventario.obtener(1).precio == Decimal("35.00")


@pytest.mark.regla("RN-005")
def test_descuento_por_mayoreo(inventario):
    assert ventas.total(inventario, [(2, 12)]) == Decimal("70.20")
    assert ventas.total(inventario, [(2, 11)]) == Decimal("71.50")


@pytest.mark.regla("RN-007")
def test_articulo_con_nombre(inventario):
    with pytest.raises(ArticuloInvalido):
        inventario.crear("  ", "4.00")


def test_crud_de_articulos(inventario):
    a = inventario.crear("Goma", "4.00", piezas=1)
    inventario.actualizar_precio(a.id, "5.00")
    assert inventario.obtener(a.id).precio == Decimal("5.00")
    inventario.borrar(a.id)
    assert inventario.obtener(a.id) is None
