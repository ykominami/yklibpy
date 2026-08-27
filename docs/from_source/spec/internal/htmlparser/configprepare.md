# ConfigPrepare — 内部仕様書

**ファイル**: `src/yklibpy/htmlparser/configprepare.py`
**継承**: なし

## 概要

HTML パーサ関連設定（YAML 由来の連想配列）へのアクセスを、キー名を意識せず読み出せるように簡略化するアクセサクラス。

---

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `parent_file_path` | `Path` | 設定ファイルの親ディレクトリ。 |
| `assoc` | `dict[str, Any]` | 設定内容そのもの。 |

---

## メソッド

### `__init__(parent_file_path: Path, assoc: dict[str, Any]) -> None`

親ディレクトリと設定辞書を保持する。

### `get(key: str) -> Any`

指定キーに対応する設定値を返す。

### `get_command() -> Any`

`command` セクション全体を返す。

### `get_command_dir() -> Any`

コマンド関連ファイルの配置ディレクトリ（`command.dir`）を返す。

### `get_category_config_file_extname() -> Any`

カテゴリ設定ファイルの拡張子（`category-config-file-extname`）を返す。

### `get_utility_category() -> Any`

ユーティリティカテゴリ一覧（`command.utility-category`）を返す。

### `get_utility_root() -> Any`

ユーティリティ探索の起点設定（`command.utility-root`）を返す。

### `get_category() -> Any`

`category` セクション全体を返す。

### `get_htmlparser() -> Any`

HTML パーサ用カテゴリ設定（`category.htmlparser`）を返す。

---

## 依存

なし（内部の `assoc` 辞書のみ）。

---

## 設計上の注意

すべてのアクセサが辞書キーの存在を検証しないため、設定ファイルにキーが欠けていると `KeyError` が送出される。呼び出し元（`Preparex` 等）ではこの例外を捕捉していない箇所があり、設定ファイルの不整合がそのまま例外として伝播する。
