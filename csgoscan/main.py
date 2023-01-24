"""FastAPI app for FaceitFinder redirector"""
import requests
import xml.etree.ElementTree as ET

from fastapi import FastAPI, Path
from fastapi.responses import RedirectResponse


URL_FACEITFINDER = "https://faceitfinder.com"
URL_STEAM = "https://steamcommunity.com"

app = FastAPI()


def make_faceitfinder_url(id: str) -> str:
    """Make a FaceitFinder URL from an ID"""
    return f"{URL_FACEITFINDER}/profile/{id}"


def get_id_from_alias(alias: str) -> str:
    """Get an ID from an alias"""
    page = requests.get(f"{URL_STEAM}/id/{alias}?xml=1")
    profile = ET.fromstring(page.content)
    return profile.find("steamID64").text


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/profiles/{id}")
async def id(id: str = Path()) -> RedirectResponse:
    """Redirect to FaceitFinder profile page"""
    redirect_url = make_faceitfinder_url(id)
    return RedirectResponse(redirect_url)


@app.get("/id/{alias}")
async def profiles(alias: str = Path()) -> RedirectResponse:
    """Redirect to FaceitFinder profile page"""
    id = get_id_from_alias(alias)
    print(id)
    redirect_url = make_faceitfinder_url(id)
    return RedirectResponse(redirect_url)
