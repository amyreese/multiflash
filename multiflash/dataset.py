# Copyright 2020 John Reese
# Licensed under the MIT License

import sqlite3
from pathlib import Path
from typing import List, Optional, Tuple

import appdirs
from aql import table, Table
from aql.engines.sqlite import SqliteEngine

DEFAULT_LOCATION: Optional[str] = None
CREATED: bool = False


class Fact:
    class_name: str
    topic: str
    keyword: str
    description: str
    values: List[str]


Facts = table(Fact)


def connect(location: Optional[str] = None) -> Tuple[sqlite3.Connection, SqliteEngine]:
    global CREATED

    if location is None:
        location = DEFAULT_LOCATION

    if location is None:
        loc = Path(appdirs.user_data_dir("multiflash", "N7.gg")) / "facts.sqlite"
    else:
        loc = Path(location)

    db = sqlite3.connect(loc)
    engine = SqliteEngine()

    if not CREATED:
        query = engine.prepare(Facts.create(if_not_exists=True))
        db.execute(*query)
        CREATED = True

    return db, engine


def set_default(location: Optional[str] = None):
    global DEFAULT_LOCATION
    DEFAULT_LOCATION = location
