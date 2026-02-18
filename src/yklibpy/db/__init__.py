from yklibpy.db.db_base import DbBase
from yklibpy.db.db_yaml import DbYaml
from yklibpy.db.storex import Storex
from yklibpy.db.appstore import AppStore

__all__ = [
    "DbBase",
    "DbYaml",
    "Storex",
    "AppStore",
    "get_or_create_db",
    "db_yaml",
    "db_yaml_x",
]


def get_or_create_db(kind: str, fname: str) -> DbYaml | None:
    if kind.lower() == "yaml":
        db = DbYaml(fname)
    else:
        db = None
    return db


def db_yaml_x() -> DbYaml:
    return db_yaml("db.yml")


def db_yaml(db_file: str) -> DbYaml:
    db = get_or_create_db("yaml", db_file)
    if db is None:
        raise ValueError("Failed to create database")
    db.load()
    db.set_item("name", "John")
    # print(f"db={db.get_data()}")
    return db


if __name__ == "__main__":
    fname = "db.yaml"
    db = get_or_create_db("yaml", fname)
    print(f"db={db}")
