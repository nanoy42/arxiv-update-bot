FROM python:3.9
RUN apt-get update && apt-get upgrade -y && apt-get -y install cron gettext-base
RUN pip install --upgrade pip
RUN pip install --upgrade arxiv-update-bot
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY docker/parse_config.py /code/
COPY docker/docker-entrypoint.sh /code/
COPY docker/crontab /code/
CMD ./docker-entrypoint.sh