from airflow.providers.postgres.hooks.postgres import PostgresHook

def connect_db(id):
    postgres_hook = PostgresHook(postgres_conn_id=f"{id}_study")
    return postgres_hook

def query_dql_db(id,sql):
    with connect_db(id).get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
    return result

def query_dml_db(id,sql):
    with connect_db(id).get_conn() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql)
        conn.commit()

def copy_csv_db(id,sql,csv_path):
    with connect_db(id).get_conn() as conn:
        with conn.cursor() as cursor:
            with open(csv_path, 'r') as f:
                cursor.copy_expert(sql,f)
        conn.commit()