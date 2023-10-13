"""FastAPI app for FaceitFinder redirector"""

from dataclasses import asdict
from fastapi import Depends, FastAPI, Request, Path
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import csgoscan
from csgoscan.website import generate_media_links

# from csgoscan.getter import get_faceit_profile, get_steam_profile, IDType
from csgoscan.profile import Profile, IDType


app = FastAPI()

package_path = csgoscan.__path__[0]
app.mount("/static", StaticFiles(directory=package_path + "/static"), name="static")
templates = Jinja2Templates(directory=package_path + "/templates")


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/{id_type}/{community_id}")
async def profiler(
    request: Request,
    id_type: IDType = Path(),
    community_id: str = Path(),
):
    profile: Profile = Profile(community_id, id_type)
    # steam_profile: SteamProfile = await get_steam_profile(id_type, community_id)
    # faceit_profile: FaceitProfile = await get_faceit_profile(steam_profile.id)

    # profile = Profile(steam_profile, faceit_profile)

    return profile.to_dict()

    # return templates.TemplateResponse(
    #     "index.html.j2",
    #     {"request": request, "profile": asdict(profile)},
    # )
