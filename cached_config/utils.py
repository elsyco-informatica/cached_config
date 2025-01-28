from typing import Union


def int_or_none(value: Union[str, None]) -> Union[int, None]:
    """
    Restituisce il valore trasformato in intero o `None` se non e' numerico.
    """
    if value is None:
        return None

    try:
        return int(value.strip())
    except ValueError:
        return None


def hex_int_or_none(value: Union[str, None]) -> Union[int, None]:
    """
    Restituisce il valore esadecimale trasformato in intero o `None` se non e' valido.
    """
    if value is None:
        return None

    try:
        return int(value.strip(), 16)
    except ValueError:
        return None


def float_or_none(value: Union[str, None]) -> Union[float, None]:
    """
    Restituisce il valore trasformato in float o `None` se non e' numerico.
    """

    if value is None:
        return None

    try:
        return float(value.strip())
    except ValueError:
        return None
