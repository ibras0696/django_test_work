import pytest
import os
import django


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    # ensures db is available for all tests
    pass
