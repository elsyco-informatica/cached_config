try:
    from cached_config.cards import cards, timecards
except ImportError:
    from .cards import cards, timecards

try:
    from cached_config.parameters import parameters
except ImportError:
    from .parameters import parameters
