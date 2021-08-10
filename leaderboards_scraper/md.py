import datetime


def generate_category_leaderboard(runs, player_id_to_players, category_name):
    return "\n".join(
        generate_jekyll_header(category_name)
        + generate_categories_header()
        + list(generate_categories_rows(runs, player_id_to_players)),
    )


def generate_categories_rows(runs, player_id_to_players):
    for i, run in enumerate(runs, 1):
        player_names = [
            player.name or player_id_to_players[player.id].name
            for player in run.players
        ]
        player_names_agg = ",".join(player_names)

        m, s = divmod(run.time, 60)
        h, m = divmod(m, 60)
        run_time = "%d:%02d:%02d" % (h, m, s)
        yield f"| {i} | {player_names_agg} | {run_time} | {run.date} | [link]({run.video_url}) |"


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