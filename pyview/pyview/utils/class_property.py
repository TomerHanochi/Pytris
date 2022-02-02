from typing import Any


class ClassPropertyDescriptor:
    def __init__(self, fget) -> None:
        self.fget = fget

    def __get__(self, obj, klass=None) -> Any:
        if klass is None:
            klass = type(obj)
        return self.fget.__get__(obj, klass)()


def classproperty(func) -> ClassPropertyDescriptor:
    if not isinstance(func, (classmethod, staticmethod)):
        func = classmethod(func)

    return ClassPropertyDescriptor(func)
