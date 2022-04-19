from typing import List
from fastapi import FastAPI, Request

from cassandra.cqlengine.management import sync_table
from . import (
    config,
    crud,
    db,
    models,
    schema,
)

settings = config.get_settings()
Product = models.Product
ProductScrapeEvent = models.ProductScrapeEvent

app = FastAPI()

session = None


@app.on_event('startup')
def on_startup():
    global session
    session = db.get_session()
    sync_table(Product)
    sync_table(ProductScrapeEvent)


@app.get('/')
def read_index():
    return {"hello": "world", "name": settings.name}


@app.get('/products', response_model=List[schema.ProductListSchema])
def products_list_view():
    return list(Product.objects.all())


@app.post('/events/scrape')
def products_list_view(data: schema.ProductListSchema):
    product, _ = crud.add_scrape_event(data.dict())
    return product


@app.get('/products/{asin}')
def product_view(asin, request: Request):
    data = dict(Product.objects.get(asin=asin))
    events_count = ProductScrapeEvent.objects().filter(asin=asin).count()
    events = list(ProductScrapeEvent.objects().filter(asin=asin).limit(5))
    events = [schema.ProductScrapeEventDetailSchema(**x) for x in events]
    data['events_count'] = events_count
    data['events_url'] = f'{request.url._url}/events'
    data['events'] = events
    return data


@app.get('/products/{asin}/events', response_model=List[schema.ProductScrapeEventDetailSchema])
def product_scrapes_list_view(asin):
    return list(ProductScrapeEvent.objects().filter(asin=asin))
