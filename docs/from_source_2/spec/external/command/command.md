# 外部仕様書 — `Command`

**対象**: 外部コマンド実行 API

## 未確定事項

正とされる2 定義文書は欠落し、代替候補も空です。履歴ファイルの正式な配置・形式は未確定です。異なる意図であればお知らせください。

## 1. 概要

外部プロセスの標準出力と終了コードを取得し、必要に応じて取得履歴を採番します。

## 2. 利用仕様

`run_command(command, shell=False, encoding="utf-8", timeout=None)` は標準出力と終了コードを返し、非 `0`終了も例外にしません。不正バイトは `U+FFFD` に置換します。`run_command_simple` は非 `0`終了を失敗とします。

`run_command_simple_with_count(appstore, command, shell=False, force=False, verbose=False)` は `get_next_count(appstore)` で履歴を採番し、採番が `1`または `force=True` のときだけコマンドを実行します。`verbose=True` の場合はコマンドを標準出力へ表示します。`get_next_count(appstore)` は `FetchCount` が選択した回数を返し、更新が必要な場合はコマンド実行前に `fetch` DB を更新します。このため、後続のコマンド実行が失敗しても履歴は残り得ます。

## 3. 作成・更新ファイル

現行実装は `AppStore` の `fetch` DB に文字列の連番キーと `Timex.get_now()` の値を保存します。正式なパス、時刻形式は定義文書欠落のため未確定です。実行失敗前にも履歴は更新され得ます。

## 4. エラー処理・終了コード

| 事象 | 挙動 | 終了コード |
|---|---|---:|
| `run_command` の子プロセス非 `0` | `(stdout, returncode)` を返す | 子の終了コード |
| タイムアウト | `TimeoutExpired` を再送出 | 最上位で未捕捉なら `1` |
| `run_command_simple` の非 `0` | ログ後 `CalledProcessError` | 最上位で未捕捉なら `1` |
| 正常 | 標準出力を返す | 呼び出し API 自体は終了しない |

## 5. 実装上の対応（参考）

本節は実装を拘束しません。`src/yklibpy/command/command.py` の `Command` が担当します。
