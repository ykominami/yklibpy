# AnchorTagx — 内部仕様書

## モジュール

`yklibpy.htmlparser.misc.anchortagx`

## 継承

`Tagx` を継承する。

## インスタンス変数（追加分）

| 変数名 | 型 | 役割 |
|--------|----|------|
| `href` | `str` | アンカーの `href` 属性値（取得失敗時は `""`） |
| `text` | `str` | `get_text(strip=True)` で取得したリンクテキスト（取得失敗時は `""`） |
| `mes_href` | `str` | `"  href: {href}"` の表示文字列 |
| `mes_text` | `str` | `"  text: {text}"` の表示文字列 |

## `__init__` の処理フロー

1. `super().__init__(anchor_tag, "anchor")` で `Tagx` を初期化
2. `self.tag is not None` のとき：
   - `hasattr(self.tag, "get")` → `self.href = self.tag.get("href", "")`
   - `hasattr(self.tag, "get_text")` → `self.text = self.tag.get_text(strip=True)`
   - `mes_href` / `mes_text` を構築

## `show` の実装詳細

```python
"\n".join([self.mes_href, self.mes_text])
```

`tag is None` の場合 `mes_href` / `mes_text` が未設定のため `AttributeError` になる点に注意。

## 依存関係

- `bs4.element.PageElement`
- `yklibpy.htmlparser.misc.tagx.Tagx`
