import datetime


def generate_category_leaderboard(runs, player_id_to_players, category_name):
    return "\n".join(
        generate_jekyll_header(category_name)
        + generate_categories_header()
        + list(generate_categories_rows(runs, player_id_to_players)),
    )


def generate_categories_rows(runs, player_id_to_players):
    rank = 1
    for i, run in enumerate(runs):
        player_names = [
            player.name or player_id_to_players[player.id].name
            for player in run.players
        ]
        player_names_agg = ",".join(player_names)
        # TODO markdown encoders can't handle many non-ascii characters
        player_names_ascii = player_names_agg.encode("ascii", errors="ignore").decode()

        run_time = str(datetime.timedelta(seconds=run.time))

        if i > 0 and runs[i - 1].time != run.time:
            rank = i + 1
        yield f"| {rank} | {player_names_ascii} | {run_time} | {run.date} | [link]({run.video_url}) |"


def generate_categories_header():
    return [
        "| Rank | Player | Time | Date | Video |",
        " ---- | ------ | ---- | ---- | ----- ",
    ]


def generate_jekyll_header(category_name):
    return [
        "---",
        "layout: post",
        f'title:  "{category_name}"',
        "date:   2021-08-09 21:00:00 -0500",
        "categories: speedrun",
        "---",
        "",
    ]