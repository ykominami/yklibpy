# AnchorTagInfo — 内部仕様書

**ファイル**: `src/yklibpy/htmlparser/misc/anchortaginfo.py`
**継承**: なし

## 概要

アンカー要素（`<a>`）本体と、その親・親の親・次の兄弟ノードの情報をまとめて保持するコンテナ。`HtmlOp` が抽出したアンカーの周辺コンテキストを扱う際に使う。

---

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `anchor` | `AnchorTagx` | アンカー本体のラッパー。 |
| `parent_parent` | `Tagx \| None` | アンカーの親の親ノード情報。`setup()` 実行後に設定される。 |
| `parent` | `Tagx \| None` | アンカーの次の兄弟ノード情報（変数名は `parent` だが実際は次の兄弟ノードを格納する。詳細は「設計上の注意」を参照）。`setup()` 実行後に設定される。 |
| `next_sibling` | `Tagx \| None` | アンカーの次の兄弟ノード情報。`setup()` 実行後に設定される。 |

---

## メソッド

### `__init__(anchor_tag: Optional[PageElement]) -> None`

アンカー要素から `AnchorTagx` を生成し、関連するタグ情報の入れ物（`None` 初期値）を用意する。

### `setup() -> None`

アンカー要素の親や兄弟ノード情報を構築する。`self.anchor.tag` が存在すれば `next_sibling`/`parent` を `Tagx` として構築し、`parent_parent` は `self.anchor.tag.parent` が存在する場合のみ `Tagx` として構築する（`self.anchor.tag.parent` が `None` の場合は `None` のまま）。`self.anchor.tag` が存在しなければすべて `None` のままにする。

---

## 依存

| クラス/変数 | 用途 |
|-------------|------|
| `AnchorTagx` | アンカー本体の保持 |
| `Tagx` | 周辺ノードのラップ |

---

## 設計上の注意

`parent` の構築に `self.anchor.tag.next_sibling` を使っており（`self.anchor.tag.parent` ではない）、変数名 `parent` と実際に格納される内容（次の兄弟ノード）が一致していない。バグの可能性がある実装のため、`parent` を利用する際は実際の値を確認すること。
