#!/usr/bin/env bash
set -euo pipefail

pip install arxiv-update-bot --upgrade
cat crontab | envsubst > /etc/cron.d/crontab
chmod 0644 /etc/cron.d/crontab
/usr/bin/crontab /etc/cron.d/crontab
python parse_config.py > config.ini
arxiv-update-bot -c config.ini -p
cron -f