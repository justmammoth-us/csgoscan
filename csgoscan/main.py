"""FastAPI app for FaceitFinder redirector"""

from fastapi import Depends, FastAPI, Request, Query
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import csgoscan
from csgoscan.dependencies import get_player

app = FastAPI()

package_path = csgoscan.__path__[0]
app.mount("/static", StaticFiles(directory=package_path + "/static"), name="static")
templates = Jinja2Templates(directory=package_path + "/templates")


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/{id_type}/{community_id}")
async def player(
    request: Request,
    player: dict = Depends(get_player),
    raw: bool = Query(default=False),
):
    return (
        templates.TemplateResponse(
            "player.html.j2",
            {"request": request, "player": player},
        )
        if not raw
        else player
    )
