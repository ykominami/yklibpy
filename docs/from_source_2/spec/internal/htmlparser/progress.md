# Progress — 内部仕様書

**ファイル**: `src/yklibpy/htmlparser/progress.py`  
**継承**: なし

## 概要

ARIA 等から取得した進捗表示値を保持し、比較・シリアライズ用の辞書表現を提供する値オブジェクトである。

---

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `meter_str` | `str` | 元の進捗表示文字列。 |
| `valuemin` | `str` | 最小値。 |
| `valuemax` | `str` | 最大値。 |
| `valuenow` | `str` | 現在値。 |
| `meter` | `str` | 最小値・最大値・現在値をハイフン連結した比較文字列。 |

---

## メソッド

### `__init__(meter_str: str, valuemin: str, valuemax: str, valuenow: str) -> None`

各値を保持し、`meter` を `valuemin-valuemax-valuenow` 形式で生成する。

### `to_dict() -> Dict[str, str]`

保持する 5 項目を同名キーの辞書として返す。

## 設計上の注意

進捗値は数値ではなく文字列のまま保持し、範囲や大小関係の妥当性検証は行わない。
