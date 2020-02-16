# Copyright 2020 John Reese
# Licensed under the MIT License

import sqlite3
from pathlib import Path
from typing import List, Optional, Tuple

import appdirs
from attr import dataclass
from aql import table, Table, Column
from aql.engines.sqlite import SqliteEngine

DEFAULT_LOCATION: Optional[str] = None
CREATED: bool = False


@dataclass
class Fact:
    class_name: str
    topic: str
    keyword: str
    description: str
    values: str


Facts = Table(
    "facts",
    [
        Column("class", str),
        Column("topic", str),
        Column("keyword", str),
        Column("description", str),
        Column("values", str),
    ],
    source=Fact,
)


def connect(location: Optional[str] = None) -> Tuple[sqlite3.Connection, SqliteEngine]:
    global CREATED

    if location is None:
        location = DEFAULT_LOCATION

    if location is None:
        loc = Path(appdirs.user_data_dir("multiflash", "N7.gg")) / "facts.sqlite"
    else:
        loc = Path(location)

    if not loc.parent.exists():
        loc.parent.mkdir(parents=True, exist_ok=True)

    print(f"connecting to {loc!r}")

    db = sqlite3.connect(loc)
    db.row_factory = sqlite3.Row
    engine = SqliteEngine()

    if not CREATED:
        query = engine.prepare(Facts.create(if_not_exists=True))
        db.execute(*query)
        db.commit()
        CREATED = True

    return db, engine


def set_default(location: Optional[str] = None):
    global DEFAULT_LOCATION
    DEFAULT_LOCATION = location
