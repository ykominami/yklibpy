# Progress — 外部仕様書

## 概要

`yklibpy.htmlparser.progress.Progress`

ARIA の進捗バー属性に対応した値をまとめて保持するデータ容器。
HTML から読み取った進捗メーター情報を構造化して持ち運ぶ用途を想定する。

## コンストラクタ

```python
Progress(
    meter_str: str,
    valuemin: str,
    valuemax: str,
    valuenow: str,
)
```

`meter` フィールドは `"{valuemin}-{valuemax}-{valuenow}"` の形式で自動生成される。

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `meter_str` | `str` | 進捗バーの表示文字列 |
| `valuemin` | `str` | 最小値（ARIA `aria-valuemin` に相当） |
| `valuemax` | `str` | 最大値（ARIA `aria-valuemax` に相当） |
| `valuenow` | `str` | 現在値（ARIA `aria-valuenow` に相当） |
| `meter` | `str` | `"{valuemin}-{valuemax}-{valuenow}"` 形式の比較用文字列 |

## パブリック API

### `to_dict() -> Dict[str, str]`

保持している進捗情報を辞書へ変換して返す。

## 依存関係

なし
