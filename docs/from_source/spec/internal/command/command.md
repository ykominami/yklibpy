# Command — 内部仕様書

**ファイル**: `src/yklibpy/command/command.py`
**継承**: なし

## 概要

外部コマンド（サブプロセス）の実行と、取得回数（実行世代）の管理を提供する基底クラス。`CommandGhUser` などサイト固有/サービス固有のコマンド実行クラスの基底クラスとして使われる。

---

## メソッド

### `__init__() -> None`

互換性維持のための空初期化を行う（`pass` のみ）。

### `run_command(command: str | list[str], shell: bool = False, encoding: str = "utf-8", timeout: Optional[int] = None) -> tuple[str, int]`

コマンドを実行し、標準出力と終了コードのタプルを返す。呼び出し先コマンドの標準出力に指定エンコーディングで不正なバイト列が含まれていても例外にせず、置換文字（U+FFFD）に置き換えて継続する（`errors="replace"`）。

**Raises**: `subprocess.TimeoutExpired` — `timeout` を超過した場合、`cmd`/`timeout`/`stdout`/`stderr` を詰め直した新規の `subprocess.TimeoutExpired` を組み立てて送出する（元の例外オブジェクトをそのまま再送出するのではない。`output`/`stderr` は `None` なら空文字に、`timeout` は `None` なら `0.0` に置き換わる）。`subprocess.SubprocessError` — その他のサブプロセスエラー（引数なしの `raise` による捕捉した例外オブジェクトそのものの再送出）。

### `run_command_simple(command: str | list[str], shell: bool = False) -> str`

終了コードを検査しながらコマンドを実行し、標準出力を返す（`check=True`）。標準出力に UTF-8 として不正なバイト列が含まれていても例外にせず、置換文字に置き換えて継続する。

**Raises**: `subprocess.CalledProcessError` — コマンドが非 0 で終了した場合（`logging.exception` でログ出力後に再送出）。

### `run_command_simple_with_count(appstore: AppStore, command: str | list[str], shell: bool = False, *, force: bool = False, verbose: bool = False) -> str`

取得回数に応じてコマンド実行を制御し、必要時のみ出力を返す。

```
処理フロー:
  1. get_next_count(appstore) で実行世代番号を採番・記録
  2. count == 1 または force=True のときだけ実際にコマンドを実行し出力を得る（それ以外は空文字）
  3. verbose=True なら appstore.show で DB 内容をログ出力
  4. 得られた出力（または空文字）を返す
```

### `get_next_count(appstore: AppStore) -> int`

保存済みの実行履歴（`AppConfig.BASE_NAME_FETCH`）から次の実行世代番号を採番し、`Timex.get_now()` のタイムスタンプ付きで `AppStore.output_db` により DB へ記録したうえで返す。

```
処理フロー:
  1. appstore.get_file_assoc_from_db(BASE_NAME_FETCH) の戻り値（OpResult[Any]）を検査し、
     成功（ok=True）なら value を履歴辞書（dict[str, str] | None）として取り出す。
     失敗（ok=False）なら None（履歴なし）として扱う
  2. 履歴が空/None なら next_count = 1 とし、新規履歴 {"1": Timex.get_now()} を作る
  3. 既存履歴があれば数値化できるキーの最大値 + 1 を next_count とし、タイムスタンプを追記
     （数値化できないキーは無視。数値化できるキーが 1 つも無い場合は next_count = 1 となる）
  4. 更新後の履歴を appstore.output_db で DB へ書き戻し、next_count を返す
```

---

## 依存

| クラス/変数 | 用途 |
|-------------|------|
| `AppStore` | 実行履歴（fetch カウント）の読み書き（`get_file_assoc_from_db`/`output_db`）と内容のデバッグログ出力（`show`） |
| `AppConfig` | 取得履歴ファイルのベース名定数（`BASE_NAME_FETCH`）と DB 種別キーの定数（`KIND_DB`） |
| `Timex` | 実行時刻の記録 |

---

## 設計上の注意

- `get_next_count()` は `AppStore.get_file_assoc_from_db` の戻り値（`OpResult[Any]`）を辞書として直接扱わず、`ok` を確認したうえで `value` を取り出す。取得失敗（`ok=False`、DB 未登録による `KeyError` 等）は「履歴なし」として扱い、採番は `1` から開始する。`value` は `Any` のため `cast(dict[str, str] | None, ...)` で辞書とみなしている。
- `AppStore.get_file_assoc_from_db` は読み込み済みの `VALUE` を返す実装（`appstore.md` 参照）のため、DB ファイルが存在していても事前に `AppStore.load_file_db` 等でロードされていなければ `ok=False` となり「履歴なし」と誤認する。この場合 `get_next_count()` は新規履歴 `{"1": ...}` を `AppStore.output_db` で書き戻すため、既存の世代履歴をファイルごと上書きして失う点に注意。
- `run_command_simple_with_count()` は「初回（count==1）または force のときだけ実行する」というキャッシュ的な制御ロジックだが、`get_next_count()` はコマンドを実際に実行しない場合でも履歴カウントを進めて DB へ書き戻す。呼び出しのたびに世代番号が増える副作用がある点に注意（設計課題として記録する）。
- `CommandGhUser` は本クラスを継承しつつ `CommandGhUser.__init__` を独自に空実装でオーバーライドしており、`run_command_simple_with_count()` の `appstore` 連携機能は使っていない。
