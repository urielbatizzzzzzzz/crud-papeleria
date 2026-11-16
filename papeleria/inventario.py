"""CRUD de artículos de la papelería (en memoria)."""
from dataclasses import dataclass
from decimal import Decimal


class SinExistencia(Exception):
    """No hay suficientes piezas del artículo."""


@dataclass
class Articulo:
    id: int
    nombre: str
    precio: Decimal
    piezas: int


class Inventario:
    def __init__(self) -> None:
        self._articulos: dict[int, Articulo] = {}
        self._siguiente = 1

    def crear(self, nombre: str, precio: str, piezas: int = 0) -> Articulo:
        articulo = Articulo(self._siguiente, nombre, Decimal(precio), piezas)
        self._articulos[articulo.id] = articulo
        self._siguiente += 1
        return articulo

    def obtener(self, articulo_id: int) -> Articulo | None:
        return self._articulos.get(articulo_id)

    def actualizar_precio(self, articulo_id: int, precio: str) -> None:
        self._articulos[articulo_id].precio = Decimal(precio)

    def sacar(self, articulo_id: int, piezas: int) -> None:
        articulo = self._articulos[articulo_id]
        if piezas > articulo.piezas:
            raise SinExistencia(f"Solo hay {articulo.piezas} de {articulo.nombre}")
        articulo.piezas -= piezas

    def borrar(self, articulo_id: int) -> None:
        del self._articulos[articulo_id]
