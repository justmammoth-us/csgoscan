from xml.etree import ElementTree

import requests
from fastapi import Path

from .website import steam


def get_id_from_alias(alias: str = Path()) -> str:
    """Get an ID from an alias"""
    user_community_page = f"https://{steam.host}/id/{alias}?xml=1"
    page = requests.get(user_community_page)
    profile = ElementTree.fromstring(page.content)
    return profile.find("steamID64").text
