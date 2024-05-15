from instorage.database.database import sessionmanager
from instorage.main.config import get_settings
from instorage.main.logging import get_logger

logger = get_logger(__name__)


def connect_to_db():
    if get_settings().testing:
        logger.warning("Connecting to test database")
        db_url = get_settings().test_database_url
    else:
        db_url = get_settings().database_url

    sessionmanager.init(db_url)
