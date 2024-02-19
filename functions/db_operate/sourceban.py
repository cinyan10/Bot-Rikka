import mysql.connector
import mysql.connector
from configs.database import db_config

db_config['database'] = 'sourceban'


def query_sb_servers():
    cursor = None
    conn = None
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM sourceban.sb_servers ORDER BY sid"
        cursor.execute(query)

        data = cursor.fetchall()
        return data

    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    result = query_sb_servers()
    print(result)
