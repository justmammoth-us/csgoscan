class FaceitProfileNotExistError(Exception):
    def __init__(self, games: str) -> None:
        self.msg = f"Faceit profile not existe for game {games}"
        super().__init__(self.msg)
