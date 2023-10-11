from dataclasses import dataclass, field


@dataclass
class Profile:
    id: str
    name: str
    alias: str | None = None
    links: list[dict] = field(default_factory=list)
