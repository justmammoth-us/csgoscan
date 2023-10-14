from abc import ABC
import asyncio
from dataclasses import dataclass
from typing import Optional
import requests
import xmltodict
from enum import Enum

from csgoscan.settings import settings


class Media(ABC):
    protocol: str = "https"
    name: str
    host: str
    path: str

    @classmethod
    @property
    def url_template(self):
        return f"{self.protocol}://{self.host}/{self.path}"

    @classmethod
    async def get_profile(cls, *args, **kwargs):
        return await cls._get_profile(cls, *args, **kwargs)

    @classmethod
    async def _get_profile(cls, ctx, *args, **kwargs):
        raise NotImplementedError()

    @classmethod
    async def test(cls, arg1):
        return arg1


@dataclass
class Profile:
    ctx: Media
    id: str

    def __post_init__(self):
        self.link: str = self.ctx.url_template.format(self.id)


@dataclass
class SteamProfile(Profile):
    alias: str
    name: str
    time_played: int


@dataclass
class FaceitProfile(Profile):
    level: int
    elo: int
    name: str
    games_played: str


class Steam(Media):
    class IDType(str, Enum):
        alias = "id"
        id = "profiles"

    name: str = "Steam"
    host: str = "steamcommunity.com"
    path: str = "profiles/{}"

    @classmethod
    async def _get_profile(
        cls, ctx, community_id: str, id_type: IDType
    ) -> SteamProfile:
        """Get an ID from an alias"""
        community_page = f"https://{cls.host}/{id_type.value}/{community_id}?xml=1"
        page = requests.get(community_page)
        steam_profile_dict = xmltodict.parse(page.content)

        profile = steam_profile_dict.get("profile")
        if not profile:
            raise Exception("No profile")

        return SteamProfile(
            ctx=ctx,
            id=profile.get("steamID64"),
            name=profile.get("steamID"),
            alias=profile.get("customURL"),
            time_played=0,
        )


class Faceit(Media):
    name: str = "Faceit Finder"
    host: str = "faceitfinder.com"
    path: str = "profile/{}"

    @classmethod
    async def _get_profile(cls, ctx, steam_id: str) -> FaceitProfile:
        page = requests.get(
            f"https://open.faceit.com/data/v4/players?game=cs2&game_player_id={steam_id}",
            headers={"Authorization": f"Bearer {settings.faceit_api_key}"},
        )
        data = page.json()

        cs2_data = data.get("games", {}).get("cs2")

        return FaceitProfile(
            ctx=ctx,
            id=data.get("nickname"),
            level=cs2_data.get("skill_level"),
            elo=cs2_data.get("faceit_elo"),
            name=data.get("nickname"),
            games_played=0,
        )


class CSGOBackpack(Media):
    name: str = "CSGO Backpack"
    host: str = "csgobackpack.net"
    path: str = "index.php?nick={}"


class FaceitFinder(Media):
    name: str = "Faceit Finder"
    host: str = "faceitfinder.com"
    path: str = "profile/{}"


class Leetify(Media):
    name: str = "Leetify"
    host: str = "leetify.com"
    path: str = "app/profile/{}"


class CSStats(Media):
    name: str = "CSStats"
    host: str = "csstats.gg"
    path: str = "player/{}"


class Player:
    steam: Steam
    medias: list[Media]

    def __init__(self, community_id: str, id_type: Steam.IDType) -> None:
        self.steam: str = Steam(community_id, id_type)
        self.id = steam.profile["id"]


#     def to_dict(self) -> dict:
#         return {
#             "steam": self.steam.to_dict(),
#             "medias": [m.to_string() for m in self.medias],
#         }


async def main():
    # print(await Steam.get_profile("jeje"))
    # steam = Steam()
    # faceit = Faceit()
    steam_player: SteamProfile = await Steam.get_profile(
        "76561198069504185", Steam.IDType.id
    )
    faceit_player: FaceitProfile = await Faceit.get_profile(steam_player.id)
    print(steam_player.link)
    print(faceit_player.link)
    # print(steam_player.link)


# print(steam.to_dict())

# faceit = Steam("76561198069504185", Steam.IDType.id)
# print(steam.to_dict())


asyncio.run(main())
