"""FastAPI app for FaceitFinder redirector"""

from fastapi import Depends, FastAPI, Path, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import csgoscan
from csgoscan.dependencies import get_id_from_alias
from csgoscan.website import cs_stats, csgo_backpack, faceit_finder, leetify

app = FastAPI()

package_path = csgoscan.__path__[0]
app.mount("/static", StaticFiles(directory= package_path + "/static"), name="static")
templates = Jinja2Templates(directory=package_path + "/templates")

websites = [faceit_finder, cs_stats, csgo_backpack, leetify]


@app.get("/")
def root():
    return {"message": "Hello World"}


def build_context(steam_id):
    links = [{"name": w.host, "url": w.profile_link(steam_id)} for w in websites]
    return {"steam_id": steam_id, "links": links}


@app.get("/id/{alias}")
async def get_by_id(request: Request, steam_id: str = Depends(get_id_from_alias)):
    context: dict = build_context(steam_id)
    context.update(request=request)

    return templates.TemplateResponse("index.html.j2", context)


@app.get("/profiles/{steam_id}")
async def get_by_alias(request: Request, steam_id: str = Path()):
    context: dict = build_context(steam_id)
    context.update(request=request)

    return templates.TemplateResponse("index.html.j2", context)
