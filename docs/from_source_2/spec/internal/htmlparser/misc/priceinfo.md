# PriceInfo — 内部仕様書

**ファイル**: `src/yklibpy/htmlparser/misc/priceinfo.py`  
**継承**: なし

## 概要

旧価格と現在価格に対応する `Tagx` を対で保持し、設定済みの補助文字列を安全に取り出す。

---

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `price_old` | `Tagx | None` | 旧価格のタグ情報。 |
| `price_real` | `Tagx | None` | 現在価格のタグ情報。 |

---

## メソッド

### `__init__(price_old: Tagx | None, price_real: Tagx | None) -> None`

旧価格と現在価格のタグ情報を保持する。

### `get_price_old() -> str | None`

旧価格があれば `Tagx.get_option()` の結果を返し、なければ `None` を返す。

### `get_price_real() -> str | None`

現在価格があれば `Tagx.get_option()` の結果を返し、なければ `None` を返す。

## 依存

| クラス/変数 | 用途 |
|-------------|------|
| `Tagx` | 価格タグと整形済み補助文字列の保持。 |

## 設計上の注意

価格の解析や数値変換は行わず、`Tagx.option` に外部から設定された文字列をそのまま返す。
