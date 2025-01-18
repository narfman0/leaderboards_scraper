from leaderboards_scraper.models import Player, Run


def parse_category_runs_page(runs_json) -> list[Run]:
    runs = []
    for run_json in runs_json:
        run = run_from_src_api_json(run_json)
        if run:
            runs.append(run)
    return runs


def parse_raw_player(player_json) -> Player:
    return Player(
        id=player_json["id"],
        name=player_json["names"]["international"],
    )


def run_from_src_api_json(run_json) -> Run:
    run_id = run_json["id"]
    players = []
    for player in run_json["players"]:
        players.append(Player(id=player.get("id"), name=player.get("name")))
    video_link = None
    for link in run_json["videos"].get("links", []):
        if "uri" in link:
            video_link = link["uri"]
    return Run(
        id=run_id,
        players=players,
        category_id=run_json["category"],
        video_url=video_link,
        comment=run_json["comment"],
        date=run_json["date"],
        time=run_json["times"].get("realtime_t"),
        splits_io_url=(run_json["splits"] or {}).get("uri"),
        status=run_json["status"]["status"],
    )
