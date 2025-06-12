import platform
from pathlib import Path
from typing import Literal, Optional

from cached_config.exceptions import NoDefaultPathForPlatform


def int_or_none(value: Optional[str]) -> Optional[int]:
    """Restituisce il valore trasformato in intero o `None` se non e' numerico."""
    if value is None:
        return None

    try:
        return int(value.strip())
    except ValueError:
        return None


def hex_int_or_none(value: Optional[str]) -> Optional[int]:
    """Restituisce il valore esadecimale trasformato in intero o `None` se non e' valido."""
    if value is None:
        return None

    try:
        return int(value.strip(), 16)
    except ValueError:
        return None


def float_or_none(value: Optional[str]) -> Optional[float]:
    """Restituisce il valore trasformato in float o `None` se non e' numerico."""
    if value is None:
        return None

    try:
        return float(value.strip())
    except ValueError:
        return None


def get_platform() -> Literal["Linux", "Other"]:
    if platform.system() == "Linux":
        return "Linux"
    return "Other"


def get_cards_path() -> Path:
    """
    Restituisce il percorso di default del file `cards.txt`.
    Se la piattaforma non e' Linux restituisce un errore.
    """
    if get_platform() == "Linux":
        return Path("/home/pi/configs/cards.txt")
    raise NoDefaultPathForPlatform()


def get_timecards_path() -> Path:
    """
    Restituisce il percorso di default del file `timecards.txt`.
    Se la piattaforma non e' Linux restituisce un errore.
    """
    if get_platform() == "Linux":
        return Path("/home/pi/configs/timecards.txt")
    raise NoDefaultPathForPlatform()


def get_parameters_path() -> Path:
    """
    Restituisce il percorso di default del file `parameters.txt`.
    Se la piattaforma non e' Linux restituisce un errore.
    """
    if get_platform() == "Linux":
        return Path("/home/pi/configs/parameters.txt")
    raise NoDefaultPathForPlatform()
