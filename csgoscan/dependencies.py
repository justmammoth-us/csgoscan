import requests
from fastapi import Path, HTTPException
import xmltodict
from enum import Enum

from csgoscan.website import steam
from csgoscan.profile import Profile


class IDType(str, Enum):
    alias = "id"
    id = "profiles"


def get_profile(id_type: IDType, community_id: str = Path()) -> str:
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

    return Profile(id=steam_id, name=steam_name, alias=steam_alias)
