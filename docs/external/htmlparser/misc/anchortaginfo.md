# AnchorTagInfo — 外部仕様書

## 概要

`yklibpy.htmlparser.misc.anchortaginfo.AnchorTagInfo`

アンカー要素と周辺ノード（親・兄弟）の情報をまとめて保持するデータ容器。
`HtmlOp.get_anchor_tag_info` が生成し、スクレイパーの解析処理に渡される。

## コンストラクタ

```python
AnchorTagInfo(anchor_tag: Optional[PageElement])
```

`AnchorTagx` を生成して `anchor` フィールドに保持する。
周辺ノードは `None` で初期化され、`setup()` を呼び出して構築する。

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `anchor` | `AnchorTagx` | アンカー要素のラッパー |
| `parent_parent` | `Tagx \| None` | アンカーの祖父要素 |
| `parent` | `Tagx \| None` | アンカーの親要素（実装上は `next_sibling` の値が入る） |
| `next_sibling` | `Tagx \| None` | アンカーの次の兄弟ノード |

## パブリック API

### `setup() -> None`

`anchor.tag` を起点に `next_sibling` / `parent` / `parent_parent` を構築する。
`anchor.tag` が `None` の場合はすべて `None` のまま。

**注意**: 現行実装では `parent` フィールドに `next_sibling` のノードが設定されている。

## 依存関係

- `yklibpy.htmlparser.misc.anchortagx.AnchorTagx`
- `yklibpy.htmlparser.misc.tagx.Tagx`
- `bs4.element.PageElement`
