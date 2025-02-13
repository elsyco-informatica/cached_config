import datetime
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, Optional, Tuple

CARDS_PATH = Path("/home/pi/configs/cards.txt")
TIMECARDS_PATH = Path("/home/pi/configs/timecards.txt")


@dataclass
class _TimeFrame:
    start: Optional[datetime.time]
    end: Optional[datetime.time]
    invalid: bool = False

    @staticmethod
    def parse(line: str) -> "_TimeFrame":
        line_split = line.split("-")
        if len(line_split) != 2:
            return _TimeFrame(None, None, invalid=True)

        try:
            start = datetime.datetime.strptime(line_split[0], "%H:%M")
            end = datetime.datetime.strptime(line_split[1], "%H:%M")
        except ValueError:
            return _TimeFrame(None, None, invalid=True)

        return _TimeFrame(start.time(), end.time())

    @property
    def range(self) -> Tuple[datetime.time, datetime.time]:
        assert self.start and self.end
        return (self.start, self.end)


@dataclass
class _CardEntry:
    card: str
    time_frame: Optional[_TimeFrame] = None


class CardStatus(Enum):
    FOUND = 0
    NOT_FOUND = 1
    OUTSIDE_TIME = 2


class Cards:
    def __init__(self, path=CARDS_PATH):
        """
        Classe che rappresenta il contenuto del file `cards.txt`.

        La classe controlla la data di modifica del file e mantiene in una
        cache le tessere per velocizzare la lettura.
        """

        self._path = path
        self._list: List[_CardEntry] = []
        self._timestamp: Optional[float] = None

        self._reload()

    def _should_reload(self):
        # Se il file `cards.txt` esiste ed e' stato modificato
        return self._path.exists() and self._timestamp != self._path.stat().st_mtime

    def _reload(self):
        # Se il file e' stato modificato lo rileggo
        self._list = []
        if self._path.exists():
            with open(self._path, "r", encoding="utf-8") as file:
                lines = file.readlines()

            self._timestamp = self._path.stat().st_mtime
            for line in lines:
                split_line = line.strip().split("=", 1)

                card = split_line[0]
                _desc = split_line[1] if len(split_line) == 2 else ""

                split_card = card.split("|")
                if len(split_card) == 1:
                    entry = _CardEntry(card.strip())
                else:
                    entry = _CardEntry(
                        split_card[0].strip(), _TimeFrame.parse(split_card[1])
                    )

                self._list.append(entry)

    def contains(self, card: str) -> CardStatus:
        """
        Controlla che la tessera sia presente all'interno del file

        Se la tessera contiene un orario, verifica anche che l'ora attuale
        sia compresa nel range.

        :param card: Il codice della tessera
        :return: `True` se la tessera e' presente, altrimenti `False`
        """
        if self._should_reload():
            self._reload()

        for entry in self._list:
            if entry.card == card:
                if entry.time_frame is None:
                    return CardStatus.FOUND

                if entry.time_frame.invalid:
                    return CardStatus.OUTSIDE_TIME

                start, end = entry.time_frame.range
                now = datetime.datetime.now().time()
                if start <= now <= end:
                    return CardStatus.FOUND
                else:
                    return CardStatus.OUTSIDE_TIME

        return CardStatus.NOT_FOUND


cards = Cards()
timecards = Cards(TIMECARDS_PATH)
