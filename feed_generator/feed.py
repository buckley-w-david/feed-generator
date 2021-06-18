from bs4 import BeautifulSoup
import logging
import toml
import os
from pathlib import Path
from urllib.request import urlopen
from urllib.parse import urljoin

import typer
from pydantic import HttpUrl, BaseModel

from feed_generator.config import Settings, FeedModel
from feed_generator import generators
from feed_generator.metadata import fetch_metadata

logging.getLogger("fanficfare").setLevel(logging.ERROR)
logger = logging.getLogger(__name__)

# TODO configurable log level
logging.basicConfig(level=logging.INFO)

app = typer.Typer()

@app.command()
def generate_feed():
    settings = Settings()
    base = Path(str(settings.base_dir))
    base.mkdir(parents=True, exist_ok=True)

    # TODO find a better way to go from str -> HttpUrl
    class MyModel(BaseModel):
        url: HttpUrl

    with open(settings.urls, 'r') as f:
        serial_urls = [MyModel(url=url.strip()) for url in f.readlines()]

    for url_model in serial_urls:
        try:
            metadata = fetch_metadata(url_model.url)
            name = metadata["title"]

            generator = generators.from_url(url_model.url)

            feed_config = FeedModel(url=url_model.url, name=name)
            logger.info("Generating feed for %s", str(feed_config.url))
            feed = generator.generate_feed(feed_config)
            feed.rss_file(f"{settings.base_dir}/{feed_config.name}.xml")
        except Exception as e:
            logger.error("%s for %s", e, url_model.url)

@app.command()
def add(url: str):
    settings = Settings()
    with open(settings.urls, 'r') as f:
        serial_urls = [url.strip() for url in f.readlines()]

    serial_urls.append(url)

    with open(settings.urls, 'w') as f:
        f.write('\n'.join(serial_urls))

@app.command()
def metadata(url: str):
    # TODO find a better way to go from str -> HttpUrl
    class MyModel(BaseModel):
        url: HttpUrl

    metadata = fetch_metadata(MyModel(url=url).url)
    print(metadata)
