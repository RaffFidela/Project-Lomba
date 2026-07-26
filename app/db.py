import sqlite3
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    db.execute('''
        CREATE TABLE IF NOT EXISTS laporan (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            kelas TEXT NOT NULL,
            lokasi TEXT NOT NULL,
            deskripsi TEXT NOT NULL,
            status TEXT DEFAULT 'Menunggu',
            waktu_lapor TEXT,
            waktu_selesai TEXT,
            foto1 TEXT,
            foto2 TEXT,
            foto3 TEXT
        )
    ''')
    db.commit()

def init_app(app):
    app.teardown_appcontext(close_db)
