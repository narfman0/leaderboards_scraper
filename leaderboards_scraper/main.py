import logging

from leaderboards_scraper import fs, md
from leaderboards_scraper.src import api


def main():
    logging.basicConfig(filename="leaderboards.log", level=logging.INFO)
    # we want to decouple api json requests and generating websites, while
    # doing this cheaply
    # 1. download all /runs locally with respectful/stealth mode invocation
    category_to_runs = api.process_runs()
    player_id_to_players = api.process_players()
    category_id_to_name = {
        category.id: category.name for category in fs.load_categories()
    }

    # 2. generate markdown from local runs json
    for category_id, runs in category_to_runs.items():
        runs = sorted(runs, key=lambda run: run.time)
        seen_players = []
        pb_runs = []
        for run in runs:
            player_ids_agg = "|".join(
                filter(None, [player.id for player in run.players])
            )
            if player_ids_agg in seen_players:
                continue
            seen_players.append(player_ids_agg)
            pb_runs.append(run)
        category_name = category_id_to_name[category_id]
        markdown = md.generate_category_leaderboard(
            pb_runs, player_id_to_players, category_name
        )
        fs.store_category_leaderboard(category_id, markdown)
    # 3. git add markdown to jekyll website, commit, push, let static site generation solve everything?
    # followon work
    # * populate database from json to enrich run information
    # * enumerate games and categories to scrape
    pass


if __name__ == "__main__":
    # execute only if run as a script
    main()
