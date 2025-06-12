from io import TextIOWrapper
from pathlib import Path
from typing import Generic, Optional, TypeVar

from cached_config.exceptions import UnimplementedException

_T = TypeVar("_T")


class CachedFile(Generic[_T]):
    def __init__(self, path: Path, default: _T) -> None:
        """
        Classe che rappresenta il contentuto di un file che deve essere mantenuto
        nella cache.

        La classe controlla la data di modifica del file e mantiene in una cache
        il contentuto per velocizzare la lettura.
        """

        self._path = path
        self._cache = default

        self._last_read_at: Optional[float] = None
        """L'ultimo momento in cui il file e' stato letto."""

    @property
    def last_read_at(self) -> Optional[float]:
        return self._last_read_at

    def parse_file(self, file: TextIOWrapper) -> _T:
        """Legge il file e restituisce il contenuto."""
        raise UnimplementedException()

    def should_reload(self) -> bool:
        """Restituisce `True` se il file e' stato modificato dall'ultima lettura."""
        return self._path.exists() and self._last_read_at != self._path.stat().st_mtime

    @property
    def cache(self) -> _T:
        if self.should_reload():
            with open(self._path, "r", encoding="utf-8") as file:
                self._cache = self.parse_file(file)

        return self._cache
