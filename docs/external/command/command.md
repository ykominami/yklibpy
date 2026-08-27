# Command — 外部仕様書

## 概要

`yklibpy.command.command.Command`

外部コマンドの実行と実行回数管理を提供するクラス。
`subprocess.run` を直接使う代わりに本クラスを経由することで、タイムアウト処理・エンコーディング指定・回数履歴管理が一貫して扱える。

## コンストラクタ

```python
Command()
```

互換性維持のための空初期化。状態を持たない。

## パブリック API

### `run_command(command, shell=False, encoding="utf-8", timeout=None) -> tuple[str, int]`

コマンドを実行し、標準出力文字列と終了コードのタプルを返す。

**Raises**:
- `subprocess.TimeoutExpired` — `timeout` 秒以内に完了しない場合。
- `subprocess.SubprocessError` — その他のサブプロセスエラー。

### `run_command_simple(command, shell=False) -> str`

終了コードを検査しながらコマンドを実行し、標準出力を返す。
コマンドが非ゼロの終了コードで完了した場合は `CalledProcessError` が送出される。

**Raises**: `subprocess.CalledProcessError` — 終了コードが非ゼロの場合。

### `run_command_simple_with_count(appstore, command, shell=False, *, force=False, verbose=False) -> str`

取得回数を確認し、**初回または `force=True`** のときのみコマンドを実行して出力を返す。
それ以外は空文字を返す。`verbose=True` の場合は `appstore.show` でデバッグ出力する。

### `get_next_count(appstore: AppStore) -> int`

`appstore` が管理する `fetch` DB から次の連番を採番して記録し、連番を返す。
DB が空の場合は `1` から開始する。

## 依存関係

- `subprocess`（標準ライブラリ）
- `logging`（標準ライブラリ）
- `yklibpy.common.timex.Timex`
- `yklibpy.config.appconfig.AppConfig`
- `yklibpy.db.appstore.AppStore`
