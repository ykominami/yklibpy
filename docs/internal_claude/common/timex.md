# Timex — 内部仕様書

## モジュール

`yklibpy.common.timex`

## クラス変数

| 変数名 | 型 | 値 | 役割 |
|--------|----|----|------|
| `JST` | `timezone` | `timezone(timedelta(hours=9))` | UTC+9 固定のタイムゾーン |

## `get_now` の実装詳細

```python
datetime.now(cls.JST).isoformat()
```

- `datetime.now(tz)` で JST 基準の現在時刻を取得
- `.isoformat()` は `2025-06-04T12:34:56.789012+09:00` 形式の文字列を返す
- マイクロ秒を含む完全形式（切り捨てなし）

## 依存関係

- `datetime.datetime`, `datetime.timedelta`, `datetime.timezone`（標準ライブラリ）
