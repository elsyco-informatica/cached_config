try:
    from cached_config.cards import CARDS_PATH, CardsFile
except ImportError:
    from .cards import CARDS_PATH, CardsFile

try:
    from cached_config.timecards import (
        TIMECARDS_PATH,
        TimecardCheckResult,
        TimecardsFile,
    )
except ImportError:
    from .timecards import TIMECARDS_PATH, TimecardCheckResult, TimecardsFile

try:
    from cached_config.parameters import ParametersFile
except ImportError:
    from .parameters import ParametersFile

try:
    from cached_config.cached_file import CachedFile
except ImportError:
    from .cached_file import CachedFile
