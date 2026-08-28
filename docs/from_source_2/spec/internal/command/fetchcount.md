# FetchCount — 内部仕様書

**ファイル**: `src/yklibpy/command/fetchcount.py`  
**継承**: なし

## 概要

取得履歴 DB の数値キーを世代番号として扱い、更新要否に応じて新規または最新の取得回数を選択する。

---

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `fetch_count` | `int` | 選択された取得回数。 |
| `needness_of_refresh` | `bool` | 新しい世代を採番するか。 |
| `needness_of_top_dir` | `bool` | 呼び出し側から受け取るトップディレクトリ要否。 |
| `appstore` | `AppStore` | 履歴の永続化先。 |
| `fetch_assoc` | `dict[str, str]` | 更新後の履歴。 |

---

## メソッド

### `__init__(needness_of_refresh, needness_of_top_dir, appstore) -> None`

状態を初期化し、更新が必要なら次番号を採番し、不要なら DB の数値キー最大値を選ぶ。

### `get() -> int`

現在の取得回数を返す。

### `output_db() -> None`

保持中の履歴を取得 DB へ書き戻す。

### `get_next_count() -> int`

DB の履歴を読み、`_next_count` で更新して次番号を返す。

### `_next_count(fetch_assoc) -> tuple[int, dict[str, str]]`

空履歴なら1を、既存履歴なら数値キー最大値の次を現在時刻とともに追加して返す。数値でないキーは無視する。

---

## 依存

| クラス/変数 | 用途 |
|-------------|------|
| `AppStore` | 履歴 DB の読み書き。 |
| `AppConfig.BASE_NAME_FETCH` | 履歴ファイル識別子。 |
| `Timex.get_now` | 採番日時。 |

## 設計上の注意

`needness_of_top_dir` は保存されるだけでクラス内では参照されない。更新不要時に読込エラーや空履歴があっても `fetch_count=1` となる一方、`fetch_assoc` は更新されない。
