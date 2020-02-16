# Copyright 2020 John Reese
# Licensed under the MIT License

import click
from .dataset import connect, set_default, Facts, Fact


@click.group(context_settings={"help_option_names": ["-h", "--help"]},)
@click.option(
    "--db",
    help="location of dataset",
    type=click.Path(dir_okay=False, file_okay=True, writable=True, resolve_path=True),
    default=None,
)
def multiflash(db):
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


if __name__ == "__main__":
    multiflash(prog_name="multiflash")  # pylint: disable=all
