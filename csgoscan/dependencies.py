from dataclasses import asdict

from fastapi import Path
from csgoscan.errors import FaceitProfileNotExistError

from csgoscan.media import CSGOBackpack, CSStats, Faceit, FaceitFinder, Leetify, Steam


async def get_player(community_id: str = Path(), id_type: Steam.IDType = Path()):
    player = {}

    steam = await Steam.get_profile(community_id, id_type)
    player.update(steam=asdict(steam))

    try:
        faceit = await Faceit.get_profile(steam.id)
        player.update(faceit=asdict(faceit))
    except FaceitProfileNotExistError:
        pass

    csgo_backpack = await CSGOBackpack.get_profile(steam.id)
    player.update(csgo_backpack=asdict(csgo_backpack))

    cs_stats = await CSStats.get_profile(steam.id)
    player.update(cs_stats=asdict(cs_stats))

    leetify = await Leetify.get_profile(steam.id)
    player.update(leetify=asdict(leetify))

    faceit_finder = await FaceitFinder.get_profile(steam.id)
    player.update(faceit_finder=asdict(faceit_finder))

    return player
