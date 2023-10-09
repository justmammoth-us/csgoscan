"""FastAPI app for FaceitFinder redirector"""

from fastapi import Depends, FastAPI, Path, Request
import requests
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from xml.etree import ElementTree

import csgoscan
from csgoscan.dependencies import get_id_from_alias
from csgoscan.website import cs_stats, csgo_backpack, faceit_finder, leetify, steam

app = FastAPI()

package_path = csgoscan.__path__[0]
app.mount("/static", StaticFiles(directory=package_path + "/static"), name="static")
templates = Jinja2Templates(directory=package_path + "/templates")

websites = [faceit_finder, cs_stats, csgo_backpack, leetify]


@app.get("/")
def root():
    return {"message": "Hello World"}


def build_media_links(steam_id) -> list:
    return [{"name": w.host, "url": w.profile_link(steam_id)} for w in websites]


def get_steam_profile(alias: str = Path()) -> str:
    """Get an ID from an alias"""
    user_community_page = f"https://{steam.host}/id/{alias}?xml=1"
    page = requests.get(user_community_page)
    profile = ElementTree.fromstring(page.content)
    user = {}
    user["id"] = profile.find("steamID64").text
    user["name"] = profile.find("steamID").text
    user["alias"] = profile.find("customURL").text
    return user


async def profiler(request: Request, steam_id: str = Path()):
    user = get_steam_profile(steam_id)
    user.update(links=build_media_links(steam_id))

    context = {"request": request, "user": user}

    return templates.TemplateResponse("index.html.j2", context)


app.add_api_route("/id/{steam_id}", profiler)
app.add_api_route("/profiles/{steam_id}", profiler)
