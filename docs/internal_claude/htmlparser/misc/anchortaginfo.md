# AnchorTagInfo — 内部仕様書

## モジュール

`yklibpy.htmlparser.misc.anchortaginfo`

## インスタンス変数

| 変数名 | 型 | 役割 |
|--------|----|------|
| `anchor` | `AnchorTagx` | アンカー要素の href とテキストを保持 |
| `parent_parent` | `Tagx \| None` | 祖父要素（`setup` 実行後に設定） |
| `parent` | `Tagx \| None` | 親要素相当（`setup` 実行後に設定、実装上は `next_sibling` と同値） |
| `next_sibling` | `Tagx \| None` | 次の兄弟要素（`setup` 実行後に設定） |

## `setup` の実装詳細

```python
self.next_sibling  = Tagx(self.anchor.tag.next_sibling, "next_sibling")
self.parent        = Tagx(self.anchor.tag.next_sibling, "parent")  # ← バグ: next_sibling と同値
self.parent_parent = Tagx(self.anchor.tag.parent.parent, "parent.parent")
```

- `self.anchor.tag` が `None` の場合、全フィールドに `None` をセット
- `parent` は `self.anchor.tag.parent` を渡すべきところ `next_sibling` を渡しているバグがある

## `HtmlOp.get_anchor_tag_info` との関係

`HtmlOp.get_anchor_tag_info` は `AnchorTagInfo(anchor_tag)` を生成するが `setup()` を呼ばないため、呼び出し元が必要に応じて `setup()` を呼ぶ必要がある。

## 依存関係

- `bs4.element.PageElement`
- `yklibpy.htmlparser.misc.anchortagx.AnchorTagx`
- `yklibpy.htmlparser.misc.tagx.Tagx`
