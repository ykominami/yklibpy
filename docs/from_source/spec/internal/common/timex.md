# Timex — 内部仕様書

**ファイル**: `src/yklibpy/common/timex.py`
**継承**: なし

## 概要

JST（日本標準時）基準の現在時刻を ISO 8601 文字列で返す、状態を持たないユーティリティクラス。

---

## クラス定数

| 定数名 | 値 | 説明 |
|--------|----|------|
| `JST` | `timezone(timedelta(hours=9))` | 日本標準時のタイムゾーンオブジェクト。 |

---

## メソッド

### `get_now() -> str` (classmethod)

現在時刻を JST の ISO 8601 文字列で返す。

---

## 依存

なし（標準の `datetime` のみ）。

---

## 設計上の注意

特になし。`FetchCount` および `Command.get_next_count` の取得履歴タイムスタンプ生成に使われる。
