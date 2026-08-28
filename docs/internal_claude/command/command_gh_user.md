# CommandGhUser — 内部仕様書

## モジュール

`yklibpy.command.command_gh_user`

## 継承

`Command` を継承する。

## クラス定数

| 定数名 | 値 | 役割 |
|--------|----|------|
| `DEFAULT_VALUE_USER` | `None` | 取得失敗時のフォールバック値（現在は `run` 内で使われていない） |

## `run` の実装詳細

1. `command_line = 'gh api user --jq ".login"'` を文字列として組み立てる（`shell=True` 前提の文字列）
2. `self.run_command_simple(command_line)` を呼ぶ（`shell=False` がデフォルトなので、文字列渡しでも `shell=False` で実行される点に注意。実際は `shell=True` にしないと正しく動かない可能性がある）
3. `Util.normalize_string(output)` で空白・改行を除去し、空ならさらに `None` に変換
4. `user or ""` で `None` を空文字へ変換して返す

## 依存関係

- `yklibpy.command.command.Command`
- `yklibpy.common.util.Util`
