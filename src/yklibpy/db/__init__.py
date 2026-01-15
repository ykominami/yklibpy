from .db_yaml import DbYaml


def get_or_create(kind, fname):
    if kind.lower() == "yaml":
        db = DbYaml(fname)
    else:
        db = None
    return db


def db_yaml():
    db = get_or_create("yaml", "db.yaml")
    db.load()
    db.set_item("name", "John")
    print(f"db={db.dump()}")
    return db


__all__ = ["DbYaml", "get_or_create", "db_yaml"]

if __name__ == "__main__":
    fname = "db.yaml"
    db = get_or_create("db_yaml", fname)
    print(f"db={db}")
