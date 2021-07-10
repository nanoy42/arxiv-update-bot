# arXiv update bot

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
## How it works

For each update, the script get the RSS flux, goes through the article and try to match the articles titles with the buzzwords. If there is match, a notification is sent.