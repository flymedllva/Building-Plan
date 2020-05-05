from os import getenv, path

DIRECTORY = path.abspath(__file__).rstrip("config.py")
SERVER_NAME = getenv("SERVER_NAME")
SERVER_HOST = getenv("SERVER_HOST")
PROJECT_NAME = getenv("PROJECT_NAME") or "BuildingPlan"
PROJECT_DESCRIPTION = getenv("PROJECT_DESCRIPTION") or "API"
PROJECT_VERSION = getenv("PROJECT_VERSION") or "1.0"
PROJECT_DOCS_URL = "/documentation"
PROJECT_API_V1_URL = "/api"

ARANGODB_DATABASE_NAME = getenv("ARANGODB_DATABASE_NAME") or "_system"
ARANGODB_DATABASE_URL = getenv("ARANGODB_DATABASE_URL") or "http://localhost:8529"
