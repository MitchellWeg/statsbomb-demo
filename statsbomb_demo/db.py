import duckdb

def init_db() -> duckdb.DuckDBPyConnection:
    conn = duckdb.connect('statsbomb.db')

    return conn