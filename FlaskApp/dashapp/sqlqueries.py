import pandas as pd


def get_unique(connection, table, col):
    query = f"""
    SELECT DISTINCT {col}
    FROM {table};
    """
    return [x[0] for x in connection.execute(query).fetchall()]


def get_range(connection, table, col):
    query = f"""
    SELECT MIN({col}), MAX({col})
    FROM {table};
    """
    return connection.execute(query).fetchall()[0]


def connect_read_sql(query, engine):
    connection = engine.connect()
    result = pd.read_sql(query, connection)
    connection.close()
    return result
