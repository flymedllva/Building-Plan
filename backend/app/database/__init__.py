from app.database.model import ArangoDB
from app.config import ARANGODB_DATABASE_URL, ARANGODB_DATABASE_NAME

database: ArangoDB = ArangoDB(
    hosts=ARANGODB_DATABASE_URL, database=ARANGODB_DATABASE_NAME
)
