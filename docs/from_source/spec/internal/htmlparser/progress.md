# Progress — 内部仕様書

**ファイル**: `src/yklibpy/htmlparser/progress.py`
**継承**: なし

## 概要

HTML の ARIA 進捗属性（`aria-valuemin`/`aria-valuemax`/`aria-valuenow` 等）由来の値をまとめて保持し、辞書へ変換するデータコンテナ。

---

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `meter_str` | `str` | 進捗メーターの元文字列。 |
| `valuemin` | `str` | 最小値。 |
| `valuemax` | `str` | 最大値。 |
| `valuenow` | `str` | 現在値。 |
| `meter` | `str` | `"{valuemin}-{valuemax}-{valuenow}"` 形式の比較用文字列。 |

---

## メソッド

### `__init__(meter_str: str, valuemin: str, valuemax: str, valuenow: str) -> None`

ARIA 由来の進捗属性を保持し、比較用の `meter` 文字列を組み立てる。

### `to_dict() -> Dict[str, str]`

保持している進捗情報を辞書へ変換する（`meter_str`/`valuemin`/`valuemax`/`valuenow`/`meter` の 5 キー）。

---

## 依存

なし（標準の `typing` のみ）。

---

## 設計上の注意

単純なデータコンテナ。ただし `src/` 内に `Progress(...)` を生成している箇所は本ファイル以外に存在せず、現状はどこからも呼び出されていない（未使用気味の実装）。
