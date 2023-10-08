class Website:
    protocol = "https"

    def __init__(self, host: str, profile_path: str) -> None:
        self.host = host
        self.profile_path = profile_path
        self.home_url = f"{self.protocol}://{self.host}/"
        self.profile_url = self.home_url + self.profile_path

    def profile_link(self, steam_id: str) -> str:
        return self.profile_url.format(steam_id)


steam = Website(host="steamcommunity.com", profile_path="profiles/{}")
faceit_finder = Website(host="faceitfinder.com", profile_path="profile/{}")
cs_stats = Website(host="csstats.gg", profile_path="player/{}")
csgo_backpack = Website(host="csgobackpack.net", profile_path="index.php?nick={}")
leetify = Website(host="leetify.com", profile_path="app/profile/{}")
