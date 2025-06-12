from io import TextIOWrapper
from pathlib import Path
from typing import Dict, Optional

from cached_config.cached_file import CachedFile
from cached_config.utils import get_cards_path


class CardsFile(CachedFile[Dict[str, str]]):
    def __init__(self, path: Optional[Path]) -> None:
        """Classe per il controllo del contenuto del file `cards.txt`."""
        if path is None:
            path = get_cards_path()

        super().__init__(path, {})

    def parse_file(self, file: TextIOWrapper) -> Dict[str, str]:
        dict: Dict[str, str] = {}
        for line in file:
            split_line = line.strip().split("=", 1)
            card = split_line[0]
            if len(split_line) == 2:
                desc = split_line[1]
            else:
                desc = ""

            dict[card] = desc

        return dict

    def contains(self, card: str) -> bool:
        """Controlla che la tessera sia presente all'interno del file."""
        return card in self.cache
