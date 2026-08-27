# 外部仕様書 — `HtmlOp`

**対象クラス**: `yklibpy.htmlparser.HtmlOp`

## 未確定事項（本書作成にあたっての前提）

定義2 文書が欠落しているため、DOM 条件とログ形式は現行実装を根拠とします。異なる意図であればお知らせください。

## 1. 概要・API

BeautifulSoup 互換要素を探索します。`get_anchor_under_b(child, cond)` は `b` ごとのアンカー情報を二次元リストで返し、`get_anchor_all(child)` は全 `a` を `AnchorTagInfo` に変換します。`get_anchor_tag_info(None)` は `None` です。`get_anchor_under_div` は `div` 配下をログ出力し、`print_tag_info` は辞書の `tag` と `mes_array` をログへ出します。

## 2. 既知の不整合

`get_anchor_under_div` は `cond` 指定時に条件を使いません。また生成する `AnchorTagInfo` は辞書でないため、そのまま `print_tag_info` に渡すと失敗します。

## 3. エラー処理・終了コード

DOM 非互換時は `AttributeError`、ログ入力の形式不一致は `TypeError` / `KeyError` が伝播します。CLI 終了コードは定義せず、未捕捉なら `1` です。

## 4. 実装上の対応（参考）

本節は実装を拘束しません。`src/yklibpy/htmlparser/htmlop.py` に対応します。
