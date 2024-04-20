import duckdb


def exists_in_db(table_name: str, id: int, conn: duckdb.DuckDBPyConnection) -> bool:
    q = f"select * from {table_name} where id = {str(id)}"
    r = conn.sql(q)

    f = r.fetchone()
    r.close()
    return (f is not None)
