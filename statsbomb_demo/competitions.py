import requests
import duckdb


class CompetitionsFetcher:
    def __init__(self, url: str, db: duckdb.DuckDBPyConnection) -> None:
        self.url = url
        self.db = db

    def fetch(self) -> dict:
        return requests.get(self.url).json()
