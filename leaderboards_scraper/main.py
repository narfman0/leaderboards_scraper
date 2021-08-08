import logging

from leaderboards_scraper.src import api


def main():
    logging.basicConfig(filename="leaderboards.log", level=logging.INFO)
    # we want to decouple api json requests and generating websites, while
    # doing this cheaply
    # 1. download all /runs locally with respectful/stealth mode invocation
    # api.process_runs()
    api.process_players()

    # 2. have system to generate markdown from local runs json
    # 3. git add markdown to jekyll website, commit, push, let static site generation solve everything?
    # followon work
    # * populate database from json to enrich run information
    # * enumerate games and categories to scrape
    pass


if __name__ == "__main__":
    # execute only if run as a script
    main()
