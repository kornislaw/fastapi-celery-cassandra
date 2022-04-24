import re
# import os, pathlib
# import pytest
#
# os.chdir( pathlib.Path.cwd() / 'tests' )
#
# pytest.main()

from app import db, main

def test_db_connection():
    session = db.get_session()
    main.on_startup()

    row = session.execute("select release_version from system.local").one()
    assert 'release_version' in row
    assert row['release_version'].startswith('4.')
    assert re.match(r'^\d+[\.\d]+\d+$', row['release_version'])
