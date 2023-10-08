"""FastAPI app for FaceitFinder redirector"""

from fastapi import FastAPI, Path, Depends, Request
from .dependencies import get_id_from_alias
from .website import faceit_finder, cs_stats, csgo_backpack, leetify
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="csgoscan/templates")

websites = [faceit_finder, cs_stats, csgo_backpack, leetify]


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/profiles/{alias}")
async def get_by_id(request: Request, steam_id: str = Depends(get_id_from_alias)):
    """Redirect to FaceitFinder profile page"""

    links = [{"name": w.host, "url": w.profile_link(steam_id)} for w in websites]

    context = {"request": request, "steam_id": steam_id, "links": links}

    return templates.TemplateResponse("index.html.j2", context)


@app.get("/id/{steam_id}")
async def get_by_alias(steam_id: str = Path()):
    links = [{"host": w.host, "link": w.profile_link(steam_id)} for w in websites]

    return {"steam_id": steam_id, "links": links}
