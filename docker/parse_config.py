import os

token = os.environ["AUB_TOKEN"]
chat_ids = os.environ["AUB_CHAT_IDS"].split(";")
categories = os.environ["AUB_CATEGORIES"].split(";")
buzzwords = os.environ["AUB_BUZZWORDS"].split(";")

TEMPLATE = """
[{category}]
chat_id = {chat_id}
category = {category}
buzzwords = {buzzwords}
"""

res = "[bot]\n"
res += f"token = {token}\n"

for i, category in enumerate(categories):
    res += TEMPLATE.format(
        category=category, chat_id=chat_ids[i], buzzwords=buzzwords[i]
    )

print(res)
