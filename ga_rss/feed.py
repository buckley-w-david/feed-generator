from bs4 import BeautifulSoup
import toml
from urllib.request import urlopen
from urllib.parse import urljoin

from ga_rss.generators import royalroad
from ga_rss.generators import aoa

GENERATORS = {
    'royalroad': royalroad,
    'aoa': aoa
}

def generate_feed(config_path: str):
    config = toml.load(config_path)

    for feed_config in config["Feeds"]:
        generator = GENERATORS[feed_config['generator']]
        feed = generator.generate_feed(feed_config)
        feed.rss_file(f"{config['base_dir']}/{feed_config['name']}.xml")
