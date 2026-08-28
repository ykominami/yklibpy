# Loggerx — 内部仕様書

## モジュール

`yklibpy.common.loggerx`

## クラス変数の実装詳細

| 変数名 | 型 | 初期値 | 役割 |
|--------|----|--------|------|
| `_loggers` | `dict[str, logging.Logger]` | `{}` | 名前をキーとするロガーのキャッシュ。同一名で何度呼んでも新規生成しない |
| `_log_level` | `int` | `logging.INFO` | クラス全体で共有するデフォルトレベル |

## プライベートメソッド

### `_get_or_create(name: str, log_level: int) -> logging.Logger`

- `_loggers` を参照し、`name` が未登録なら `logging.getLogger(name)` で生成してキャッシュ登録する
- 生成済みでも毎回 `setLevel(cls._log_level)` を呼ぶ（`set_log_level` による変更を即時反映するため）
- `log_level` 引数は現時点では `setLevel` に使われず `cls._log_level` が優先される（引数は将来の拡張のみ）

## パブリックメソッドの実装メモ

- `debug` / `info` / `warning` / `error` / `critical` はすべて `_get_or_create(name or "yklibpy", <level>)` を呼び、取得したロガーの対応メソッドを実行する
- `name` が `None` の場合は固定文字列 `"yklibpy"` を使う（ライブラリ全体のルートロガー）
- `error` と `critical` にはコメントアウトされた `if cls._verbose:` の痕跡がある（`_verbose` は現実装に存在しない）

## `set_log_level` の副作用

`logging.basicConfig(level=cls._log_level)` を呼ぶため、ルートロガーのハンドラが未設定のときに限りコンソールハンドラが追加される。既にハンドラが設定済みの場合 `basicConfig` は何もしない（Python 標準の仕様）。

## 依存関係

- `logging`（標準ライブラリ）

## 制約・注意事項

- すべてのメソッドがクラスメソッドのため、インスタンス化して使う用途は想定していない
- スレッドセーフではない（`_loggers` 辞書への同時書き込みは未保護）
