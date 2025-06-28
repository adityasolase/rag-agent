import pymysql

def connect_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",  
        database="portfolio_db"
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
