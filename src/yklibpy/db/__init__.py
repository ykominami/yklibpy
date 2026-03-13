from yklibpy.common.loggerx import Loggerx
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
    """`kind` に応じた DB オブジェクトを生成する。

    現在は YAML バックエンドだけを扱い、未対応の種類では `None` を返す。
    """
    if kind.lower() == "yaml":
        db = DbYaml(fname)
    else:
        db = None
    return db


def db_yaml_x() -> DbYaml:
    """既定ファイル名 `db.yml` を使う `DbYaml` を返す。"""
    return db_yaml("db.yml")


def db_yaml(db_file: str) -> DbYaml:
    """YAML DB を読み込み、初期データを書き込んで返す。

    テストや簡易利用向けに `name` キーへ初期値を設定する。
    """
    db = get_or_create_db("yaml", db_file)
    if db is None:
        raise ValueError("Failed to create database")
    db.load()
    db.set_item("name", "John")
    return db


if __name__ == "__main__":
    fname = "db.yaml"
    db = get_or_create_db("yaml", fname)
    Loggerx.debug(f"db={db}", __name__)
