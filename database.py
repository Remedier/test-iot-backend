import sqlite3

# SQLite 데이터베이스 연결
conn = sqlite3.connect("sensor_data.db", check_same_thread=False)
cursor = conn.cursor()

# 센서 데이터를 저장할 테이블 생성
cursor.execute("""
    CREATE TABLE IF NOT EXISTS sensor_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        value REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()

def insert_sensor_data(value):
    """ 센서 데이터를 저장하는 함수 """
    cursor.execute("INSERT INTO sensor_data (value) VALUES (?)", (value,))
    conn.commit()

def get_latest_sensor_data(limit=10):
    """ 최근 저장된 센서 데이터를 가져오는 함수 """
    cursor.execute("SELECT * FROM sensor_data ORDER BY id DESC LIMIT ?", (limit,))
    return cursor.fetchall()
