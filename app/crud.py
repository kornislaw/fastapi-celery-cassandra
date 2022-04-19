import copy
import uuid

from .models import Product, ProductScrapeEvent
from . import utils


def create_entry(data: dict):
    return Product.create(**data)


def create_scrape_entry(data: dict):
    data['uuid'] = uuid.uuid1()  # include timestamp
    data['created_v2'] = utils.uuid1_time_to_datetime(data['uuid'].time)
    print(data['created_v2'])
    return ProductScrapeEvent.create(**data)


def add_scrape_event(data: dict, fresh=False):
    if fresh:
        data = copy.deepcopy(data)
    product = create_entry(data)
    scrape_obj = create_scrape_entry(data)
    return product, scrape_obj
