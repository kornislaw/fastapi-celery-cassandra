from . import config
from atexit import register
import os
import pathlib

from dotenv import load_dotenv

# from readline import get_current_history_length
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.cqlengine.connection import register_connection, set_default_connection

BASE_DIR = pathlib.Path(__file__).parent
CLUSTER_BUNDLE = str(BASE_DIR / 'ignore' / 'connect.zip')
print(CLUSTER_BUNDLE)
settings = config.get_settings()

# load_dotenv()

ASTRA_DB_CLIENT_ID = settings.db_client_id
ASTRA_DB_CLIENT_SECRET = settings.db_client_secret


def get_cluster():
    cloud_config = {
        'secure_connect_bundle': CLUSTER_BUNDLE,
        'init-query-timeout': 20,  # kornislaw added this one from https://community.datastax.com/questions/7062/unable-to-connect-to-the-metadata-service.html
        'connect_timeout': 20,  # kornislaw added this one from https://community.datastax.com/questions/7062/unable-to-connect-to-the-metadata-service.html
        'set-keyspace-timeout': 20  # kornislaw added this one from https://community.datastax.com/questions/7062/unable-to-connect-to-the-metadata-service.html
    }
    auth_provider = PlainTextAuthProvider(
        ASTRA_DB_CLIENT_ID, ASTRA_DB_CLIENT_SECRET)
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    return cluster


def get_session():
    cluster = get_cluster()
    session = cluster.connect()
    register_connection(str(session), session=session)
    set_default_connection(str(session))
    return session


# session = get_session()
# row = session.execute("select release_version from system.local").one()
# if row:
#     print(row[0])
# else:
#     print("An error occurred.")
