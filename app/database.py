import sqlite3


class URLDatabase:
    def __init__(self, db_path: str = "shortner.db"):
        self.connection = sqlite3.connect(db_path, check_same_thread=False)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS urls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                short_code TEXT UNIQUE,
                long_url TEXT NOT NULL
            )
        """)
        self.connection.commit()

    def long_url_exists(self, long_url: str):
        """Returns the existing row if this long_url was already shortened, else None."""
        self.cursor.execute("SELECT * FROM urls WHERE long_url = ?", (long_url,))
        return self.cursor.fetchone()

    def insert_url(self, long_url: str) -> int:
        """Inserts a row with just the long_url. Returns the new row's id."""
        self.cursor.execute("INSERT INTO urls (long_url) VALUES (?)", (long_url,))
        self.connection.commit()
        assert self.cursor.lastrowid is not None
        return self.cursor.lastrowid

    def set_short_code(self, url_id: int, short_code: str):
        """Updates the row with its generated short_code."""
        self.cursor.execute(
            "UPDATE urls SET short_code = ? WHERE id = ?", (short_code, url_id)
        )
        self.connection.commit()

    def get_short_code_by_long_url(self, long_url: str) -> str | None:
        """Returns the existing short_code for this long_url, or None if not found."""
        self.cursor.execute(
            "SELECT short_code FROM urls WHERE long_url = ?", (long_url,)
        )
        row = self.cursor.fetchone()
        return row["short_code"] if row else None

    def get_by_code(self, short_code: str):
        self.cursor.execute("SELECT * FROM urls WHERE short_code = ?", (short_code,))
        return self.cursor.fetchone()

    def close(self):
        self.connection.close()
