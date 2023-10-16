from dataclasses import dataclass, field


@dataclass
class Profile:
    ctx: dict
    id: str
    link: str = field(init=False)

    def __post_init__(self):
        self.link: str = self.ctx.get("url_template", "").format(self.id)


@dataclass
class SteamProfile(Profile):
    alias: str
    name: str
    avatar: str
    time_played: int
    last_weeks_time_played: int


@dataclass
class FaceitProfile(Profile):
    level: int
    elo: int
    internal_id: str
    games_played: str
    game: str
    country: str
    banned: bool
