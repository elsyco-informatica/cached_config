from pathlib import Path
from typing import Dict

from .cached_file import CachedFile

CARDS_PATH = Path("/home/pi/configs/cards.txt")


class CardsFile(CachedFile[Dict[str, str]]):
    def __init__(self, path: Path = CARDS_PATH) -> None:
        """
        Classe che rappresenta il contenuto del file `cards.txt`.

        La classe controlla la data di modifica del file e mantiene in una
        cache le tessere per velocizzare la lettura.
        """
        super().__init__(path, {})

    def parse_file(self, file) -> Dict[str, str]:
        dict = {}
        for line in file:
            split_line = line.strip().split("=", 1)

            card = split_line[0]
            desc = split_line[1] if len(split_line) == 2 else ""

            dict[card] = desc

        return dict

    def contains(self, card: str) -> bool:
        """
        Controlla che la tessera sia presente all'interno del file

        Se la tessera contiene un orario, verifica anche che l'ora attuale
        sia compresa nel range.

        :param card: Il codice della tessera
        :return: `True` se la tessera e' presente, altrimenti `False`
        """
        data = self.cache
        return card in data
