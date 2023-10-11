class Website:
    protocol = "https"

    def __init__(self, name: str, host: str, profile_path: str) -> None:
        self.name = name
        self.host = host
        self.profile_path = profile_path
        self.home_url = f"{self.protocol}://{self.host}/"
        self.profile_url = self.home_url + self.profile_path

    def profile_link(self, steam_id: str) -> str:
        return self.profile_url.format(steam_id)


steam = Website(
    name="Steam",
    host="steamcommunity.com",
    profile_path="profiles/{}",
)
faceit_finder = Website(
    name="Faceit Finder",
    host="faceitfinder.com",
    profile_path="profile/{}",
)
cs_stats = Website(
    name="CSStats",
    host="csstats.gg",
    profile_path="player/{}",
)
csgo_backpack = Website(
    name="CSGO Backpack",
    host="csgobackpack.net",
    profile_path="index.php?nick={}",
)
leetify = Website(
    name="Leetify",
    host="leetify.com",
    profile_path="app/profile/{}",
)

websites = [faceit_finder, cs_stats, csgo_backpack, leetify]
