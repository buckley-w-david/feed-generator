from bs4 import BeautifulSoup
import toml
import os
from pathlib import Path
from urllib.request import urlopen
from urllib.parse import urljoin

import typer

from feed_generator.config import Settings
from feed_generator import generators
from feed_generator.metadata import fetch_metadata

app = typer.Typer()

@app.command()
def generate_feed():
    settings = Settings()
    base = Path(str(settings.base_dir))
    base.mkdir(parents=True, exist_ok=True)

    for feed_config in settings.feeds:
        generator = generators.from_url(feed_config.url)
        feed = generator.generate_feed(feed_config)
        feed.rss_file(f"{settings.base_dir}/{feed_config.name}.xml")

@app.command()
def add(url: str):
    config = toml.load(config_path)
    metadata = fetch_metadata(url)
    name = metadata["title"]

    config["Feeds"].append({"url": url, "name": name})
    with open(config_path, 'w') as f:
        toml.dump(config, f)
