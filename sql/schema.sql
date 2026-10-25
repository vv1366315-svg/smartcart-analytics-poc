-- SmartCart demo analytics schema (SQLite)
CREATE TABLE IF NOT EXISTS events (
    event_id INTEGER PRIMARY KEY,
    user_id TEXT NOT NULL,
    session_id TEXT NOT NULL,
    event_timestamp TEXT NOT NULL,
    event_name TEXT NOT NULL,
    product_id TEXT,
    product_name TEXT,
    price REAL,
    quantity INTEGER DEFAULT 1,
    source TEXT,
    device TEXT,
    is_synthetic INTEGER DEFAULT 1
);
