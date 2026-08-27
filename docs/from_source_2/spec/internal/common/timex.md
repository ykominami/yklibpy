# Timex — 内部仕様書

**ファイル**: `src/yklibpy/common/timex.py`  
**継承**: なし

## 概要

日本標準時の現在時刻を ISO 8601 文字列として取得する時刻ユーティリティです。

---

## クラス定数

| 定数名 | 値 | 説明 |
|--------|----|------|
| `JST` | `timezone(timedelta(hours=9))` | UTC+9 の固定オフセットタイムゾーンです。 |

---

## メソッド

### `get_now() -> str` (classmethod)

JST の現在時刻をタイムゾーン付き ISO 8601 形式で返します。

**Returns**: `datetime.isoformat()` による時刻文字列です。

## 依存

| クラス/変数 | 用途 |
|-------------|------|
| `datetime`, `timedelta`, `timezone` | JST 定義と現在時刻取得に使用します。 |
