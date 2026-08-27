# AnchorTagx — 外部仕様書

## 概要

`yklibpy.htmlparser.misc.anchortagx.AnchorTagx`

`Tagx` を継承し、アンカー要素（`<a>`）の `href` 属性と表示テキストを扱う拡張クラス。

## 継承

```
Tagx
  └── AnchorTagx
```

## コンストラクタ

```python
AnchorTagx(anchor_tag: Optional[PageElement])
```

スーパークラスを `namex="anchor"` で初期化した後、`href` と `text` を抽出する。
`anchor_tag` が `None` または `get` / `get_text` を持たない場合は空文字を設定する。

## インスタンス変数（追加分）

| 変数名 | 型 | 説明 |
|--------|----|------|
| `href` | `str` | アンカーの `href` 属性値（取得できない場合は空文字） |
| `text` | `str` | アンカーのテキスト内容（`get_text(strip=True)`） |
| `mes_href` | `str` | `href` のデバッグ用表示文字列 |
| `mes_text` | `str` | テキストのデバッグ用表示文字列 |

※ `anchor_tag` が `None` の場合、`mes_href` と `mes_text` は初期化されない。

## パブリック API

### `show() -> str`

`mes_href` と `mes_text` を改行区切りで連結した文字列を返す。

## 依存関係

- `yklibpy.htmlparser.misc.tagx.Tagx`
- `bs4.element.PageElement`
