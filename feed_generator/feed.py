from bs4 import BeautifulSoup
import toml
from pathlib import Path
from urllib.request import urlopen
from urllib.parse import urljoin

from feed_generator.generators import royalroad
from feed_generator.generators import aoa
from feed_generator.generators import ffnet

GENERATORS = {
    'royalroad': royalroad,
    'aoa': aoa,
    'ffnet': ffnet
}

def generate_feed(config_path: str):
    config = toml.load(config_path)
    base = Path(config['base_dir'])
    base.mkdir(parents=True, exist_ok=True)

    for feed_config in config["Feeds"]:
        generator = GENERATORS[feed_config['generator']]
        feed = generator.generate_feed(feed_config)
        feed.rss_file(f"{config['base_dir']}/{feed_config['name']}.xml")
