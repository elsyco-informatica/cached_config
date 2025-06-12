class UnimplementedException(Exception): ...


class NoDefaultPathForPlatform(Exception):
    def __init__(self) -> None:
        super().__init__(
            "Impossibile trovare il percorso di default per questa piattaforma"
        )
