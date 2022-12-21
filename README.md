# arXiv update bot


[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style black](https://img.shields.io/badge/code%20style-black-000000.svg)]("https://github.com/psf/black)
[![GitHub release](https://img.shields.io/github/release/nanoy42/arxiv-update-bot.svg)](https://github.com/nanoy42/arxiv-update-bot/releases/)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)
[![Docker](https://img.shields.io/docker/cloud/build/nanoy/arxiv-update-bot?label=Docker&style=flat)](https://hub.docker.com/r/nanoy/arxiv-update-bot)

arxiv update bot is a simple python script that scraps the arXiv, search for interesting paper and send a message on telegram if any was found.

## Usage

The package comes with a command line script arxiv-update-bot. Here the help message :

```
usage: arxiv-update-bot [-h] [-c CONFIG_PATH] [-q]

Scrap the arXiv

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG_PATH, --config-path CONFIG_PATH
                        Path for configuration path. Replace default of
                        /etc/arxiv-update-bot/config.ini
  -q, --quiet           If quiet is set, then the bot will not send message if
                        no article are found.
```

## Installation

The package can be installed either via the pypi repository :

or using the sources :

## Configuration file

In order to work, the script needs a configuration file. It will by default search for the configuration file in `/etc/arxiv-update-bot/config.ini`. Note that you have to manually create the folder and give the good permissions.

You can override the default behavior with the `-c` option on the command line and by giving the path as argument.

An example configuration can be found at `arxiv_update_bot/config.example.ini` and is also included in the package. Here is the example:

```ini
[bot]
token = 0000000000:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

[quant-ph]
chat_id = 0
category = quant-ph
buzzwords = cvqkd,continuous variable,continuous-variable,qkd,quantum key distribution,rfsoc,fpga
```

The `[bot]` section is here to parametrize the bot. It must have the `token` value (with the "bot" word).

Then for each update, you need to define a section. The name of the section is not really important (it must be unique and not "bot"). 
* The `chat_id` corresponds to the id of the individual or group where the notification must be sent. For now you can only configure 1 recipient per update.
* The `category` is the name of the arxiv category. It will be used to determinate which RSS flux will be scraped.
* The `buzzwords` are a list of words, separated by comas (without spaces) and in lowercase. The articles that will be keeped will be the ones with one of the buzwwords in the title.

## Cron configuration

It is advised to use a cron to execute the script periodically :

```
0 10 * * * arxiv-update-bot
```
to run the script every day at 10 am.

## Docker image

As of version 0.8 of `arxiv-update-bot`, a docker image is now available : https://hub.docker.com/r/nanoy/arxiv-update-bot. It allows you to simply run the script with minimal commands. If you are using `docker-compose` you can use the following configuration file :

```yml
version: '3.6'

services:
  arxiv-update-bot:
    image: nanoy/arxiv-update-bot
    environment:
      - AUB_TOKEN=0000000000:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
      - AUB_CHAT_IDS=0
      - AUB_CATEGORIES=quant-ph
      - AUB_BUZZWORDS=cvqkd,cv-qkd,continuous variable,continuous-variable,qkd,quantum key distribution,rfsoc,fpga
      - AUB_CRONTAB=0 10 * * *

```

or you can directly use the following docker command 

```
docker run -d -t -i -e AUB_TOKEN=0000000000:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA -e AUB_CHAT_IDS=0 -e AUB_CATEGORIES=quant-ph -e AUB_BUZZWORDS='cvqkd,cv-qkd,continuous variable,continuous-variable,qkd,quantum key distribution,rfsoc,fpga' -e AUB_CRONTAB='0 10 * * *' --name arxiv-update-bot nanoy/arxiv-update-bot
```

Please note that if you want to have several updates section, you can give them by separating with semi-colons, like so 

```yml
version: '3.6'

services:
  arxiv-update-bot:
    image: nanoy/arxiv-update-bot
    environment:
      - AUB_TOKEN=0000000000:AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
      - AUB_CHAT_IDS=0;10
      - AUB_CATEGORIES=quant-ph;category2
      - AUB_BUZZWORDS=cvqkd,cv-qkd,continuous variable,continuous-variable,qkd,quantum key distribution,rfsoc,fpga;buzzword1, buzzword2
      - AUB_CRONTAB=0 10 * * *

```
## How it works

For each update, the script get the RSS flux, goes through the article and try to match the articles titles with the buzzwords. If there is match, a notification is sent.