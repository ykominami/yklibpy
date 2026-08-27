# Tagx — 内部仕様書

## モジュール

`yklibpy.htmlparser.misc.tagx`

## インスタンス変数

| 変数名 | 型 | 役割 |
|--------|----|------|
| `option` | `str` | `set_option` / `get_option` で管理する補助文字列 |
| `tag` | `PageElement \| None` | 保持する BeautifulSoup 要素 |
| `strx` | `str` | `str(tag)` の文字列表現 |
| `type` | `type` | `type(tag)` |
| `mes_type` | `str` | `"  type({namex}): {str(type(namex))}"` ※`namex` の型を表示している（バグと思われる） |
| `text` | `str` | `tag.get_text(strip=True)` の結果（`tag` が `None` でなく `get_text` を持つ場合） |
| `mes_text` | `str` | テキスト表示用文字列 |
| `mes_name` | `str` | `tag.name` の表示用文字列 |

## `__init__` の実装詳細

- `tag is not None` かつ `hasattr(tag, "get_text")` のときのみ `text` / `mes_text` を設定
- `hasattr(tag, "name")` のときのみ `mes_name` を設定
- `tag is None` の場合、`text` / `mes_text` / `mes_name` は設定されない（アクセスで `AttributeError`）

## 既知の問題

`mes_type` の生成式 `str(type(namex))` は `namex`（文字列）の型を表示しており、`tag` の型ではない。

## 依存関係

- `bs4.element.PageElement`
