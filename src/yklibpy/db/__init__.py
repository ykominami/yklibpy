from yklibpy.db.db_base import DbBase
from yklibpy.db.db_yaml import DbYaml

__all__ = ["DbBase", "DbYaml", "get_or_create_db", "db_yaml", "db_yaml_x"]

def get_or_create_db(kind, fname):
    if kind.lower() == "yaml":
        db = DbYaml(fname)
    else:
        db = None
    return db

def db_yaml_x() -> DbYaml:
    return db_yaml("db.yml")

def db_yaml(db_file:str) -> DbYaml:
    db = get_or_create_db("yaml", "db.yaml")
    if db is None:
        raise ValueError("Failed to create database")
    db.load()
    db.set_item("name", "John")
    print(f"db={db.dump()}")
    return db


__all__ = ["DbYaml", "get_or_create_db", "db_yaml"]

if __name__ == "__main__":
    fname = "db.yaml"
    db = get_or_create_db("db_yaml", fname)
    print(f"db={db}")
