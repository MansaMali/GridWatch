import sqlite3

def create_connection():

    conn = sqlite3.connect("substation.db")

    return conn


def create_tables():

    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute("""
        Create Table IF NOT EXISTS telemetry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_id TEXT,
            metric TEXT,
            value REAL,
            timestamp TEXT
    )
""")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS health_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_id TEXT,
            health_status TEXT,
            health_score REAL,
            health_reason TEXT,
            timestamp TEXT
        )
""")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_id TEXT,
            previous_status,
            new_status,
            message TEXT,
            timestamp TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS security_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            asset_id TEXT,
            event_type TEXT,
            severity TEXT,
            source TEXT,
            description TEXT,
            status TEXT,
            timestamp TEXT
    )
""")
    

    conn.commit()

    conn.close()

    
def insert_telemetry(asset_id, metric, value, timestamp):

    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO telemetry
        (asset_id, metric, value, timestamp)
        VALUES(?, ?, ?, ?)
    """, (asset_id, metric,value,timestamp))

    conn.commit()

    conn.close()


def get_telemetry():
    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM telemetry
""")
    
    rows = cursor.fetchall()

    conn.close()

    return rows


def get_asset_telemetry(asset_id):

    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM TELEMETRY
        WHERE ASSET_ID = ?
        ORDER BY timestamp
        """, (asset_id,))
    
    rows = cursor.fetchall()

    conn.close()

    return rows


def get_average_metric(asset_id, metric):

    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute("""
    SELECT AVG(value)
    FROM telemetry
    WHERE asset_id = ?
    AND metric = ?
""", (asset_id, metric))
    
    result = cursor.fetchone()

    conn.close()

    return result[0]


def get_max_metric(asset_id, metric):

    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT MAX(value)
        FROM telemetry
        WHERE asset_id = ?
        AND metric = ?
""", (asset_id, metric))

    result = cursor.fetchone()

    conn.close()

    return result[0]


def get_latest_metric(asset_id, metric):

    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT value
        FROM telemetry
        WHERE asset_id = ?
        AND metric = ?
        ORDER BY id DESC
        LIMIT 1
""", (asset_id, metric))

    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]
    return None


def get_latest_readings(asset_id, metric, count):

    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT value
        FROM telemetry
        WHERE ASSET_ID = ?
        AND metric = ?
        ORDER BY id DESC
        LIMIT ?
""", (asset_id, metric, count))

    rows = cursor.fetchall()

    conn.close()

    return rows

def insert_health_reports(
    asset_id,
    health_status,
    health_score,
    health_reason,
    timestamp
):

    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO health_reports
        (asset_id, health_status, health_score, health_reason, timestamp)
        VALUES (?, ?, ?, ?, ?)
""", (
    asset_id,
    health_status,
    health_score,
    health_reason,
    timestamp
))

    conn.commit()

    conn.close()

def get_health_reports():

    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM health_reports
        ORDER BY id
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows

def insert_event(
    asset_id,
    previous_status,
    new_status,
    message,
    timestamp
):
    
    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO events
        (asset_id, previous_status, new_status, message, timestamp)
        VALUES (?, ?, ?, ? , ?)
""", (
    asset_id,
    previous_status,
    new_status,
    message,
    timestamp
))

    conn.commit()
    conn.close()

def get_events():

    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM events 
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


def insert_security_event(
    asset_id,
    event_type,
    severity,
    source,
    description,
    status,
    timestamp
):

    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO security_events
        (
            asset_id,
            event_type,
            severity,
            source,
            description,
            status,
            timestamp
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
""", (
    asset_id,
    event_type,
    severity,
    source,
    description,
    status,
    timestamp
))

    conn.commit()
    conn.close()

def get_security_events():

    conn = create_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM security_events
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows