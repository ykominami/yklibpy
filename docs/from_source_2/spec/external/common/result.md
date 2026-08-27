# 外部仕様書 — `Util.Result`

**対象クラス**: `Util.Result`

## 未確定事項（本書作成にあたっての前提）

- 正規の定義2 文書が欠落し、代替候補も空です。URL 判定理由は現行実装の文字列です。異なる意図であればお知らせください。

## 1. 概要

URL 検証結果として `success`、入力 `url`、`reason`、解析済み `parsed` を保持します。

## 2. 値仕様

理由は `URL is empty`、`URL scheme is invalid`、`URL is not a valid URI: missing authority, path, or fragment`、`URL is valid` のいずれかです。

## 3. エラー処理・終了コード

値コンテナ自体は例外処理を行いません。ライブラリのため終了コードはなく、未捕捉例外の CLI 終了コードは `1` です。

## 4. 実装上の対応（参考）

本節は実装を拘束しません。`src/yklibpy/common/util.py` 内の入れ子クラスです。
