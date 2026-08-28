# 外部仕様書 — `Cli`

**対象**: `argparse` ベースの CLI 構築 API

## 未確定事項

正とされる2 定義文書は欠落し、`docs/projects/def_of_file_and_dir.md` も空です。本書は現行実装の挙動を記載します。異なる意図であればお知らせください。

## 1. 概要

説明付きの引数パーサを生成し、必須サブコマンドと解析結果を保持するライブラリ API です。

## 2. 利用仕様

```python
cli = Cli("説明")
parser = cli.get_parser()
subparsers = cli.get_subparsers("command")
args = cli.parse_args()
same_args = cli.get_args()
```

`get_parser()` は内部の `argparse.ArgumentParser` を返します。`parse_args()` は明示的な引数列を受け取らず、プロセスの `sys.argv` を解析して結果を保持します。`get_args()` は保持中の解析結果を返し、解析前は `None` です。`get_subparsers(name)` が作るサブコマンドは必須です。

## 3. エラー処理・終了コード

| 事象 | 挙動 | 終了コード |
|---|---|---:|
| 不明な引数、必須サブコマンドなし | usage とエラーを標準エラーへ出力 | `2`（`argparse`） |
| 正常解析 | `argparse.Namespace` を返す | コマンドとしては終了しない |
| その他の未捕捉例外 | 呼び出し元へ伝播 | CLI 最上位なら `1` |

## 4. 実装上の対応（参考）

本節は実装を拘束しません。`src/yklibpy/cli/cli.py` の `Cli` が担当します。
