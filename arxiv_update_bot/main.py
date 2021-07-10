import argparse
import configparser

import feedparser
import telebot

DEFAULT_CONFIGURATION_PATH = "/etc/arxiv-update-bot/config.ini"


def load_config(path):
    """Load the configuration from the path.
    It will try to load the token from the [bot] section.
    Then it will iterate over the other sections to find the updates to verify.

    Args:
        path (string): path of the config file.

    Raises:
        Exception: if the bot section is not found.
        Exception: if there is no token value in the bot section.
        Exception: if an update section is not complete.

    Returns:
        (string, list): the token and the list of updates.
    """
    config = configparser.ConfigParser()
    config.read(path)

    if "bot" not in config:
        raise Exception(
            "A bot section must be in the configuration file to set the token"
        )

    bot_config = config["bot"]
    if "token" not in bot_config:
        raise Exception("The bot section must have the bot token.")

    token = bot_config["token"]
    updates = []
    for section in config.sections():
        if str(section) != "bot":
            current_section = config[section]
            if not (
                "category" in current_section
                and "chat_id" in current_section
                and "buzzwords" in current_section
            ):
                raise Exception(
                    f"The section {current_section} is not complete. Missing one of three : category, chat_id or buzzwords."
                )
            updates.append(
                {
                    "category": current_section["category"],
                    "chat_id": current_section["chat_id"],
                    "buzzwords": current_section["buzzwords"].split(","),
                }
            )
    return token, updates


def get_articles(category, buzzwords):
    """Get the articles from arXiv.

    It get the RSS flux re;ated to the category of the update,
    then filter the entries with the buzzwords.

    Args:
        category (string): the name of the category.
        buzzwords (list): a list of buzzwords.

    Returns:
        list: list of entries.
    """
    news_feed = feedparser.parse(f"http://export.arxiv.org/rss/{category}")
    res = []
    for entry in news_feed.entries:
        for buzzword in buzzwords:
            if buzzword in entry.title.lower():
                res.append(entry)

    return res


def send_articles(bot, chat_id, category, buzzwords, quiet=False):
    """Send the articles to telegram.

    Args:
        bot (Telebot): telebot instance.
        chat_id (int): the chat id to send the message. Either a group or individual.
        category (string): the category for arXiv.
        buzzwords (list): list of buzzwords.
        quiet (bool, optional): whether to send a messae when no article is found. Defaults to False.
    """
    articles = get_articles(category, buzzwords)

    if not articles:
        if not quiet:
            bot.send_message(
                chat_id,
                text="I scraped the arXiv RSS but found nothing of interest for you. Sorry.",
            )
    else:
        bot.send_message(
            chat_id,
            text=f"You are going to be happy. I found {len(articles)} article(s) of potential interest.",
        )
        for article in articles:
            bot.send_message(
                chat_id,
                text=f"<strong>Title</strong>: {article.title}\n<strong>Authors</strong>: {article.authors[0]['name']}\n<strong>Link</strong>: {article.id}",
            )


def main():
    """
    The main function.
    """
    parser = argparse.ArgumentParser(description="Scrap the arXiv")
    parser.add_argument(
        "-c",
        "--config-path",
        help="Path for configuration path. Replace default of /etc/arxiv-update-bot/config.ini",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="If quiet is set, then the bot will not send message if no article are found.",
    )
    args = parser.parse_args()
    config_path = args.config_path or DEFAULT_CONFIGURATION_PATH
    quiet = args.quiet

    token, updates = load_config(config_path)

    bot = telebot.TeleBot(token, parse_mode="HTML")

    for update in updates:
        send_articles(
            bot, update["chat_id"], update["category"], update["buzzwords"], quiet=quiet
        )


if __name__ == "__main__":
    main()
