import configparser
from openai import OpenAI

cfg = configparser.ConfigParser()
cfg.read("config.ini", encoding="utf-8")
client = OpenAI(api_key=cfg["llm"]["api_key"], base_url=cfg["llm"]["base_url"])
resp = client.chat.completions.create(
    model=cfg["llm"]["model"],
    messages=[{"role": "user", "content": input("你: ")}],
)
print(resp.choices[0].message.content)
