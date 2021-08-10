def generate_category_leaderboard(category_id, runs, player_id_to_players):
    return "\n".join(
        generate_categories_header()
        + list(generate_categories_rows(category_id, runs, player_id_to_players)),
    )


def generate_categories_rows(category_id, runs, player_id_to_players):
    for i, run in enumerate(runs, 1):
        player_names = [
            player_id_to_players[player_id].name for player_id in run.player_ids
        ]
        player_names_agg = ",".join(player_names)
        yield f"| {i} | {player_names_agg} | {run.time}s | {run.date} | {run.video_url} |"


def generate_categories_header():
    return [
        "| Rank | Player | Time | Date | Video |",
        " ---- | ------ | ---- | ---- | ----- ",
    ]
