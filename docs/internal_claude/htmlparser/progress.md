# Progress — 内部仕様書

## モジュール

`yklibpy.htmlparser.progress`

## インスタンス変数

| 変数名 | 型 | 役割 |
|--------|----|------|
| `meter_str` | `str` | プログレスバー要素の文字列表現 |
| `valuemin` | `str` | ARIA `aria-valuemin` 属性値 |
| `valuemax` | `str` | ARIA `aria-valuemax` 属性値 |
| `valuenow` | `str` | ARIA `aria-valuenow` 属性値 |
| `meter` | `str` | `"{valuemin}-{valuemax}-{valuenow}"` の複合文字列（比較・重複検出用） |

## `to_dict` の実装詳細

```python
{
    "meter_str": self.meter_str,
    "valuemin":  self.valuemin,
    "valuemax":  self.valuemax,
    "valuenow":  self.valuenow,
    "meter":     self.meter,
}
```

単純な辞書変換で、フィールドのコピーのみを行う。

## 依存関係

- なし
