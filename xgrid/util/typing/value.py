import ctypes
from dataclasses import dataclass
from xgrid.util.typing import BaseType


@dataclass
class Value(BaseType):
    pass


@dataclass
class Void(Value):
    def __repr__(self) -> str:
        return "Void"


@dataclass
class Boolean(Value):
    @property
    def ctype(self):
        return ctypes.c_bool

    def serialize(self, value):
        return ctypes.c_bool(value)

    def __repr__(self) -> str:
        return "Boolean"


@dataclass
class Number(Value):
    width_bytes: int

    @property
    def width_bits(self) -> int:
        return self.width_bytes * 8

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.width_bits})"


@dataclass
class Integer(Number):
    __concrete_typing__ = True

    def __post_init__(self):
        assert self.width_bytes in (0, 1, 2, 4, 8)
        self._ctype = {1: ctypes.c_int8, 2: ctypes.c_int16,
                       4: ctypes.c_int32, 8: ctypes.c_int64}[self.width_bytes]

    @property
    def ctype(self):
        return self._ctype

    def serialize(self, value):
        return self._ctype(value)


@dataclass
class Floating(Number):
    __concrete_typing__ = True

    def __post_init__(self):
        assert self.width_bytes in (4, 8)
        self._ctype = ctypes.c_float if self.width_bytes == 4 else ctypes.c_double

    @property
    def ctype(self):
        return self._ctype

    def serialize(self, value):
        return self._ctype(value)


@dataclass
class Structure(Value):
    __concrete_typing__ = True

    dataclass: type
    name: str
    elements: tuple[tuple[str, Value], ...]

    def __post_init__(self):
        self.elements_map = dict(self.elements)

    @property
    def ctype(self):
        return super().ctype

    def serialize(self, value):
        # TODO: Implement serialize and deserialize for structure type
        return super().serialize(value)

    def deserialize(self, value):
        return super().deserialize(value)

    def __repr__(self) -> str:
        return self.name