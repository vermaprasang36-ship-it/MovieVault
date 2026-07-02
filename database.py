import sqlite3

DB_NAME = "movievault.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS watchlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tmdb_id INTEGER UNIQUE NOT NULL,
            title TEXT NOT NULL,
            release_date TEXT,
            rating REAL,
            overview TEXT,
            poster_url TEXT,
            watched INTEGER DEFAULT 0,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

def add_movie_to_watchlist(tmdb_id, title, release_date, rating, overview, poster_url):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO watchlist
        (tmdb_id, title, release_date, rating, overview, poster_url)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (tmdb_id, title, release_date, rating, overview, poster_url))

    conn.commit()
    conn.close()

def get_all_watchlist_movies():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM watchlist ORDER BY added_at DESC")

    movies = cursor.fetchall()

    conn.close()
    return movies

def remove_movie_from_watchlist(tmdb_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM watchlist WHERE tmdb_id = ?", (tmdb_id,))

    conn.commit()
    conn.close()

def update_watched_status(tmdb_id, watched):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE watchlist SET watched = ? WHERE tmdb_id = ?",
        (1 if watched else 0, tmdb_id)
    )

    conn.commit()
    conn.close()

def is_movie_in_watchlist(tmdb_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT 1
        FROM watchlist
        WHERE tmdb_id = ?
        """,
        (tmdb_id,)
    )

    exists = cursor.fetchone() is not None

    conn.close()

    return exists


if __name__ == "__main__":
    create_tables()
    print("Database setup completed successfully.")


