FROM python:3

WORKDIR /usr/src/app

RUN pip install setuptools
COPY setup.py .
RUN python setup.py develop
COPY leaderboards_scraper ./leaderboards_scraper

CMD [ "python", "-m", "leaderboards_scraper.main" ]
