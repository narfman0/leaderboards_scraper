FROM python:3

WORKDIR /usr/src/app

COPY . .
RUN python setup.py develop


CMD [ "python", "-m", "leaderboards_scraper.main" ]
