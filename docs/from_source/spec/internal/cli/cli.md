# Cli — 内部仕様書

**ファイル**: `src/yklibpy/cli/cli.py`
**継承**: なし

## 概要

`argparse.ArgumentParser` を扱いやすく包む薄いラッパー。パーサの生成、サブコマンド定義、引数解析結果の保持を 1 箇所にまとめる。

---

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `parser` | `argparse.ArgumentParser` | 内部で保持するパーサ本体。 |
| `args` | `argparse.Namespace \| None` | 直近の `parse_args()` 結果。未解析時は `None`。 |
| `subparsers` | `argparse._SubParsersAction[argparse.ArgumentParser]` | `get_subparsers()` 呼び出し後に設定されるサブコマンド定義。未呼び出し時は未設定（属性自体が存在せず、アクセスすると `AttributeError`）。 |

---

## メソッド

### `__init__(help_text: str) -> None`

説明文付きのパーサを初期化する。

### `get_parser() -> argparse.ArgumentParser`

保持しているパーサを返す。

### `get_args() -> argparse.Namespace | None`

直近に解析した引数解析結果を返す。

### `parse_args() -> argparse.Namespace`

コマンドライン引数を解析して `self.args` に保持し、その結果を返す。

### `get_subparsers(name: str) -> argparse._SubParsersAction[argparse.ArgumentParser]`

指定名を `dest` に持つサブコマンド定義（`required=True`）を作成し、`self.subparsers` に保持したうえで返す。

---

## 依存

なし（標準の `argparse` のみ）。

---

## 設計上の注意

`subparsers` は `__init__()` では初期化されず、`get_subparsers()` を呼んで初めて属性として存在する。呼び出し前に `self.subparsers` へアクセスすると `AttributeError` になる。
