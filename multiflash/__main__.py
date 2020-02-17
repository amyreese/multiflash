# Copyright 2020 John Reese
# Licensed under the MIT License

import click

from multiflash.dataset import Fact, Facts, connect, set_default
from multiflash.quiz import Quiz


@click.group(context_settings={"help_option_names": ["-h", "--help"]},)
@click.option(
    "--db",
    help="location of dataset",
    type=click.Path(dir_okay=False, file_okay=True, writable=True, resolve_path=True),
    default=None,
)
@click.pass_context
def multiflash(ctx, db):
    """Interact with the multiflash database"""
    if db is not None:
        set_default(db)


@multiflash.command("add")
@click.argument("class_name")
@click.argument("topic")
@click.argument("keyword")
@click.argument("description")
@click.argument("values", nargs=-1)
def add(class_name, topic, keyword, description, values):
    """Add a new fact to the dataset"""
    fact = Fact(class_name, topic, keyword, description, "|||".join(values))
    db, engine = connect()
    db.execute(*engine.prepare(Facts.insert().values(fact)))
    db.commit()


@multiflash.command("list")
@click.argument("class_name", required=False, default=None)
def list(class_name):
    """List facts"""
    db, engine = connect()
    query = Facts.select()
    if class_name:
        query.where(Facts.class_name == class_name)
    sql, parameters = engine.prepare(query)
    sql += " ORDER BY class_name ASC, topic ASC, keyword ASC"
    cursor = db.execute(*engine.prepare(query))
    for row in cursor:
        fact = Fact(**row)
        print(
            f"{fact.class_name} | {fact.topic} | {fact.keyword} | "
            f"{fact.description} | {fact.values}"
        )


@multiflash.command("quiz")
@click.argument("class_name")
def quiz(class_name):
    """Take a quiz"""
    quiz = Quiz(class_name)
    quiz.start()


@multiflash.command("gui")
def gui():
    """Start the Multiflash GUI"""
    from multiflash.gui import start

    start()


if __name__ == "__main__":
    multiflash(prog_name="multiflash")  # pylint: disable=all
