from helpers import read_sql_file
import duckdb

def init_db() -> duckdb.DuckDBPyConnection:
    conn = duckdb.connect('statsbomb.db')
    qs = read_sql_file("init")
    conn.sql(qs)

    return conn