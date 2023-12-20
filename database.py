import sqlite3

def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(conn):
    """Create a table if it doesn't exist."""
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS pdf_data (
        file_path TEXT PRIMARY KEY,
        last_page INTEGER
    );
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)

def save_last_viewed_page(conn, file_path, page_number):
    """Save the last viewed page number for a given PDF."""
    sql = ''' INSERT OR REPLACE INTO pdf_data (file_path, last_page)
              VALUES (?, ?); '''
    try:
        c = conn.cursor()
        c.execute(sql, (file_path, page_number))
        conn.commit()
    except sqlite3.Error as e:
        print(e)

def get_last_viewed_page(conn, file_path):
    """Get the last viewed page number for a given PDF."""
    sql = ''' SELECT last_page FROM pdf_data WHERE file_path = ?; '''
    try:
        c = conn.cursor()
        c.execute(sql, (file_path,))
        result = c.fetchone()
        return result[0] if result else 0
    except sqlite3.Error as e:
        print(e)
        return 0
