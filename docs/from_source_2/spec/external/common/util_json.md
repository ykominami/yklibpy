# 外部仕様書 — `UtilJson`

**対象クラス**: `UtilJson`

## 未確定事項（本書作成にあたっての前提）

- 正規の定義2 文書が欠落し、代替候補も空です。JSON 配置・スキーマは未定義です。異なる意図であればお知らせください。

## 1. 概要

UTF-8 JSON ファイルまたは JSON 文字列を Python オブジェクトへ変換します。

## 2. 公開仕様

`load_file(file_name)` はファイルを読み、`load_string(string)` は文字列を解析します。スキーマ検証はしません。

## 3. エラー処理・終了コード

`OSError` と `json.JSONDecodeError` を伝播します。ライブラリのため終了コードはなく、CLI 未捕捉時は `1` です。

## 4. 実装上の対応（参考）

本節は実装を拘束しません。`src/yklibpy/common/util_json.py` が処理します。
