# -*- coding: utf-8 -*-
"""SQLite score storage, one table per world (was game_db.py).

The only change from the original is that the database path is resolved with the
cross-platform :func:`paths.user_data_dir` instead of a Windows-only
``os.environ['LOCALAPPDATA']`` lookup at import time.
"""
import os
import sqlite3
from datetime import datetime

from . import paths

TABLES = ['world_1', 'world_2', 'world_3', 'world_4', 'world_5']


def db_path():
    """Absolute path to scores.db inside the per-user data directory."""
    return os.path.join(paths.user_data_dir(), 'scores.db')


def init_database():
    """Create the database and its per-world tables if they do not exist."""
    conn = sqlite3.connect(db_path())
    c = conn.cursor()
    for table in TABLES:
        c.execute(f"""CREATE TABLE IF NOT EXISTS {table} (
            id INTEGER PRIMARY KEY,
            score INTEGER,
            date TEXT
        );
        """)
    conn.commit()
    conn.close()


def save_value_to_database(score, world_number):
    """Insert a score (with the current date/time) into the given world's table."""
    conn = sqlite3.connect(db_path())
    cursor = conn.cursor()
    column_name = f"world_{world_number}"
    query = f"INSERT INTO {column_name} (score, date) VALUES (?, ?)"
    date = datetime.now().strftime('%d-%m-%Y %H:%M')
    try:
        cursor.execute(query, (score, date))
        conn.commit()
    except sqlite3.Error as e:
        print("Erreur dans la sauvegarde de score :", e)
    cursor.close()
    conn.close()


def get_highest_score_and_date(world_number):
    """Return ``(score, date)`` of the best run for a world, or ``(None, None)``."""
    conn = sqlite3.connect(db_path())
    cursor = conn.cursor()
    column_name = f"world_{world_number}"
    query = f"SELECT score, date FROM {column_name} ORDER BY score DESC LIMIT 1"
    try:
        cursor.execute(query)
        result = cursor.fetchone()
        if result:
            highest_score, date = result
            return highest_score, date
        else:
            return None, None
    except sqlite3.Error as e:
        print("Erreur dans le renvoi de score :", e)
        return None, None
    finally:
        cursor.close()
        conn.close()


def wipe_table_contents():
    """Empty every world table (used when the player resets their save)."""
    try:
        conn = sqlite3.connect(db_path())
        cursor = conn.cursor()
        for table_name in TABLES:
            cursor.execute(f"DELETE FROM {table_name};")
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print("Erreur dans la suppression du contenu des tables :", e)
