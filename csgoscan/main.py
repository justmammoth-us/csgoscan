"""FastAPI app for FaceitFinder redirector"""

from fastapi import Depends, FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import csgoscan
from csgoscan.website import websites
from csgoscan.dependencies import get_profile
from csgoscan.profile import Profile


app = FastAPI()

package_path = csgoscan.__path__[0]
app.mount("/static", StaticFiles(directory=package_path + "/static"), name="static")
templates = Jinja2Templates(directory=package_path + "/templates")


@app.get("/")
def root():
    return {"message": "Hello World"}


def build_media_links(steam_id) -> list:
    return [{"name": w.name, "url": w.profile_link(steam_id)} for w in websites]


@app.get("/{id_type}/{community_id}")
async def profiler(request: Request, profile: Profile = Depends(get_profile)):
    profile.medias = build_media_links(profile.id)

    return templates.TemplateResponse(
        "index.html.j2",
        {"request": request, "profile": profile},
    )
