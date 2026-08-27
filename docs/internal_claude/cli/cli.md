# Cli — 内部仕様書

## モジュール

`yklibpy.cli.cli`

## インスタンス変数

| 変数名 | 型 | 初期値 | 役割 |
|--------|----|--------|------|
| `parser` | `argparse.ArgumentParser` | `ArgumentParser(description=help_text)` | 内部で保持するパーサ本体 |
| `args` | `argparse.Namespace \| None` | `None` | `parse_args` 実行後の解析結果 |
| `subparsers` | `argparse._SubParsersAction` | （未設定） | `get_subparsers` 呼び出し後に設定されるサブコマンド定義 |

## メソッドの実装詳細

### `get_subparsers(name: str)`

- `self.parser.add_subparsers(dest=name, required=True)` を呼ぶ
- 戻り値をそのまま `self.subparsers` に保存し返却する
- `required=True` のため、サブコマンドなしで実行するとエラーになる

### `parse_args()`

- `self.parser.parse_args()` を呼び、結果を `self.args` に保存してから返す
- 引数リストの注入（`parse_args([...])` 形式）は直接サポートしていない

## 依存関係

- `argparse`（標準ライブラリ）
