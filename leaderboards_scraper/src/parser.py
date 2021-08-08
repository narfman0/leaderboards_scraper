import logging

from leaderboards_scraper.models import Run


def parse_category_runs_page(runs_json):
    runs = []
    for run_json in runs_json:
        run = run_from_src_api_json(run_json)
        if run:
            runs.append(run)
    return runs


def run_from_src_api_json(run_json):
    run_id = run_json["id"]
    try:
        player_ids = []
        for player in run_json["players"]:
            if "id" in player:
                player_ids.append(player["id"])
            else:
                logging.info(f"Player found without id: {player}")
        return Run(
            id=run_id,
            player_ids=player_ids,
            category_id=run_json["category"],
            video_url=run_json["videos"]["links"][0]["uri"],
            comment=run_json["comment"],
            date=run_json["date"],
            time=run_json["times"].get("realtime_t"),
            splits_io_url=(run_json["splits"] or {}).get("uri"),
        )
    except Exception as e:
        logging.warning(f"Exception {e} received for run_id {run_id}")