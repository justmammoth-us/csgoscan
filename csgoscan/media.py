from enum import Enum

import requests
import xmltodict

from csgoscan.profile import FaceitProfile, Profile, SteamProfile
from csgoscan.settings import settings
from csgoscan.errors import FaceitProfileNotExistError


class Media:
    protocol: str = "https"
    name: str
    host: str
    path: str

    @classmethod
    @property
    def url_template(self) -> str:
        return f"{self.protocol}://{self.host}/{self.path}"

    @classmethod
    async def get_profile(cls, *args, **kwargs) -> Profile:
        return await cls._get_profile(cls.asdict(), *args, **kwargs)

    @staticmethod
    async def _get_profile(ctx: dict, steam_id: str) -> Profile:
        return Profile(ctx=ctx, id=steam_id)

    @classmethod
    def asdict(cls) -> dict:
        return {
            "protocol": cls.protocol,
            "name": cls.name,
            "host": cls.host,
            "path": cls.path,
            "url_template": cls.url_template,
        }


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
            avatar=profile.get("avatarFull"),
        )


class Faceit(Media):
    name: str = "Faceit"
    host: str = "faceit.com"
    path: str = "/en/players/{}"

    @classmethod
    async def _fetch_profile_by_game(cls, game: str, steam_id: str) -> dict:
        response = requests.get(
            f"https://open.faceit.com/data/v4/players?game={game}&game_player_id={steam_id}",
            headers={"Authorization": f"Bearer {settings.faceit_api_key}"},
        )

        if response.status_code == 404:
            raise FaceitProfileNotExistError(game)

        return response.json()

    @classmethod
    async def _is_profile_banned(cls, game: str, internal_id: str) -> bool:
        return False

    @classmethod
    async def _get_profile(cls, ctx, steam_id: str) -> FaceitProfile:
        try:
            game = "cs2"
            data = await cls._fetch_profile_by_game(game, steam_id)
        except FaceitProfileNotExistError:
            game = "csgo"
            data = await cls._fetch_profile_by_game(game, steam_id)

        games_data = data.get("games", {}).get(game)
        faceit_id = data.get("nickname")
        internal_id = data.get("player_id")

        banned = await cls._is_profile_banned(game, internal_id)

        return FaceitProfile(
            ctx=ctx,
            game=game,
            id=faceit_id,
            level=games_data.get("skill_level"),
            elo=games_data.get("faceit_elo"),
            internal_id=internal_id,
            games_played=0,
            country=data.get("country"),
            banned=banned,
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
