from dataclasses import dataclass, asdict
from enum import Enum
import requests
import xmltodict
from csgoscan.settings import settings


class IDType(str, Enum):
    alias = "id"
    id = "profiles"


@dataclass
class Website:
    name: str
    host: str
    profile_path: str
    protocol: str = "https"

    def __post_init__(self):
        self.home_url = f"{self.protocol}://{self.host}/"
        self.profile_url = self.home_url + self.profile_path
    
    # def to_dict(self):
    #     return {
    #         "name":self.name,
    #         "host":self.host,
    #         "profile_path": self.profile_path,
    #         "protocol": self.protocol,
    #         "home_url": self.home_url,
    #         "profile_url": self.profile_url
    #     }


websites = {
    "steam": Website(
        name="Steam",
        host="steamcommunity.com",
        profile_path="profiles/{}",
    ),
    "faceit_finder": Website(
        name="Faceit Finder",
        host="faceitfinder.com",
        profile_path="profile/{}",
    ),
    "cs_stats": Website(
        name="CSStats",
        host="csstats.gg",
        profile_path="player/{}",
    ),
    "csgo_backpack": Website(
        name="CSGO Backpack",
        host="csgobackpack.net",
        profile_path="index.php?nick={}",
    ),
    "leetify": Website(
        name="Leetify",
        host="leetify.com",
        profile_path="app/profile/{}",
    ),
    "faceit": Website(
        name="Faceit",
        host="faceit.com",
        profile_path="en/players/{}",
    ),
}


class ProfileBase:
    def __init__(self, id: str, website: Website):
        self.id = id
        self.website = website
        self.link = self.website.profile_url.format(self.id)

    def to_dict(self) -> dict:
        return {"id": self.id, "link": self.link, "website": asdict(self.website)}


class SteamProfile(ProfileBase):
    def __init__(self, id: str, name: str, alias: str | None = None):
        super().__init__(id, websites["steam"])
        self.name = name
        self.alias = alias

    def to_dict(self):
        return super().to_dict() | {"name": self.name, "alias": self.alias}


class FaceitProfile(ProfileBase):
    def __init__(self, id, name, level, elo, number_of_games):
        super().__init__(id, websites["faceit"])
        self.level = level
        self.elo = elo
        self.name = name
        self.number_of_games = number_of_games

    def to_dict(self):
        return super().to_dict() | {
            "level": self.level,
            "elo": self.elo,
            "name": self.name,
            "number_of_games": self.number_of_games,
        }


class Profile:
    def __init__(self, community_id, id_type: IDType = IDType.id) -> None:
        self.steam: SteamProfile = self.get_steam(community_id, id_type)
        self.faceit: FaceitProfile = self.get_faceit(self.steam.id)

    def get_steam(self, community_id: str, id_type: IDType) -> SteamProfile:
        """Get an ID from an alias"""
        community_page = f"https://{websites["steam"].host}/{id_type.value}/{community_id}?xml=1"
        page = requests.get(community_page)
        steam_profile_dict = xmltodict.parse(page.content)

        steam_profile = steam_profile_dict.get("profile")
        if not steam_profile:
            raise Exception("No profile")

        steam_id = steam_profile.get("steamID64")
        steam_name = steam_profile.get("steamID")
        steam_alias = steam_profile.get("customURL")

        return SteamProfile(id=steam_id, name=steam_name, alias=steam_alias)

    def get_faceit(self, steam_id: str):
        page = requests.get(
            f"https://open.faceit.com/data/v4/players?game=cs2&game_player_id={steam_id}",
            headers={"Authorization": f"Bearer {settings.faceit_api_key}"},
        )
        data = page.json()

        cs2_data = data.get("games", {}).get("cs2")

        return FaceitProfile(
            id=data.get("nickname"),
            level=cs2_data.get("skill_level"),
            elo=cs2_data.get("faceit_elo"),
            name=cs2_data.get("nickname"),
            number_of_games=0,
        )

    def to_dict(self):
        return {
            **self.steam.to_dict(),
            "medias": [
                self.faceit.to_dict(),
            ],
        }


def create_profile():
    return Profile()
