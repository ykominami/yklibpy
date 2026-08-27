# FetchCount — 内部仕様書

**ファイル**: `src/yklibpy/command/fetchcount.py`
**継承**: なし

## 概要

取得済みデータ（GitHub からのダウンロード等）の世代番号（何回目の取得か）を管理するクラス。更新が必要な場合は新しい番号を採番し、不要な場合は既存履歴から最新番号を選択する。履歴の実体は `AppStore` 経由で読み書きする取得履歴辞書（連番文字列 → タイムスタンプ）である。

---

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `fetch_count` | `int` | 選択された取得回数。初期値 `-1`（コンストラクタ内で必ず上書きされる）。 |
| `needness_of_refresh` | `bool` | 新規ダウンロードが必要かどうか。 |
| `needness_of_top_dir` | `bool` | トップディレクトリの新規作成が必要かどうか（コンストラクタで受け取り保持されるのみで、クラス内のどのメソッドからも参照されていない未使用フィールド）。 |
| `appstore` | `AppStore` | 取得履歴 DB へのアクセス元。 |
| `fetch_assoc` | `dict[str, str]` | 取得履歴（連番文字列 → タイムスタンプ）の辞書。初期値は空辞書で、`get_next_count()` 実行時のみ更新される。 |

---

## メソッド

### `__init__(needness_of_refresh: bool, needness_of_top_dir: bool, appstore: AppStore) -> None`

更新要否に応じて利用すべき取得回数を決定する。

```
処理フロー:
  1. needness_of_refresh が True なら get_next_count() で新規番号を採番し fetch_count に設定
  2. False なら appstore.get_file_assoc_from_db(BASE_NAME_FETCH) の戻り値（OpResult[Any]）を検査する
  3. 成功（ok=True）かつ value が None でなければ value を履歴辞書（dict[str, str] へ cast）として扱い、
     数値化できるキーの最大値（最低でも 1）を fetch_count に採用する（既存番号の選択であり、採番・履歴更新は行わない）
  4. 失敗（ok=False）または value が None の場合は空辞書を用いる（fetch_count は 1）
```

### `get() -> int`

現在選択されている取得回数を返す。

### `output_db() -> None`

計算済みの取得履歴（`self.fetch_assoc`）を `appstore.output_db(BASE_NAME_FETCH, ...)` で DB ファイルへ書き戻す。

### `get_next_count() -> int`

次の取得回数を採番し、更新後の履歴を `self.fetch_assoc` へ反映して返す。

```
処理フロー:
  1. appstore.get_file_assoc_from_db(BASE_NAME_FETCH) の戻り値（OpResult[Any]）を検査する
  2. 成功（ok=True）なら value（dict[str, str] | None へ cast）を、失敗（ok=False）なら None を _next_count へ渡す
  3. _next_count の結果（次番号・更新後履歴）を受け取り、履歴を self.fetch_assoc へ反映して次番号を返す
```

**Returns**: 次に使う取得回数。

DB ファイルへの書き戻しは行わない（メモリ上の `self.fetch_assoc` の更新のみ）。永続化には呼び出し側が別途 `output_db()` を呼ぶ必要がある。

### `_next_count(fetch_assoc: dict[str, str] | None) -> tuple[int, dict[str, str]]`

履歴辞書から次に使う取得回数と更新後辞書を求める。

```
処理フロー:
  1. 履歴が空/None なら次番号 1 とし、新規履歴 {"1": Timex.get_now()} を返す
  2. 既存履歴があれば数値化できるキーの最大値 + 1 を次番号とする
     （数値化できないキーは無視。数値化できるキーが 1 つも無い場合は次番号 1 となる）
  3. 次番号のタイムスタンプを Timex.get_now() で履歴へ追記し、(次番号, 更新後履歴) を返す
```

**Args**: `fetch_assoc` — 既存の履歴辞書。「履歴なし」は `None` または空辞書で表す。
**Returns**: 次に使う取得回数と、その番号のタイムスタンプを追記した更新後履歴のタプル。

---

## 依存

| クラス/変数 | 用途 |
|-------------|------|
| `AppStore` | 取得履歴 DB の読み書き（`get_file_assoc_from_db`/`output_db`） |
| `AppConfig` | 取得履歴ファイルのベース名定数（`BASE_NAME_FETCH`） |
| `Timex` | タイムスタンプ生成 |

---

## 設計上の注意

- `AppStore.get_file_assoc_from_db` は `OpResult[Any]` を返すため、戻り値を辞書として直接扱わず `ok` を確認したうえで `value` を取り出す。ただし検査条件と `cast` 先は分岐ごとに異なる: `__init__()` の `else` 分岐は `ok` かつ `value is not None` を検査して `dict[str, str]` へ、`get_next_count()` は `ok` のみ検査して `dict[str, str] | None` へ cast する（`value` が `None` の成功結果は `_next_count()` 側の「履歴なし」判定で吸収される）。
- 取得失敗（`ok=False`）は「履歴なし」として扱われる。`AppStore.get_file_assoc_from_db` は読み込み済みの `VALUE` を返す実装（`appstore.md` 参照）のため、DB ファイルが存在していても事前に `AppStore.load_file_db` 等でロードされていなければ `KeyError` → `ok=False` となり、番号が `1` へリセットされる点に注意。
- `get_next_count()` の docstring は「DB の履歴を更新しながら次の取得回数を返す」だが、実際に更新されるのはメモリ上の `self.fetch_assoc` のみで、DB ファイルへの書き戻しは `output_db()` の明示呼び出しが必要（docstring と実装の乖離）。同名の `Command.get_next_count` は採番と同時に `AppStore.output_db` まで行うため、挙動が異なる（`command.md` 参照）。
- `output_db()` が呼ぶ `AppStore.output_db` はファイルへの書き戻しのみを行い、メモリ上の `VALUE` を更新しない（`appstore.md` の「設計上の注意」参照）。そのため書き戻し後に `AppStore.get_file_assoc_from_db` を呼んでも反映前の古い履歴が返る。
- `needness_of_top_dir` はコンストラクタで受け取るのみで、クラス内のどのメソッドからも参照されていない（未使用フィールド）。
