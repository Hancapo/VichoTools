from typing import Any, Type, TypeVar

_TEnum = TypeVar("_TEnum", bound="Enum")

class Enum:
    @classmethod
    def GetName(cls, enumType: Type[_TEnum], value: Any) -> str | None: ...
    @classmethod
    def GetNames(cls, enumType: Type[_TEnum]) -> list[str]: ...
    @classmethod
    def GetValues(cls, enumType: Type[_TEnum]) -> list[Any]: ...
    @classmethod
    def Parse(cls, enumType: Type[_TEnum], value: str) -> _TEnum: ...
    @classmethod
    def IsDefined(cls, enumType: Type[_TEnum], value: Any) -> bool: ...

class UInt32(int):
    MinValue: int
    MaxValue: int
    def __new__(cls, value: int = ...) -> "UInt32": ...
