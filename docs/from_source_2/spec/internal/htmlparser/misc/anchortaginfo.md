# AnchorTagInfo — 内部仕様書

**ファイル**: `src/yklibpy/htmlparser/misc/anchortaginfo.py`  
**継承**: なし

## 概要

アンカー要素本体を `AnchorTagx` として保持し、周辺の親・祖先・次兄弟ノードを `Tagx` に変換してまとめる。

---

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `anchor` | `AnchorTagx` | 対象アンカー要素の情報。 |
| `parent_parent` | `Optional[Tagx]` | アンカーの祖先ノード情報。 |
| `parent` | `Optional[Tagx]` | 親として扱うノード情報。 |
| `next_sibling` | `Optional[Tagx]` | 次の兄弟ノード情報。 |

---

## メソッド

### `__init__(anchor_tag: Optional[PageElement]) -> None`

アンカー情報を生成し、周辺ノード情報を未設定状態で初期化する。

### `setup() -> None`

アンカー要素の有無に応じて周辺ノード情報を構築またはクリアする。

処理フロー:

1. アンカー要素が存在するか確認する。
2. 次兄弟、親として扱うノード、祖先ノードを `Tagx` へ変換する。
3. アンカーがない場合は周辺情報をすべて `None` にする。

## 依存

| クラス/変数 | 用途 |
|-------------|------|
| `AnchorTagx` | アンカー要素の href とテキストを保持する。 |
| `Tagx` | 周辺ノードの表示情報を保持する。 |

## 設計上の注意

`setup` は `parent` に `anchor.tag.parent` ではなく `anchor.tag.next_sibling` を渡しており、変数名と実値が一致しない可能性がある。初期化だけでは周辺情報は構築されず、利用側が明示的に `setup` を呼ぶ必要がある。
