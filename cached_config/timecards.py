from dataclasses import dataclass
from datetime import date, datetime, time
from enum import Enum
from pathlib import Path
from typing import Dict, Union

from .cached_file import CachedFile

TIMECARDS_PATH = Path("/home/pi/configs/cards.txt")


@dataclass
class _TimeRange:
    start: time
    end: time

    @staticmethod
    def parse(line: str) -> Union["_TimeRange", None]:
        line_split = line.split("-")
        if len(line_split) != 2:
            return None

        try:
            start = datetime.strptime(line_split[0], "%H:%M").time()
            end = datetime.strptime(line_split[1], "%H:%M").time()
        except ValueError:
            return None

        if start > end:
            return None

        return _TimeRange(start, end)


@dataclass
class _CardEntry:
    card: str
    desc: str
    time_range: _TimeRange
    expiration: date


class TimecardCheckResult(Enum):
    FOUND = 0
    NOT_FOUND = 1
    OUTSIDE_DATE = 2
    OUTSIDE_TIME = 3


class TimecardsFile(CachedFile[Dict[str, _CardEntry]]):
    def __init__(self, path: Path = TIMECARDS_PATH) -> None:
        """
        Classe che rappresenta il contenuto del file `cards.txt`.

        La classe controlla la data di modifica del file e mantiene in una
        cache le tessere per velocizzare la lettura.
        """
        super().__init__(path)

    def parse_file(self, file) -> Dict[str, _CardEntry]:
        dict = {}
        for line in file:
            split_line = line.strip().split("=", 1)

            card = split_line[0].strip()
            desc = split_line[1].strip() if len(split_line) == 2 else ""

            split_card = card.split("|")
            if len(split_card) != 3:
                continue

            card = split_card[0].strip()
            time_range = _TimeRange.parse(split_card[1].strip())
            if time_range is None:
                continue

            try:
                expiration = datetime.strptime(split_card[2].strip(), "%d/%m/%Y").date()
            except ValueError:
                continue

            dict[card] = _CardEntry(card, desc, time_range, expiration)

        return dict

    def check(self, card: str) -> TimecardCheckResult:
        """
        Controlla che la tessera sia presente all'interno del file

        Se la tessera contiene un orario, verifica anche che l'ora attuale
        sia compresa nel range.

        :param card: Il codice della tessera
        :return: `True` se la tessera e' presente, altrimenti `False`
        """
        data = self.cache
        if card not in data:
            return TimecardCheckResult.NOT_FOUND

        entry = data[card]
        if entry.expiration < datetime.now().date():
            return TimecardCheckResult.OUTSIDE_DATE

        if entry.time_range.start <= datetime.now().time() <= entry.time_range.end:
            return TimecardCheckResult.FOUND

        return TimecardCheckResult.OUTSIDE_TIME
