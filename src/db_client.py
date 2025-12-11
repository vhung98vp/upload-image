import psycopg2
from psycopg2 import sql
# from psycopg2.extras import execute_values
from config import DB, TABLE


def get_connection(db_name=DB["name"]):
    return psycopg2.connect(
        host=DB["host"],
        port=DB["port"],
        dbname=db_name,
        user=DB["user"],
        password=DB["password"]
    )


def ensure_db():
    conn = get_connection("postgres")
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB["name"],))
    exists = cur.fetchone()
    if not exists:
        cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DB["name"])))
        print(f"Database {DB['name']} created")

    cur.close()
    conn.close()

def ensure_table(table_name=TABLE["name"]):
    conn = get_connection()
    cur = conn.cursor()

    columns = [f"{col} {col_type}" for col, col_type in TABLE["fields"].items()]
    columns.append("id SERIAL PRIMARY KEY")
    columns.append("created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
    query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})"
    cur.execute(query)

    conn.commit()
    cur.close()
    conn.close()


def save_data(user_id, saved_path):
    if not user_id or not saved_path:
        return
    conn = get_connection()
    cur = conn.cursor()

    query = f"""
        INSERT INTO {TABLE["name"]} ({", ".join(TABLE["fields"].keys())})
        VALUES (%s, %s)
    """

    cur.execute(query, (user_id, saved_path))
    conn.commit()
    cur.close()
    conn.close()


ensure_db()
ensure_table()