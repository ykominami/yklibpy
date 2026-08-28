# Cli — 外部仕様書

## 概要

`yklibpy.cli.cli.Cli`

`argparse.ArgumentParser` を薄く包み、CLI アプリの引数定義・解析・サブコマンド管理を扱いやすくするラッパー。

## コンストラクタ

```python
Cli(help_text: str)
```

`help_text` を description に持つ `ArgumentParser` を生成する。`args` は初期値 `None`。

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `parser` | `argparse.ArgumentParser` | 内部の引数パーサ |
| `args` | `argparse.Namespace \| None` | `parse_args` 実行後の解析結果 |

## パブリック API

### `get_parser() -> argparse.ArgumentParser`

保持している `ArgumentParser` を返す。引数の追加定義に使用する。

### `get_args() -> argparse.Namespace | None`

直近の `parse_args` 呼び出しで得た解析結果を返す。`parse_args` 呼び出し前は `None`。

### `parse_args() -> argparse.Namespace`

コマンドライン引数を解析して内部に保持する。
`argparse.ArgumentParser.parse_args()` を呼び出すため、エラー時はプロセスが終了する。

### `get_subparsers(name: str) -> argparse._SubParsersAction`

`name` を `dest` に持つサブコマンド定義オブジェクトを生成して返す。`required=True` が設定されており、サブコマンドの指定が必須となる。

## 使用例

```python
cli = Cli("My tool description")
cli.get_parser().add_argument("--verbose", action="store_true")
args = cli.parse_args()
```

## 依存関係

- `argparse`（標準ライブラリ）
