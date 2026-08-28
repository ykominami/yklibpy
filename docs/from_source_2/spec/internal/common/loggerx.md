# Loggerx — 内部仕様書

**ファイル**: `src/yklibpy/common/loggerx.py`  
**継承**: なし

## 概要

名前別の標準 `logging.Logger` をキャッシュし、共通ログレベルでログ出力するクラスです。

---

## クラス定数

| 定数名 | 値 | 説明 |
|--------|----|------|
| `_loggers` | `dict[str, logging.Logger]` | 生成済みロガーの名前別キャッシュです。 |
| `_log_level` | `logging.INFO` | 全ロガーへ適用する現在のログレベルです。 |

---

## メソッド

### `set_log_level(log_level: int = logging.INFO) -> None` (classmethod)

共通ログレベルを更新し、`logging.basicConfig` にも設定します。

### `_get_or_create(name: str, log_level: int = logging.INFO) -> logging.Logger` (classmethod)

名前別ロガーを取得または生成し、共通ログレベルを設定して返します。

### `debug(message: str, name: str | None = None) -> None` (classmethod)

指定名、または既定名 `yklibpy` のロガーへデバッグログを出力します。

### `info(message: str, name: str | None = None) -> None` (classmethod)

情報ログを出力します。

### `warning(message: str, name: str | None = None) -> None` (classmethod)

警告ログを出力します。

### `error(message: str, name: str | None = None) -> None` (classmethod)

エラーログを出力します。

### `critical(message: str, name: str | None = None) -> None` (classmethod)

致命的エラーログを出力します。

---

## 依存

| クラス/変数 | 用途 |
|-------------|------|
| `logging` | ロガー生成、レベル設定、ログ記録を担当します。 |

## 設計上の注意

`_get_or_create` の `log_level` 引数は使用されず、各出力メソッドが渡すレベルにかかわらず `_log_level` が設定されます。
