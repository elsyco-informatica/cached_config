import time
import unittest
from pathlib import Path
from typing import Dict, Optional

from cached_file import CachedFile
from cards import CardsFile
from parameters import ParametersFile
from timecards import TimecardCheckResult, TimecardsFile


class TestFile(CachedFile[Dict[str, str]]):
    def __init__(self):
        super().__init__(Path("./file.txt"))

    def parse_file(self, file) -> Dict[str, str]:
        dict = {}

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


class TestCachedFile(unittest.TestCase):
    def test_cached_file(self):
        path = Path("./file.txt")
        with open(path, "w") as file:
            file.write("1\nPAR1=3\n")

        test_file = TestFile()

        assert test_file.get("PAR1") == "3"
        last_read = test_file._last_read_at
        time.sleep(1)

        assert test_file.get("PAR1") == "3"
        assert test_file._last_read_at == last_read

        with open(path, "w") as file:
            file.write("1\nPAR1=4")

        assert test_file.get("PAR1") == "4"

    def test_parameters_file(self):
        path = Path("./file.txt")
        with open(path, "w") as file:
            file.write("1\nPAR1=3\n")

        param = ParametersFile(Path("./file.txt"))
        last_read = param._last_read_at

        assert param.int_par("PAR1") == 3
        time.sleep(1)
        assert param.int_par("PAR1") == 3
        assert param._last_read_at == last_read

        with open(path, "w") as file:
            file.write("1\nPAR1=4")

        assert param.int_par("PAR1") == 4

    def test_cards_file(self):
        path = Path("./file.txt")
        with open(path, "w") as file:
            file.write("00250001152225=\n25001849322552=\n")

        cards = CardsFile(Path("./file.txt"))

        assert cards.contains("00250001152225")
        last_read = cards._last_read_at
        time.sleep(1)

        assert cards.contains("25001849322552")
        assert cards._last_read_at == last_read

        with open(path, "w") as file:
            file.write("25001849322552=\n")

        assert not cards.contains("00250001152225")
        assert cards.contains("25001849322552")

    def test_timecards_file(self):
        path = Path("./file.txt")
        with open(path, "w") as file:
            file.write(
                "00250001152225|09:00-18:00|31/12/2025=VALIDA\n"
                "25001849322552|09:00-18:00|31/12/2024=SCAD_DATA\n"
            )

        timecards = TimecardsFile(Path("./file.txt"))

        assert timecards.check("00250001152225") is TimecardCheckResult.FOUND
        last_read = timecards._last_read_at
        time.sleep(1)

        assert timecards.check("25001849322552") is TimecardCheckResult.OUTSIDE_DATE
        assert timecards._last_read_at == last_read

        with open(path, "w") as file:
            file.write(
                "12562548912455|09:00-16:00|31/12/2025=SCAD_ORA\n"
                "12566311942455|09000|31/12/2025=IGNORATA\n"
                "12549548452455|09000|31/2025=IGNORATA\n"
            )

        assert timecards.check("12562548912455") is TimecardCheckResult.OUTSIDE_TIME
        assert timecards.check("12566311942455") is TimecardCheckResult.NOT_FOUND
        assert timecards.check("12549548452455") is TimecardCheckResult.NOT_FOUND


if __name__ == "__main__":
    unittest.main()
