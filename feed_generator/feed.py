from bs4 import BeautifulSoup
import toml
import os
from pathlib import Path
from urllib.request import urlopen
from urllib.parse import urljoin

import typer

from feed_generator.generators import royalroad
from feed_generator.generators import aoa
from feed_generator.generators import ffnet

GENERATORS = {
    'royalroad': royalroad,
    'aoa': aoa,
    'ffnet': ffnet
}

app = typer.Typer()

@app.command()
def generate_feed(config_path: str = os.environ.get("FEED_GENERATOR_CONFIG", "config.toml")):
    config = toml.load(config_path)
    base = Path(config['base_dir'])
    base.mkdir(parents=True, exist_ok=True)

    for feed_config in config["Feeds"]:
        generator = GENERATORS[feed_config['generator']]
        feed = generator.generate_feed(feed_config)
        feed.rss_file(f"{config['base_dir']}/{feed_config['name']}.xml")


@app.command()
def add(url: str, generator: str, name: str, config_path: str = os.environ.get("FEED_GENERATOR_CONFIG", "config.toml")):
    config = toml.load(config_path)
    config["Feeds"].append({"url": url, "name": name, "generator": generator})
    with open(config_path, 'w') as f:
        toml.dump(config, f)
