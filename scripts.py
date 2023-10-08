import uvicorn


def dev():
    uvicorn.run("csgoscan.main:app", port=8080, reload=True)


def start():
    uvicorn.run("csgoscan.main:app", port=8080)
