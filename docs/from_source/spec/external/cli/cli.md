# 外部仕様書 — `cli`

**対象クラス**: `yklibpy.cli.cli.Cli`
**対応サブコマンド**: なし（ライブラリクラス）

本書は `docs/projects/def_ot_terms.md`（用語の定義）および `docs/projects/def_of_file_and_dir.md`（ディレクトリ/ファイル定義）を正とする方針で作成したが、本書作成時点で両ファイルは空である。そのため本書の記述はすべて「現行実装の挙動」に基づく。

## 未確定事項（本書作成にあたっての前提）

- 定義ドキュメント 2 件がいずれも空のため、定義由来の記述は存在せず、全記述を「現行実装の挙動」として扱った。異なる意図であればお知らせください。

## 1. 概要

`argparse.ArgumentParser` を扱いやすく包む薄いラッパー。パーサの生成、サブコマンド定義、引数解析結果の保持を 1 箇所にまとめる。CLI アプリケーションを構築する利用側コードの部品として使う。

## 2. 公開インタフェース

### 生成

```python
Cli(help_text: str)
```

`help_text` を説明文に持つパーサを初期化する。

### メソッド

| メソッド | 説明 |
|---------|------|
| `get_parser() -> argparse.ArgumentParser` | 保持しているパーサ本体を返す（引数定義の追加は利用側がこのパーサへ直接行う） |
| `parse_args() -> argparse.Namespace` | コマンドライン引数を解析して保持し、その結果を返す |
| `get_args() -> argparse.Namespace \| None` | 直近の解析結果を返す。未解析時は `None` |
| `get_subparsers(name) -> argparse._SubParsersAction` | 指定名を `dest` に持つサブコマンド定義（`required=True`）を作成して返す |

## 3. 制約（現行実装の挙動）

サブコマンド定義は `get_subparsers()` を呼んで初めて属性として存在する。呼び出し前に `subparsers` 属性へアクセスすると `AttributeError` になる。

## 4. エラー処理・終了コード

| 事象 | 挙動 | 終了コード |
|------|------|-----------|
| `parse_args()` で引数が不正（未定義オプション・必須サブコマンド欠落等） | `argparse` の標準挙動としてエラーメッセージを表示し `SystemExit` | `2` |
| `get_subparsers()` 未呼び出しで `subparsers` 属性へアクセス | `AttributeError` が呼び出し元へ伝播する | —（利用側が捕捉しなければ `1`） |

本クラス自体はコマンドとして起動されないため、上記以外の終了コードは規定しない。

## 5. 実装上の対応（参考）

本節は実装を拘束しない。

| 役割 | モジュール |
|------|-----------|
| argparse ラッパー | `yklibpy.cli.cli.Cli` |
