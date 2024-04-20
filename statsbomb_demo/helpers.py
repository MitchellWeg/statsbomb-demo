import duckdb
import os

def read_sql_file(name: str) -> str:
    cwd = os.getcwd()
    p = os.path.join(cwd, f"sql/{name}.sql")

    return open(p).read()


def exists_in_db(table_name: str, id: int, conn: duckdb.DuckDBPyConnection) -> bool:
    q = f"select * from {table_name} where id = {str(id)}"
    r = conn.sql(q)

    f = r.fetchone()
    r.close()
    return (f is not None)


def clean_str(s: str) -> str:
    return s.replace("'", "''")
