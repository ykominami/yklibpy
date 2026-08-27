# Command — 内部仕様書

**ファイル**: `src/yklibpy/command/command.py`  
**継承**: なし

## 概要

外部プロセスの実行を抽象化し、永続化された取得履歴に基づく実行回数制御を提供する。

---

## メソッド

### `__init__() -> None`

互換性のため何も初期化しない。

### `run_command(command, shell=False, encoding="utf-8", timeout=None) -> tuple[str, int]`

外部コマンドを実行し、標準出力と終了コードを返す。

1. 出力を捕捉し、不正バイトを置換する設定で `subprocess.run` を呼ぶ。
2. 正常終了時は標準出力と終了コードを返す。
3. タイムアウト時は出力を空文字へ正規化した `TimeoutExpired` を再構築して送出し、その他の `SubprocessError` は再送出する。

**Args**: `command` は文字列または引数列、`timeout` は秒数。  
**Returns**: 標準出力と終了コード。  
**Raises**: `subprocess.TimeoutExpired` — 制限時間を超えた場合。  
**Raises**: `subprocess.SubprocessError` — サブプロセス処理に失敗した場合。

### `run_command_simple(command, shell=False) -> str`

終了コード0を必須としてコマンドを実行し、UTF-8標準出力を返す。失敗時は例外ログを記録して `CalledProcessError` を再送出する。

### `run_command_simple_with_count(appstore, command, shell=False, *, force=False, verbose=False) -> str`

履歴を採番し、初回または強制指定時だけコマンドを実行する。

1. `get_next_count()` で履歴を更新する。
2. 初回または `force` 指定時だけコマンドを実行し、それ以外は空文字とする。
3. `verbose` 指定時は取得 DB をログ表示して結果を返す。

### `get_next_count(appstore: AppStore) -> int`

保存済み履歴の数値キー最大値から次の連番を求め、現在時刻とともに DB へ記録する。数値でないキーは無視する。

---

## 依存

| クラス/変数 | 用途 |
|-------------|------|
| `subprocess` | 外部プロセス実行。 |
| `AppStore` | 取得履歴の読み書き。 |
| `AppConfig` | DB 種別と取得履歴名。 |
| `Timex` | 採番時刻の生成。 |

## 設計上の注意

`run_command_simple` は終了コードを検査するが、`run_command` は呼び出し側へ終了コードを委ねる。履歴はコマンド実行前に必ず更新されるため、実行失敗でも採番だけが残り得る。
