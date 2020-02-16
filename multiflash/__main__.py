# Copyright 2020 John Reese
# Licensed under the MIT License

import click


@click.group("multiflash")
def main():
    pass


@main.group("class")
def _class():
    pass


@_class.command("create")
@click.argument("name", type=str)
def class_create(name: str):
    pass


@main.group("topic")
def topic():
    pass


@topic.command("create")
@click.argument("class_name", type=str)
def topic_create(class_name: str):
    pass


if __name__ == "__main__":
    main()
