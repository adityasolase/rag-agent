import pymysql
import os
from urllib.parse import urlparse

def connect_db():
    db_url = os.getenv("MYSQL_URI", "mysql+pymysql://root:aviBvUaWAsiVtFUXtFbwVVpluUCUMrtB@trolley.proxy.rlwy.net:57861/railway")
    
    if db_url.startswith("mysql+pymysql://"):
        parse_url = db_url.replace("mysql+pymysql://", "mysql://")
    else:
        parse_url = db_url
        
    url = urlparse(parse_url)
    
    # Extract connection parameters
    user = url.username
    password = url.password
    host = url.hostname
    port = url.port or 3306
    database = url.path.lstrip('/')
    
    # Connect to the database
    return pymysql.connect(
        host=host,
        user=user,
        password=password,
        port=port,
        database=database
    )

def get_top_portfolios(limit=5):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT client_name FROM transactions ORDER BY value DESC LIMIT %s", (limit,))
    result = [row[0] for row in cursor.fetchall()]
    connection.close()
    return result

def get_manager_breakup():
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT manager_name, SUM(value) FROM transactions GROUP BY manager_name")
    result = [{"manager": row[0], "value": row[1]} for row in cursor.fetchall()]
    connection.close()
    return result

def get_top_holders(stock):
    connection = connect_db()
    cursor = connection.cursor()
    cursor.execute("SELECT client_name, value FROM transactions WHERE stock_name LIKE %s", ('%' + stock + '%',))
    rows = cursor.fetchall()
    connection.close()
    return {
        "labels": [r[0] for r in rows],
        "data": [r[1] for r in rows]
    }
