# 外部仕様書 — `Progress`

**対象クラス**: `yklibpy.htmlparser.Progress`

## 未確定事項（本書作成にあたっての前提）

進捗値の定義文書が欠落しているため、文字列として扱う現行実装を記載します。異なる意図であればお知らせください。

## 1. 出力形式

`to_dict()` は `meter_str`、`valuemin`、`valuemax`、`valuenow` と、`<valuemin>-<valuemax>-<valuenow>` 形式の `meter` を返します。数値変換、値域、大小関係は検証しません。

## 2. エラー処理・終了コード

独自例外と終了コードはありません。未捕捉例外でプロセスが終了する場合は `1` です。

## 3. 実装上の対応（参考）

本節は実装を拘束しません。`src/yklibpy/htmlparser/progress.py` に対応します。
