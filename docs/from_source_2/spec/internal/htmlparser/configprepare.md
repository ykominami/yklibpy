# ConfigPrepare — 内部仕様書

**ファイル**: `src/yklibpy/htmlparser/configprepare.py`  
**継承**: なし

## 概要

HTML パーサ関連の設定辞書とその基準ファイル位置を保持し、既知の設定階層へ簡潔にアクセスする。

---

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `parent_file_path` | `Path` | 設定の基準となる親ファイル位置。 |
| `assoc` | `dict[str, Any]` | 設定値を保持する辞書。 |

---

## メソッド

### `__init__(parent_file_path: Path, assoc: dict[str, Any]) -> None`

基準パスと設定辞書を保持する。

### `get(key: str) -> Any`

トップレベルの指定キーに対応する値を返す。

**Raises**: `KeyError` — キーが設定辞書に存在しない場合。

### `get_command() -> Any`

`command` セクションを返す。

### `get_command_dir() -> Any`

`command.dir` の値を返す。

### `get_category_config_file_extname() -> Any`

`category-config-file-extname` の値を返す。

### `get_utility_category() -> Any`

`command.utility-category` の値を返す。

### `get_utility_root() -> Any`

`command.utility-root` の値を返す。

### `get_category() -> Any`

`category` セクションを返す。

### `get_htmlparser() -> Any`

`category.htmlparser` の値を返す。

## 依存

| クラス/変数 | 用途 |
|-------------|------|
| `Path` | 設定ファイル位置の表現。 |

## 設計上の注意

全アクセサーは辞書の直接添字参照を使うため、必須キーの欠落時には `KeyError` が伝播する。戻り値は `Any` であり、型や値の妥当性検証は行わない。
