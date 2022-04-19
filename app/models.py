from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


data = {
    'asin': "B07W2Z2ZS3",
    'title': 'Garmin Fcośtam innego'
}


class Product(Model):  # --> Table
    __keyspace__ = "scraper_app"
    asin = columns.Text(primary_key=True, required=True)
    title = columns.Text()
    price_str = columns.Text(default="-1")


class ProductScrapeEvent(Model):  # --> Table
    __keyspace__ = "scraper_app"
    uuid = columns.UUID(primary_key=True)
    asin = columns.Text(index=True)
    title = columns.Text()
    price_str = columns.Text(default="-1")
    created_v2 = columns.DateTime()
