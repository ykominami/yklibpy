# 外部仕様書 — `opresult`

**対象クラス**: `yklibpy.common.opresult.OpResult`
**対応サブコマンド**: なし（ライブラリクラス）

本書は `docs/projects/def_ot_terms.md`（用語の定義）および `docs/projects/def_of_file_and_dir.md`（ディレクトリ/ファイル定義）を正とする方針で作成したが、本書作成時点で両ファイルは空である。そのため本書の記述はすべて「現行実装の挙動」に基づく。

## 未確定事項（本書作成にあたっての前提）

- 定義ドキュメント 2 件がいずれも空のため、定義由来の記述は存在せず、全記述を「現行実装の挙動」として扱った。異なる意図であればお知らせください。

## 1. 概要

操作の成否と、失敗時の例外情報（発生箇所・メッセージ・型）を保持するイミュータブルな結果オブジェクト（`Generic[T]`、frozen dataclass）。保存先管理クラスの取得系メソッドが、例外を送出する代わりに返す戻り値型として使う。

## 2. 公開インタフェース

### フィールド

| フィールド | 型 | 説明 |
|-----------|----|------|
| `ok` | `bool` | 操作が成功したかどうか |
| `value` | `T \| None` | 成功時の値。失敗時は `None` |
| `exc_occurred` | `bool` | 例外が発生したかどうか |
| `exc_location` | `str \| None` | 発生箇所（`ファイル名:行番号 in 関数名` 形式） |
| `exc_message` | `str \| None` | 例外メッセージ |
| `exc_type` | `str \| None` | 例外の型名 |
| `optional_string` | `str \| None` | 呼び出し元が付与する補足文字列（デバッグ用コンテキスト） |

frozen のため生成後にフィールドは変更できない（変更しようとすると `dataclasses.FrozenInstanceError`）。

### `success(value: T) -> OpResult[T]`（classmethod）

成功結果を生成する。例外関連フィールドはすべて `None`/`False`。

### `from_exception(exc: BaseException, optional_string: str) -> OpResult[T]`（classmethod）

例外から失敗結果を生成する。`exc_location` にはトレースバックの最内フレーム（実際に例外が起きた行）を `ファイル名:行番号 in 関数名` 形式で記録する。トレースバックが無い例外の場合は `"unknown"` になる。

## 3. 利用側の規約

呼び出し元は `result.ok` を確認してから `result.value` を使う。`ok` が `False` の場合 `value` は常に `None` であり、例外は再送出されないため、判定漏れに注意する。

## 4. エラー処理・終了コード

本クラス自身が例外を送出する経路は無い。ライブラリクラスであり単体のコマンドとして起動される経路は無いため、終了コードは規定しない。

## 5. 実装上の対応（参考）

本節は実装を拘束しない。

| 役割 | モジュール |
|------|-----------|
| 結果型 | `yklibpy.common.opresult.OpResult` |
| 主な利用元 | `yklibpy.db.appstore.AppStore` の取得系メソッド |
