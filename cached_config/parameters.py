from pathlib import Path
from typing import Dict, List, Union

from .cached_file import CachedFile
from .utils import float_or_none, hex_int_or_none, int_or_none

PARAMETERS_PATH = Path("/home/pi/configs/parameters.txt")


class ParametersFile(CachedFile[Dict[str, str]]):
    def __init__(self, path: Path = PARAMETERS_PATH) -> None:
        """
        Una classe per il recupero dei parametri dal file `parameters.txt`.

        La classe controlla la data di modifica del file e mantiene in una
        cache i parametri per velocizzare la lettura.
        """
        super().__init__(path, {})

    def parse_file(self, file) -> Dict[str, str]:
        dict = {}
        for line in file:
            if line.find("=") > -1:
                if line.find("=") > -1:
                    [key, value] = line.split("=", 1)
                    dict[key.strip().upper()] = value.strip()

        return dict

    def _get(self, name: str) -> Union[str, None]:
        """
        Restituisce il parametro o `None` se non e' presente.

        Se il file e' stato modificato ricarica il contenuto

        :param name: Nome del parametro richiesto
        """
        data = self.cache

        name = name.upper()
        if name in data:
            return data[name].strip()
        return None

    def par(self, name: str) -> Union[str, None]:
        """Restituisce il parametro richiesto."""
        return self._get(name)

    def par_or_none(self, name: str) -> Union[str, None]:
        par = self._get(name)
        if par is None or par.strip() == "":
            return None

        return par

    def int_par(self, name: str) -> Union[int, None]:
        """
        Restituisce il parametro intero richiesto o `None` se non esiste o
        non e' numerico.
        """
        par = self._get(name)
        if par is not None:
            try:
                return int(par)
            except ValueError:
                return None

        return None

    def hex_par(self, name: str) -> Union[int, None]:
        """
        Restituisce il parametro intero richiesto leggendolo come esadecimale,
        altrimenti `None` se non esiste o non e' in forma esadecimale.
        """
        par = self._get(name)
        if par is not None:
            try:
                return int(par, 16)
            except ValueError:
                return None
        return None

    def float_par(self, name: str) -> Union[float, None]:
        """
        Restituisce il parametro intero richiesto leggendolo come float,
        altrimenti `None` se non esiste o non e' in forma numerica.
        """
        par = self._get(name)
        if par is not None:
            try:
                return float(par)
            except ValueError:
                return None
        return None

    def bool_par(self, name: str) -> Union[bool, None]:
        """
        Restituisce il parametro booleano richiesto, altrimenti `None` se non
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

    def list_par(self, name: str) -> Union[List[str], None]:
        """
        Restituisce un parametro in forma `List[str]` o `None` se non esiste.
        """
        par = self._get(name)
        if par is None:
            return None

        return [par.strip() for par in par.split(",")]

    def par_list(self, *names: str) -> List[Union[str, None]]:
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

    def int_list_par(self, name: str) -> Union[List[int], None]:
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

    def int_par_list(self, *names) -> List[Union[int, None]]:
        """
        Restituisce una lista di parametri in forma `int | None`.
        """
        return [int_or_none(self._get(name)) for name in names]

    def hex_list_par(self, name: str) -> Union[List[int], None]:
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

    def hex_par_list(self, *names: str) -> List[Union[int, None]]:
        """
        Restituisce una lista di parametri esadecimali in forma `List[int] | None`.
        """
        return [hex_int_or_none(self._get(name)) for name in names]

    def float_list_par(self, name: str) -> Union[List[float], None]:
        """
        Restituisce un parametro in forma `List[float]` o `None` se non esiste.

        I valori della lista non float sono ignorati.
        """
        par = self._get(name)
        if par is None:
            return None

        return [par for el in par.split(",") if (par := float_or_none(el)) is not None]

    def float_par_list(self, *names: str) -> List[Union[float, None]]:
        """
        Restituisce una lista di parametri in forma `float | None`.
        """
        return [float_or_none(self._get(name)) for name in names]
