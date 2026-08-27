# Command — 内部仕様書

## モジュール

`yklibpy.command.command`

## `__init__`

- `pass` のみ。`AppStore` への参照は持たず、各メソッドが引数で受け取る設計。

## メソッドの実装詳細

### `run_command`

- `subprocess.run` に `capture_output=True, text=True` を渡す
- `TimeoutExpired` を捕捉して再送出する際、`output` / `stderr` を `e.stdout or ""` でフォールバックする（`None` 防止）
- `SubprocessError` はそのまま再送出（ラップしない）
- 戻り値は `(stdout, returncode)` のタプル

### `run_command_simple`

- `check=True` を指定するため終了コード非ゼロで `CalledProcessError` を送出する
- 例外時は `logging.exception` でトレースを記録してから再送出する

### `run_command_simple_with_count`

- `get_next_count(appstore)` で実行回数を採番し、`count == 1 or force` のときだけコマンドを実行する
- `verbose=True` 時は `appstore.show(AppConfig.KIND_DB, AppConfig.BASE_NAME_FETCH)` でデバッグ表示する
- 実行しなかった場合は空文字列を返す

### `get_next_count`

- `appstore.get_file_assoc_from_db(AppConfig.BASE_NAME_FETCH)` で取得回数履歴辞書を取得する
- 辞書が空 / None なら `next_count = 1` にし、`{"1": 現在時刻}` を初期化する
- 辞書があれば整数変換可能なキーの最大値 + 1 を `next_count` にする（`ValueError` は `continue` でスキップ）
- 更新した辞書を `appstore.output_db` で書き戻す

## 依存関係

- `subprocess`, `logging`（標準ライブラリ）
- `yklibpy.common.timex.Timex`
- `yklibpy.config.appconfig.AppConfig`
- `yklibpy.db.appstore.AppStore`
