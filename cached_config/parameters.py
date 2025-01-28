from pathlib import Path
from typing import Dict, List, Optional, Union

from cached_config.utils import float_or_none, hex_int_or_none, int_or_none

PARAMETERS_PATH = Path("/home/pi/configs/parameters.txt")


class Parameters:
    def __init__(self):
        """
        Una classe per il recupero dei parametri dal file `parameters.txt`.

        La classe controlla la data di modifica del file e mantiene in una
        cache i parametri per velocizzare la lettura.
        """

        self._dict: Dict[str, str] = {}
        self._timestamp: Optional[float] = None

        self._reload()

    def _should_reload(self):
        # Se il file `parameters.txt` esiste ed e' stato modificato
        return (
            PARAMETERS_PATH.exists()
            and self._timestamp != PARAMETERS_PATH.stat().st_mtime
        )

    def _reload(self):
        # Se il file e' stato modificato lo rileggo
        if PARAMETERS_PATH.exists():
            with open(PARAMETERS_PATH, "r", encoding="utf-8") as file:
                lines = file.readlines()

            # Memorizzo la data di modifica del file
            Parameters._timestamp = PARAMETERS_PATH.stat().st_mtime
            for line in lines:
                # Per ogni linea del file divido in base al primo carattere "="
                # che trovo
                if line.find("=") > -1:
                    [key, value] = line.split("=", 1)
                    self._dict[key.strip().upper()] = value.strip()

    def _get(self, name: str):
        """
        Restituisce il parametro o `None` se non e' presente.

        Se il file e' stato modificato ricarica il contenuto

        :param name: Nome del parametro richiesto
        """
        if self._should_reload():
            self._reload()

        name = name.upper()
        if name in self._dict:
            return self._dict[name].strip()
        return None

    def par(self, name: str):
        """Restituisce il parametro richiesto."""
        return self._get(name)

    def par_or_none(self, name: str):
        par = self._get(name)
        if par is None or par.strip() == "":
            return None

        return par

    def int_par(self, name: str):
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

    def hex_par(self, name: str):
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

    def float_par(self, name: str):
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

    def bool_par(self, name: str):
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


parameters = Parameters()
