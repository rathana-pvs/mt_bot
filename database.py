import sqlite3

DB_NAME = "trading_bot.db"

def init_db():
    """Create the configuration table if it doesn't exist."""
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("PRAGMA journal_mode=WAL;")  # Enable concurrent read/write
        query = """
        CREATE TABLE IF NOT EXISTS bot_settings (
            acc_id INTEGER PRIMARY KEY,
            pair TEXT NOT NULL,
            lot_size REAL NOT NULL,
            grid_step INTEGER NOT NULL,
            tp REAL NOT NULL,
            max_position INTEGER NOT NULL,
            active INTEGER DEFAULT 1,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """
        conn.execute(query)
        conn.commit()

def find_by_acc_id(acc_id):
    """Retrieve settings for a specific account ID."""
    with sqlite3.connect(DB_NAME) as conn:
        conn.row_factory = sqlite3.Row  # Allows accessing columns by name
        cursor = conn.execute("SELECT * FROM bot_settings WHERE acc_id = ?", (acc_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def update_by_acc_id(acc_id, pair, lot_size, grid_step, tp, max_position, active=1):
    """Insert or Update the configuration for an account."""
    with sqlite3.connect(DB_NAME, timeout=5000) as conn:
        query = """
        INSERT INTO bot_settings (acc_id, pair, lot_size, grid_step, tp, max_position, active)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(acc_id) DO UPDATE SET
            pair=excluded.pair,
            lot_size=excluded.lot_size,
            grid_step=excluded.grid_step,
            tp=excluded.tp,
            max_position=excluded.max_position,
            active=excluded.active,
            updated_at=CURRENT_TIMESTAMP;
        """
        conn.execute(query, (acc_id, pair, lot_size, grid_step, tp, max_position, active))
        conn.commit()
