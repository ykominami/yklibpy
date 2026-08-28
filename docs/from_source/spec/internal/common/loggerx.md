# Loggerx — 内部仕様書

**ファイル**: `src/yklibpy/common/loggerx.py`
**継承**: なし

## 概要

標準 `logging` モジュールへの薄いラッパー。名前ごとのロガーをキャッシュし、共通のログレベル管理と `debug`/`info`/`warning`/`error`/`critical` の各メソッドを提供する。プロジェクト全体で `logging` を直接呼ばず、本クラス経由でログ出力する規約になっている。

---

## クラス変数

| 変数名 | 値 | 説明 |
|--------|----|------|
| `_loggers` | `ClassVar[dict[str, logging.Logger]]`（既定 `{}`） | 名前をキーにしたロガーのキャッシュ。 |
| `_log_level` | `ClassVar[int]`（既定 `logging.INFO`） | 既定のログレベル。 |

---

## メソッド

### `set_log_level(log_level: int = logging.INFO) -> None` (classmethod)

既定のログレベルを更新し、`logging.basicConfig` へ反映する。

### `_get_or_create(name: str, log_level: int = logging.INFO) -> logging.Logger` (classmethod)

名前に対応するロガーを取得し、未生成なら作成してキャッシュする。取得のたびにロガーの閾値を、クラス変数 `_log_level`（`set_log_level()` でのみ変更される、全呼び出し共通の既定値）で再設定する。引数の `log_level`（`debug`/`info`/`warning`/`error`/`critical` それぞれが `logging.DEBUG`/`logging.INFO`/... と異なる値を渡す）は本文で未使用であり、無視される。そのため `debug()` 等を呼んでも、ロガーの実効レベルは呼び出したメソッドの種類に関わらず常に共有の `_log_level`（既定 `logging.INFO`）になる。

### `debug(message: str, name: str | None = None) -> None` / `info(...)` / `warning(...)` / `error(...)` / `critical(...)` (classmethod)

各ログレベルでメッセージを記録する。`name` 省略時は `"yklibpy"` を使う。

---

## 依存

なし（標準の `logging` のみ）。

---

## 設計上の注意

- `_get_or_create()` の引数 `log_level` は本文で未使用であり、呼び出し元（`debug`/`info`/`warning`/`error`/`critical`）がそれぞれ異なる値を渡しても効果が無い（意図された「呼び出しごとのレベル設定」が機能していない可能性がある）。ロガーの実効レベルは常にクラス変数 `_log_level` に従う。
- `_loggers` と `_log_level` はクラス変数であり、アプリ全体で共有されるグローバル状態になる。テストで独立したログレベルを検証する場合は影響し合う点に注意。
- `error`/`critical` にはコメントアウトされた `_verbose` 参照が残っており、未整理のコードが残っている。
