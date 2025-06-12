from io import TextIOWrapper
from pathlib import Path
from typing import Dict, List, Optional

from cached_config.cached_file import CachedFile
from cached_config.utils import (
    float_or_none,
    get_parameters_path,
    hex_int_or_none,
    int_or_none,
)


class ParametersFile(CachedFile[Dict[str, str]]):
    def __init__(self, path: Optional[Path] = None) -> None:
        """Una classe per il controllo del contenuto del file `parameters.txt`."""
        if path is None:
            path = get_parameters_path()

        super().__init__(path, {})

    def parse_file(self, file: TextIOWrapper) -> Dict[str, str]:
        dict: Dict[str, str] = {}
        for line in file:
            if "=" in line:
                [key, value] = line.split("=", 1)
                dict[key.strip().upper()] = value.strip()

        return dict

    def _get(self, name: str) -> Optional[str]:
        """Restituisce il parametro o `None` se non e' presente."""
        data = self.cache
        name = name.upper()
        if name in data:
            return data[name].strip()
        return None

    def par(self, name: str) -> Optional[str]:
        """Resttuisce il parametro richiesto."""
        return self._get(name)

    def par_or_none(self, name: str) -> Optional[str]:
        """Restituisce il parametro o `None` se non esiste o e' vuoto."""
        par = self._get(name)
        if par is None or par.strip() == "":
            return None
        return par

    def int_par(self, name: str) -> Optional[int]:
        """
        Restituisce il parametro intero o `None` se non esiste o
        non e' numerico.
        """
        par = self._get(name)
        if par is not None:
            try:
                return int(par)
            except ValueError:
                return None

        return None

    def hex_par(self, name: str) -> Optional[int]:
        """
        Restituisce il parametro intero da esadecimale, o `None` se non esiste o
        non e' valido.
        """
        par = self._get(name)
        if par is not None:
            try:
                return int(par, 16)
            except ValueError:
                return None
        return None

    def float_par(self, name: str) -> Optional[float]:
        """
        Restituisce il parametro float altrimenti `None` se non esiste o
        non e' valido.
        """
        par = self._get(name)
        if par is not None:
            try:
                return float(par)
            except ValueError:
                return None
        return None

    def bool_par(self, name: str) -> Optional[bool]:
        """
        Restituisce il parametro bool, altrimenti `None` se non
        esiste o non e' in forma booleana.
        """
        par = self._get(name)
        if par is None:
            return None

        if par == "1" or par.capitalize() == "S" or par.capitalize() == "TRUE":
            return True
        elif par == "0" or par.capitalize() == "N" or par.capitalize() == "FALSE":
            return False
        else:
            return None

    def list_par(self, name: str) -> Optional[List[str]]:
        """
        Restituisce un parametro in forma `List[str]` o `None` se non esiste.
        """
        par = self._get(name)
        if par is None:
            return None

        return [par.strip() for par in par.split(",")]

    def par_list(self, *names: str) -> List[Optional[str]]:
        """
        Restituisce una lista di parametri in forma `str | None`.
        """
        return [self._get(name) for name in names]

    def par_not_empty_list(self, *names: str) -> List[str]:
        """
        Restituisce una lista di parametri solo se esistono e non sono vuoti.
        """
        return [
            par
            for name in names
            if (par := self._get(name)) is not None and par.strip() != ""
        ]

    def int_list_par(self, name: str) -> Optional[List[int]]:
        """
        Restituisce un parametro in forma `List[int]` o `None` se non esiste.

        I valori della lista non interi sono ignorati.
        """
        par = self._get(name)
        if par is None:
            return None

        return [
            parsed for el in par.split(",") if (parsed := int_or_none(el)) is not None
        ]

    def int_par_list(self, *names: str) -> List[Optional[int]]:
        """
        Restituisce una lista di parametri in forma `int | None`.
        """
        return [int_or_none(self._get(name)) for name in names]

    def hex_list_par(self, name: str) -> Optional[List[int]]:
        """
        Restituisce un parametro esadecimale in forma `List[int]` o `None` se non esiste.

        I valori della lista non esadecimali sono ignorati.
        """
        par = self._get(name)
        if par is None:
            return None

        return [
            parsed
            for el in par.split(",")
            if (parsed := hex_int_or_none(el)) is not None
        ]

    def hex_par_list(self, *names: str) -> List[Optional[int]]:
        """
        Restituisce una lista di parametri esadecimali in forma `List[int] | None`.
        """
        return [hex_int_or_none(self._get(name)) for name in names]

    def float_list_par(self, name: str) -> Optional[List[float]]:
        """
        Restituisce un parametro in forma `List[float]` o `None` se non esiste.

        I valori della lista non float sono ignorati.
        """
        par = self._get(name)
        if par is None:
            return None

        return [par for el in par.split(",") if (par := float_or_none(el)) is not None]

    def float_par_list(self, *names: str) -> List[Optional[float]]:
        """
        Restituisce una lista di parametri in forma `float | None`.
        """
        return [float_or_none(self._get(name)) for name in names]
