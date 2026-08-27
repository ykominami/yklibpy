# db.__init__ — 内部仕様書

**ファイル**: `src/yklibpy/db/__init__.py`

## 概要

ストレージ関連クラスを公開し、YAML DB の生成・初期化と疎通確認用エントリポイントを提供する。

---

## モジュールレベル定数・型

| 変数名 | 値/型 | 用途 |
|--------|-------|------|
| `__all__` | `list[str]` | DB クラスと補助関数を公開する。 |

## モジュールレベル関数

### `get_or_create_db(kind: str, fname: str) -> DbYaml | None`

`kind` が大文字小文字を問わず `yaml` の場合だけ `DbYaml` を生成する。

### `db_yaml_x() -> DbYaml`

`db.yml` を保存先とする `db_yaml()` の結果を返す。

### `db_yaml(db_file: str) -> DbYaml`

YAML DB を生成・ロードし、`name: John` をメモリ上に設定して返す。生成不能時は `ValueError` を送出する。

### `db_yaml_main() -> None`

既定 DB を初期化し、結果をデバッグログへ出す。

### `xmain() -> None` / `ymain() -> None`

各系統の疎通確認メッセージをログと標準出力へ出す。

---

## 依存

| クラス/変数 | 用途 |
|-------------|------|
| `DbYaml` | YAML バックエンド。 |
| `DbBase` / `Storex` / `AppStore` | パッケージ公開 API。 |
| `Loggerx` | 動作ログ。 |

## 設計上の注意

ファクトリは YAML 以外を黙って `None` とする。`db_yaml()` はロード直後のデータへ固定値を書き込むが、保存はしない。
