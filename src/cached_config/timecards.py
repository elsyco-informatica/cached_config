import datetime
import enum
from dataclasses import dataclass
from io import TextIOWrapper
from pathlib import Path
from typing import Dict, Optional

from cached_config.cached_file import CachedFile
from cached_config.utils import get_timecards_path


@dataclass
class _TimeRange:
    start: datetime.time
    end: datetime.time

    @staticmethod
    def parse(line: str) -> Optional["_TimeRange"]:
        line_split = line.strip().split("-")
        if len(line_split) != 2:
            return None

        try:
            start = datetime.datetime.strptime(line_split[0], "%H:%M").time()
            end = (
                datetime.datetime.strptime(line_split[1], "%H:%M")
                .time()
                .replace(second=59, microsecond=999999)
            )
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
    expiration: datetime.date


class TimecardCheckResult(enum.Enum):
    FOUND = 0
    NOT_FOUND = 1
    OUTSIDE_DATE = 2
    OUTSIDE_TIME = 3


class TimecardsFile(CachedFile[Dict[str, _CardEntry]]):
    def __init__(self, path: Optional[Path]) -> None:
        """Classe per il controllo del contenuto del file `timecards.txt`."""
        if path is None:
            path = get_timecards_path()

        super().__init__(path, {})

    def parse_file(self, file: TextIOWrapper) -> Dict[str, _CardEntry]:
        dict: Dict[str, _CardEntry] = {}
        for line in file:
            split_line = line.strip().split("=", 1)
            card = split_line[0].strip()
            if len(split_line) == 2:
                desc = split_line[1].strip()
            else:
                desc = ""

            split_card = card.split("|")
            if len(split_card) != 3:
                continue

            card = split_card[0].strip()
            time_range = _TimeRange.parse(split_card[1].strip())
            if time_range is None:
                continue

            try:
                expiration = datetime.datetime.strptime(
                    split_card[2].strip(), "%d/%m/%Y"
                ).date()
            except ValueError:
                continue

            dict[card] = _CardEntry(card, desc, time_range, expiration)

        return dict

    def check(self, card: str) -> TimecardCheckResult:
        """
        Controlla che la tessera sia presente all'interno del file.

        :param card: Il codice della tessera
        """
        data = self.cache
        if card not in data:
            return TimecardCheckResult.NOT_FOUND

        entry = data[card]
        if entry.expiration < datetime.datetime.now().date():
            return TimecardCheckResult.OUTSIDE_DATE

        if (
            entry.time_range.start
            <= datetime.datetime.now().time()
            <= entry.time_range.end
        ):
            return TimecardCheckResult.FOUND

        return TimecardCheckResult.OUTSIDE_TIME
