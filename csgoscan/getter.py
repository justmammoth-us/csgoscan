import requests
from fastapi import Path, HTTPException
import xmltodict
from enum import Enum

from csgoscan.website import steam
from csgoscan.profile import Profile
from csgoscan.settings import settings


class IDType(str, Enum):
    alias = "id"
    id = "profiles"


async def get_steam_profile(id_type: IDType, community_id: str) -> SteamProfile:
    """Get an ID from an alias"""
    community_page = f"https://{steam.host}/{id_type.value}/{community_id}?xml=1"
    page = requests.get(community_page)
    steam_profile_dict = xmltodict.parse(page.content)

    steam_profile = steam_profile_dict.get("profile")
    if not steam_profile:
        raise HTTPException(status_code=404)

    steam_id = steam_profile.get("steamID64")
    steam_name = steam_profile.get("steamID")
    steam_alias = steam_profile.get("customURL")

    return SteamProfile(id=steam_id, name=steam_name, alias=steam_alias)


async def get_faceit_profile(steam_id: str) -> FaceitProfile:
    page = requests.get(
        f"https://open.faceit.com/data/v4/players?game=cs2&game_player_id={steam_id}",
        headers={"Authorization": f"Bearer {settings.faceit_api_key}"},
    )
    data = page.json()

    cs2_data = data.get("games", {}).get("cs2")

    return FaceitProfile(
        id=data.get("player_id"),
        level=cs2_data.get("skill_level"),
        elo=cs2_data.get("faceit_elo"),
        name=cs2_data.get("nickname"),
        number_of_games=0,
    )
