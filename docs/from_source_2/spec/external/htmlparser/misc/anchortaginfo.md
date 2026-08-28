# 外部仕様書 — `AnchorTagInfo`

**対象クラス**: `yklibpy.htmlparser.misc.AnchorTagInfo`

## 未確定事項（本書作成にあたっての前提）

周辺 DOM の意味を定める定義2 文書が欠落しているため、現行実装を記載します。異なる意図であればお知らせください。

## 1. 利用仕様

アンカーを `AnchorTagx` で保持します。初期化直後の `parent_parent`、`parent`、`next_sibling` は `None` で、`setup()` により周辺ノードを `Tagx` に変換します。

## 2. 既知の不整合

`parent` には親でなく `anchor.tag.next_sibling` が設定され、`next_sibling` と同じ元ノードを異なる表示名でラップします。

## 3. エラー処理・終了コード

アンカー自体が欠落している場合、`parent_parent`、`parent`、`next_sibling` は `None` になります。アンカーが存在する場合、欠落した `next_sibling` または `parent.parent` も `Tagx(None, ...)` としてラップされ、属性自体は `None` になりません。非互換入力の属性例外は伝播し、未捕捉なら終了コードは `1` です。

## 4. 実装上の対応（参考）

本節は実装を拘束しません。`src/yklibpy/htmlparser/misc/anchortaginfo.py` に対応します。
