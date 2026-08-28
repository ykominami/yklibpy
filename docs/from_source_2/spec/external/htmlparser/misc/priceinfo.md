# 外部仕様書 — `PriceInfo`

**対象クラス**: `yklibpy.htmlparser.misc.PriceInfo`

## 未確定事項（本書作成にあたっての前提）

価格形式・通貨の定義2 文書が欠落しています。本クラスは文字列コンテナとして扱います。異なる意図であればお知らせください。

## 1. 利用仕様

`get_price_old()` と `get_price_real()` は対象 `Tagx` がなければ `None`、あれば `get_option()` の文字列を返します。価格解析、通貨判定、妥当性検証は行いません。

## 2. エラー処理・終了コード

`None` は正常値です。非互換オブジェクトによる `AttributeError` は伝播し、未捕捉なら終了コードは `1` です。

## 3. 実装上の対応（参考）

本節は実装を拘束しません。`src/yklibpy/htmlparser/misc/priceinfo.py` に対応します。
