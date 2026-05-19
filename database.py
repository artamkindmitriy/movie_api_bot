import sqlite3
from datetime import datetime

DB_NAME = "bot_history.db"


def init_db():
    """Инициализация базы данных и создание таблицы истории"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS search_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            search_date TEXT NOT NULL,
            movie_id INTEGER NOT NULL,
            title TEXT,
            description TEXT,
            rating REAL,
            year INTEGER,
            genre TEXT,
            age_rating TEXT,
            poster_url TEXT,
            is_watched INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()


def add_to_history(user_id: int, movie_data: dict):
    """Сохраняет найденный фильм в историю поиска текущего пользователя"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    current_date = datetime.now().strftime("%Y-%m-%d")

    genres_list = movie_data.get("genres", [])
    genre_string = ", ".join([g.get("name") for g in genres_list if g.get("name")])

    movie_id = movie_data.get("id")
    title = movie_data.get("name") or movie_data.get("alternativeName") or "Без названия"
    description = movie_data.get("description") or "Описание отсутствует."
    year = movie_data.get("year")
    age_rating = movie_data.get("ageRating") or "Не указан"

    rating = movie_data.get("rating", {}).get("kp") or movie_data.get("rating", {}).get("imdb") or 0.0
    poster_url = movie_data.get("poster", {}).get("url")

    cursor.execute("""
        INSERT INTO search_history (
            user_id, search_date, movie_id, title, 
            description, rating, year, genre, age_rating, poster_url
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id, current_date, movie_id, title,
        description, rating, year, genre_string, age_rating, poster_url
    ))

    conn.commit()
    conn.close()


def get_user_history(user_id: int, date_str: str = None) -> list:
    """
    Возвращает историю поиска пользователя.
    Если передана строка даты (ГГГГ-ММ-ДД), фильтрует историю за этот день.
    """
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    if date_str:
        cursor.execute("""
            SELECT * FROM search_history 
            WHERE user_id = ? AND search_date = ? 
            ORDER BY id DESC
        """, (user_id, date_str))
    else:
        cursor.execute("""
            SELECT * FROM search_history 
            WHERE user_id = ? 
            ORDER BY search_date DESC, id DESC
        """, (user_id,))

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


def toggle_watched(user_id: int, movie_id: int) -> int:
    """
    Переключает статус фильма (просмотрено/не просмотрено).
    Возвращает новый статус (0 или 1).
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT is_watched FROM search_history WHERE user_id = ? AND movie_id = ? LIMIT 1",
                   (user_id, movie_id))
    result = cursor.fetchone()

    new_status = 0
    if result:
        new_status = 1 if result[0] == 0 else 0
        cursor.execute("UPDATE search_history SET is_watched = ? WHERE user_id = ? AND movie_id = ?",
                       (new_status, user_id, movie_id))
        conn.commit()

    conn.close()
    return new_status

if __name__ == "__main__":
    init_db()
    print("База данных и таблицы успешно инициализированы в файле bot_history.db!")