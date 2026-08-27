# Loggerx — 外部仕様書

## 概要

`yklibpy.common.loggerx.Loggerx`

ロガーの生成とログレベル管理を一か所に集約するクラスメソッド集。
`logging.getLogger` を直接使う代わりに本クラスを経由することで、ライブラリ全体のログレベルを一括制御できる。

## 責務

- モジュール名を `name` として受け取り、対応する `logging.Logger` を生成・キャッシュする。
- `set_log_level` で全体のデフォルトレベルを変更し、既存ロガーに即時反映する。
- `debug` / `info` / `warning` / `error` / `critical` の 5 段階でメッセージを記録する。

## クラス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `_loggers` | `dict[str, logging.Logger]` | 生成済みロガーのキャッシュ（名前をキーとする） |
| `_log_level` | `int` | 現在のデフォルトログレベル。初期値は `logging.INFO` |

## パブリック API

### `set_log_level(log_level: int = logging.INFO) -> None`

デフォルトログレベルを変更し、`logging.basicConfig` へ即時反映する。
デバッグ出力を有効にするには `logging.DEBUG` を渡す。

### `debug(message: str, name: str | None = None) -> None`

DEBUG レベルでメッセージを記録する。`name` を省略すると `"yklibpy"` を使う。

### `info(message: str, name: str | None = None) -> None`

INFO レベルでメッセージを記録する。

### `warning(message: str, name: str | None = None) -> None`

WARNING レベルでメッセージを記録する。

### `error(message: str, name: str | None = None) -> None`

ERROR レベルでメッセージを記録する。

### `critical(message: str, name: str | None = None) -> None`

CRITICAL レベルでメッセージを記録する。

## 使用規約

- `name` には `__name__` を渡す（モジュール名でロガーを区別できる）。
- デフォルトは INFO のため、DEBUG ログは `set_log_level(logging.DEBUG)` を呼ばないと出力されない。

## 依存関係

- `logging`（標準ライブラリ）
