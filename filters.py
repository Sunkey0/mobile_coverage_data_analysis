import duckdb

def connect_to_duckdb(data):
    con = duckdb.connect(database=':memory:')
    con.register('data', data)
    return con

def apply_filters(con, año_seleccionado, trimestre_seleccionado, departamento_seleccionado):
    query = """
        SELECT * FROM data
        WHERE AÑO = ? AND TRIMESTRE = ?
    """
    params = [año_seleccionado, trimestre_seleccionado]

    if departamento_seleccionado:
        query += " AND DEPARTAMENTO IN ({})".format(", ".join(["'{}'".format(d) for d in departamento_seleccionado]))

    return con.execute(query, params).fetchdf()
