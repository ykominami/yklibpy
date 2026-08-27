# 外部仕様書 — `util_json`

**対象クラス**: `yklibpy.common.util_json.UtilJson`
**対応サブコマンド**: なし（ライブラリクラス）

本書は `docs/projects/def_ot_terms.md`（用語の定義）および `docs/projects/def_of_file_and_dir.md`（ディレクトリ/ファイル定義）を正とする方針で作成したが、本書作成時点で両ファイルは空である。そのため本書の記述はすべて「現行実装の挙動」に基づく。

## 未確定事項（本書作成にあたっての前提）

- 定義ドキュメント 2 件がいずれも空のため、定義由来の記述は存在せず、全記述を「現行実装の挙動」として扱った。異なる意図であればお知らせください。

## 1. 概要

JSON の読み込み処理（ファイル/文字列）をまとめた補助クラス。状態を持たず、すべて classmethod として提供する。書き込み側の処理は持たない（読み込み専用）。

## 2. 公開インタフェース

### `load_file(file_name: str) -> Any`（classmethod）

JSON ファイルを UTF-8 で読み込み、パース結果を返す。

### `load_string(string: str) -> Any`（classmethod）

JSON 文字列をパースして Python オブジェクトへ変換する。

## 3. エラー処理・終了コード

| 事象 | 挙動 |
|------|------|
| 指定ファイルが存在しない | `FileNotFoundError` が呼び出し元へ伝播する |
| JSON として不正な内容 | `json.JSONDecodeError` が呼び出し元へ伝播する |

ライブラリクラスであり単体のコマンドとして起動される経路は無いため、終了コードは規定しない。

## 4. 実装上の対応（参考）

本節は実装を拘束しない。

| 役割 | モジュール |
|------|-----------|
| JSON 読み込み | `yklibpy.common.util_json.UtilJson` |
| 書き込みが必要な場合の代替 | `yklibpy.db.storex.Storex`/`yklibpy.tomlop.fileitem.FileItem` |
