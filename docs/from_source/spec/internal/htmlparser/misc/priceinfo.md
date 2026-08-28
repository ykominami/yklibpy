# PriceInfo — 内部仕様書

**ファイル**: `src/yklibpy/htmlparser/misc/priceinfo.py`
**継承**: なし

## 概要

旧価格と現在価格の表示文字列をまとめて保持するコンテナ。各値は `Tagx` 経由で保持し、`get_option()` で取り出す。

---

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `price_old` | `Tagx \| None` | 旧価格に対応する `Tagx`。 |
| `price_real` | `Tagx \| None` | 現在価格に対応する `Tagx`。 |

---

## メソッド

### `__init__(price_old: Tagx | None, price_real: Tagx | None) -> None`

価格表示に対応する `Tagx` を保持する。

### `get_price_old() -> str | None`

保持している旧価格文字列を返す。`price_old` が `None` なら `None`。

### `get_price_real() -> str | None`

保持している現在価格文字列を返す。`price_real` が `None` なら `None`。

---

## 依存

| クラス/変数 | 用途 |
|-------------|------|
| `Tagx` | 価格表示文字列の保持元（`get_option()`） |

---

## 設計上の注意

`get_price_old()`/`get_price_real()` は `Tagx.get_option()` を経由するため、呼び出し前に `Tagx.set_option()` で値を設定しておく必要がある（未設定の場合は空文字が返る）。
