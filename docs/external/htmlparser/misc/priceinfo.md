# PriceInfo — 外部仕様書

## 概要

`yklibpy.htmlparser.misc.priceinfo.PriceInfo`

旧価格と現在価格の表示文字列を `Tagx` の `option` フィールドを通じてまとめて保持するデータ容器。
ECサイトスクレイパーが価格情報を持ち運ぶ際に使用する。

## コンストラクタ

```python
PriceInfo(
    price_old: Tagx | None,
    price_real: Tagx | None,
)
```

価格情報が存在しない場合は `None` を渡す。

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `price_old` | `Tagx \| None` | 旧価格を保持する `Tagx`。`option` に価格文字列が格納される |
| `price_real` | `Tagx \| None` | 現在価格を保持する `Tagx`。`option` に価格文字列が格納される |

## パブリック API

### `get_price_old() -> str | None`

旧価格文字列を返す。`price_old` が `None` の場合は `None` を返す。

### `get_price_real() -> str | None`

現在価格文字列を返す。`price_real` が `None` の場合は `None` を返す。

## 依存関係

- `yklibpy.htmlparser.misc.tagx.Tagx`
