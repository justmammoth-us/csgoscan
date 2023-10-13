from csgoscan.profile import Profile


class Website:
    protocol: str = "https"

    def __init__(self, name: str, host: str, profile_path: str, id_type: str) -> None:
        self.name = name
        self.host = host
        self.profile_path = profile_path
        self.id_type = id_type
        self.home_url = f"{self.protocol}://{self.host}/"
        self.profile_url = self.home_url + self.profile_path

    def profile_link(self, id: str) -> str:
        return self.profile_url.format(id)


steam = Website(
    name="Steam",
    host="steamcommunity.com",
    profile_path="profiles/{}",
    id_type="steam",
)
faceit_finder = Website(
    name="Faceit Finder",
    host="faceitfinder.com",
    profile_path="profile/{}",
    id_type="steam",
)
cs_stats = Website(
    name="CSStats",
    host="csstats.gg",
    profile_path="player/{}",
    id_type="steam",
)
csgo_backpack = Website(
    name="CSGO Backpack",
    host="csgobackpack.net",
    profile_path="index.php?nick={}",
    id_type="steam",
)
leetify = Website(
    name="Leetify",
    host="leetify.com",
    profile_path="app/profile/{}",
    id_type="steam",
)

websites = [faceit_finder, cs_stats, csgo_backpack, leetify]


def generate_media_links(profile: Profile) -> list:
    return [
        {"name": w.name, "url": w.profile_link(profile[w.id_type].id)} for w in websites
    ]
