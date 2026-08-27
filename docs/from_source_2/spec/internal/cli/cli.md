# Cli — 内部仕様書

**ファイル**: `src/yklibpy/cli/cli.py`  
**継承**: なし

## 概要

`argparse.ArgumentParser` と解析結果を保持し、サブコマンド定義を簡潔に扱うためのラッパーである。

---

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `parser` | `argparse.ArgumentParser` | コマンドライン引数パーサ。 |
| `args` | `argparse.Namespace \| None` | 直近の解析結果。 |
| `subparsers` | `argparse._SubParsersAction` | `get_subparsers` 呼び出し後のサブパーサ群。 |

---

## メソッド

### `__init__(help_text: str) -> None`

説明文を指定してパーサを作り、解析結果を未設定にする。

### `get_parser() -> argparse.ArgumentParser`

保持中のパーサを返す。

### `get_args() -> argparse.Namespace | None`

直近の解析結果を返す。

### `parse_args() -> argparse.Namespace`

プロセスの引数を解析し、結果を `args` に保存して返す。

### `get_subparsers(name: str) -> argparse._SubParsersAction[argparse.ArgumentParser]`

`name` を選択済みコマンド格納先とする必須サブパーサ群を作り、保持して返す。

---

## 依存

| クラス/変数 | 用途 |
|-------------|------|
| `argparse.ArgumentParser` | 引数定義と解析を担当する。 |

## 設計上の注意

`subparsers` はコンストラクタでは宣言されず、`get_subparsers()` の初回呼び出し時に動的に追加される。`parse_args()` は引数列を受け取れず、常にプロセスの `sys.argv` を解析する。
