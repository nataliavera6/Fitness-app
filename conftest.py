# conftest.py
import pytest
from unittest.mock import patch, MagicMock

@pytest.fixture(autouse=True, scope="session")
def mock_bigquery_client():
    with patch("setup_database.bigquery.Client", MagicMock()):
        yield