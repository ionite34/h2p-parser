# Local Read/Write Cache for Transformed and User-Defined Resolutions
from __future__ import annotations

import sqlite3
from sqlite3 import Error
from typing import Any, Tuple
from . import format_ph
from . import DATA_PATH


_cache_db = 'cache.db'


class DictCache:
    def __init__(self):
        self._cache = {}
        self._check_db_table()

    # Check if database table exists, if not create it
    @staticmethod
    def _check_db_table():
        with DATA_PATH.joinpath(_cache_db) as f, sqlite3.connect(str(f)) as db:
            # Word, Phoneme, Source
            # Word is the default key, phoneme is the value
            # Word cannot have duplicate entries
            # Word and Phoneme cannot be null
            db.execute('''CREATE TABLE IF NOT EXISTS cache
                                (
                                    word TEXT primary key not null on conflict ignore,
                                    phoneme TEXT not null,
                                    source_parser TEXT,
                                    checked BOOLEAN default false
                                )''')

    # Loads database to dictionary
    def load(self):
        with DATA_PATH.joinpath(_cache_db) as f:
            with sqlite3.connect(str(f)) as db:
                self._check_db_table()
                cursor = db.cursor()
                cursor.execute('''SELECT word, phoneme, source_parser, checked FROM cache''')
                for row in cursor.fetchall():
                    self._cache[row[0]] = (row[1], row[2], row[3])

    # Saves dictionary to database
    def save(self):
        with DATA_PATH.joinpath(_cache_db) as f:
            db = sqlite3.connect(str(f))
            cursor = db.cursor()
            for word in self._cache:
                phoneme, source, checked = self._cache[word]
                cursor.execute('''INSERT OR REPLACE INTO cache 
                                        VALUES (?, ?, ?, ?)''', (word, phoneme, source, checked))
            db.commit()
            db.close()

    # Get the phoneme for a word
    def get(self, word: str) -> tuple[Any, Any, Any] | None | Any:
        # Returns a tuple of (phoneme, source, checked)
        return self._cache.get(word)

    # Add a new word-phoneme entry to the sqlite3 database
    def add(self, word: str, phoneme: str, source: str = None, checked: bool = False):
        if word in self._cache:
            return
        # Convert all phonemes to sds
        ph = format_ph.to_sds(phoneme)
        self._cache[word] = (ph, source, checked)  # Also add to cache
