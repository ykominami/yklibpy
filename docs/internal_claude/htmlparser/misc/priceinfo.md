# PriceInfo — 内部仕様書

## モジュール

`yklibpy.htmlparser.misc.priceinfo`

## インスタンス変数

| 変数名 | 型 | 役割 |
|--------|----|------|
| `price_old` | `Tagx \| None` | 旧価格の `Tagx` オブジェクト |
| `price_real` | `Tagx \| None` | 現在価格の `Tagx` オブジェクト |

## `get_price_old` / `get_price_real` の実装詳細

- 対応する `Tagx` が `None` なら `None` を返す
- それ以外は `Tagx.get_option()` の値を返す
- `Tagx.option` は `set_option` で外部から設定するため、未設定の場合は初期値 `""` が返される

## 依存関係

- `yklibpy.htmlparser.misc.tagx.Tagx`
