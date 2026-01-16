import time
from datetime import datetime, timedelta
from io import TextIOWrapper
from pathlib import Path
from typing import Dict, Optional

from cached_config.cached_file import CachedFile
from cached_config.cards import CardsFile
from cached_config.parameters import ParametersFile
from cached_config.timecards import TimecardCheckResult, TimecardsFile


class TestFile(CachedFile[Dict[str, str]]):
    __test__ = False

    def __init__(self, path: Path):
        super().__init__(path, {})

    def parse_file(self, file: TextIOWrapper) -> Dict[str, str]:
        dict: Dict[str, str] = {}
        for line in file:
            if "=" not in line.strip():
                continue

            parts = line.strip().split("=")
            dict[parts[0]] = parts[1]

        return dict

    def get(self, key: str) -> Optional[str]:
        content = self.cache
        if key in content:
            return content[key]
        return None


def test_cached_file(tmp_path: Path):
    path = tmp_path / "file.txt"
    with open(path, "w") as file:
        file.write("1\nPAR1=3\n")

    test_file = TestFile(path)

    assert test_file.get("PAR1") == "3"
    last_read = test_file.last_read_at
    time.sleep(1)

    assert test_file.get("PAR1") == "3"
    assert test_file.last_read_at == last_read

    with open(path, "w") as file:
        file.write("1\nPAR1=4")

    assert test_file.get("PAR1") == "4"
    assert test_file.last_read_at == path.stat().st_mtime


def test_parameters_file(tmp_path: Path):
    path = tmp_path / "file.txt"
    with open(path, "w") as file:
        file.write("1\nPAR1=3\n")

    param = ParametersFile(path)
    assert param.last_read_at is None

    assert param.int_par("PAR1") == 3
    time.sleep(1)
    assert param.int_par("PAR1") == 3
    assert param.last_read_at is not None

    with open(path, "w") as file:
        file.write("1\nPAR1=4")

    assert param.int_par("PAR1") == 4
    assert param.last_read_at == path.stat().st_mtime


def test_cards_file(tmp_path: Path):
    path = tmp_path / "file.txt"
    with open(path, "w") as file:
        file.write("00250001152225=\n25001849322552=\n")

    cards = CardsFile(path)

    assert cards.contains("00250001152225")
    last_read = cards.last_read_at
    time.sleep(1)

    assert cards.contains("25001849322552")
    assert cards.last_read_at == last_read

    with open(path, "w") as file:
        file.write("25001849322552=\n")

    assert not cards.contains("00250001152225")
    assert cards.contains("25001849322552")
    assert cards.last_read_at == path.stat().st_mtime


def test_timecards_file(tmp_path: Path):
    path = tmp_path / "file.txt"
    valid_date = (datetime.now() + timedelta(days=3)).strftime("%d/%m/%Y")
    with open(path, "w") as file:
        file.write(
            f"00250001152225|09:00-18:00|{valid_date}=VALIDA\n"
            "25001849322552|09:00-18:00|31/12/2024=SCAD_DATA\n"
        )

    timecards = TimecardsFile(path)

    assert timecards.check("00250001152225") is TimecardCheckResult.FOUND
    last_read = timecards.last_read_at
    time.sleep(1)

    assert timecards.check("25001849322552") is TimecardCheckResult.OUTSIDE_DATE
    assert timecards.last_read_at == last_read

    valid_date = (datetime.now() + timedelta(days=3)).strftime("%d/%m/%Y")

    time_start = datetime.now() - timedelta(hours=2)
    time_end = time_start + timedelta(hours=1)

    with open(path, "w") as file:
        file.write(
            f"12562548912455|{time_start.strftime('%H:%M')}-{time_end.strftime('%H:%M')}|{valid_date}=SCAD_ORA\n"
            "12566311942455|09000|31/12/2025=IGNORATA\n"
            "12549548452455|09000|31/2025=IGNORATA\n"
        )

    assert timecards.check("12562548912455") is TimecardCheckResult.OUTSIDE_TIME
    assert timecards.check("12566311942455") is TimecardCheckResult.NOT_FOUND
    assert timecards.check("12549548452455") is TimecardCheckResult.NOT_FOUND
    assert timecards.last_read_at == path.stat().st_mtime
