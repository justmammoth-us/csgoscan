import requests
from xml.etree import ElementTree
from fastapi import Path
from .website import steam


def get_id_from_alias(alias: str = Path()) -> str:
    """Get an ID from an alias"""
    user_community_page = steam.profile_link(alias)
    page = requests.get(f"{user_community_page}?xml=1")
    profile = ElementTree.fromstring(page.content)
    return profile.find("steamID64").text
