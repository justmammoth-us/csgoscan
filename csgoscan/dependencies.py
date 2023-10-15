from dataclasses import asdict
from fastapi import Path
from csgoscan.media import (
    Steam,
    Faceit,
    CSGOBackpack,
    CSStats,
    Leetify,
    FaceitFinder,
)


async def get_player(community_id: str = Path(), id_type: Steam.IDType = Path()):
    steam = await Steam.get_profile(community_id, id_type)
    faceit = await Faceit.get_profile(steam.id)
    csgo_backpack = await CSGOBackpack.get_profile(steam.id)
    cs_stats = await CSStats.get_profile(steam.id)
    leetify = await Leetify.get_profile(steam.id)
    faceit_finder = await FaceitFinder.get_profile(steam.id)

    return {
        "media": {
            "steam": asdict(steam),
            "faceit": asdict(faceit),
            "csgo_backpack": asdict(csgo_backpack),
            "cs_stats": asdict(cs_stats),
            "leetify": asdict(leetify),
            "faceit_finder": asdict(faceit_finder),
        },
    }
