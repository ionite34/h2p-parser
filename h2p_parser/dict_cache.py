# Local Read/Write Cache for Transformed and User-Defined Resolutions
from __future__ import annotations

import csv
import sqlite3
from sqlite3 import Error
from typing import Any, Tuple
from . import format_ph
from . import DATA_PATH


class DictCache:
    def __init__(self, db_name='cache.db'):
        self._db_name = db_name
        self._cache = {}
        self._check_db_table()

    # Check if database table exists, if not create it
    def _check_db_table(self):
        with DATA_PATH.joinpath(self._db_name) as f, sqlite3.connect(str(f)) as db:
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

    # Check entries affected by clear
    def check_clear(self, clear_all: bool = False) -> tuple[int, int]:
        with DATA_PATH.joinpath(self._db_name) as f, sqlite3.connect(str(f)) as db:
            # Check how many entries will be cleared
            # First get the total number of entries
            entries = db.execute('''SELECT COUNT(*) FROM cache''').fetchone()[0]
            if not clear_all:
                cursor = db.execute('''SELECT COUNT(*) FROM cache WHERE checked = 0''')
                affected = cursor.fetchone()[0]
            else:
                affected = entries
            # Return result
            return affected, entries

    # Clear the non-confirmed entries
    def clear(self, clear_all: bool = False):
        self._cache.clear()
        with DATA_PATH.joinpath(self._db_name) as f, sqlite3.connect(str(f)) as db:
            if not clear_all:
                db.execute('''DELETE FROM cache WHERE checked = 0''')
            else:
                db.execute('''DELETE FROM cache''')
            db.commit()

    # Loads database to dictionary
    def load(self):
        with DATA_PATH.joinpath(self._db_name) as f:
            with sqlite3.connect(str(f)) as db:
                self._check_db_table()
                cursor = db.cursor()
                cursor.execute('''SELECT word, phoneme, source_parser, checked FROM cache''')
                for row in cursor.fetchall():
                    self._cache[row[0]] = (row[1], row[2], row[3])

    # Saves dictionary to database
    def save(self):
        with DATA_PATH.joinpath(self._db_name) as f:
            db = sqlite3.connect(str(f))
            cursor = db.cursor()
            for word in self._cache:
                phoneme, source, checked = self._cache[word]
                cursor.execute('''INSERT OR REPLACE INTO cache 
                                        VALUES (?, ?, ?, ?)''', (word, phoneme, source, checked))
            db.commit()
            db.close()

    # Export to Dictionary file
    def export(self, path, only_checked: bool = True, delimiter: str = '  '):
        with open(path, 'w', newline='') as write_f:
            with DATA_PATH.joinpath(self._db_name) as db_f, sqlite3.connect(str(db_f)) as db:
                self._check_db_table()
                cursor = db.cursor()
                if only_checked:
                    cursor.execute('''SELECT word, phoneme
                                        FROM cache WHERE checked = 1''')
                else:
                    cursor.execute('''SELECT word, phoneme FROM cache''')
                for row in cursor.fetchall():
                    write_f.write(row[0] + delimiter + row[1] + '\n')

    # Get the phoneme for a word
    def get(self, word: str) -> tuple[Any, Any, Any] | None | Any:
        # Returns a tuple of (phoneme, source, checked)
        return self._cache.get(word)

    # Add a new word-phoneme entry to the sqlite3 database
    def add(self, word: str, phoneme: str, source: str = None, checked: bool = False):
        # Convert all phonemes to sds
        ph = format_ph.to_sds(phoneme)
        self._cache[word] = (ph, source, checked)  # Also add to cache
