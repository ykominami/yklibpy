# 外部仕様書 — `tomlop`

**対象クラス**: `yklibpy.tomlop.tomlop.Tomlop`
**対応サブコマンド**: `yklibpy-tomlop-zmain`/`yklibpy-toml2yaml`/`yklibpy-yaml2toml`（CLI エントリポイント）
**コマンド**: `yklibpy-tomlop-zmain [ref_file [config_file]]`、`yklibpy-toml2yaml <file>`、`yklibpy-yaml2toml <file>`

本書は `docs/projects/def_ot_terms.md`（用語の定義）および `docs/projects/def_of_file_and_dir.md`（ディレクトリ/ファイル定義）を正とする方針で作成したが、本書作成時点で両ファイルは空である。そのため本書の記述はすべて「現行実装の挙動」に基づく。

## 未確定事項（本書作成にあたっての前提）

- 定義ドキュメント 2 件がいずれも空のため、出力ファイル名（`new_pyproject.toml` 等）はすべて現行実装の挙動として記載した。異なる意図であればお知らせください。
- `yklibpy-tomlop-zmain` の中核処理（差分計算・補完・出力）は現行実装で無効化されており（§5）、本書は現状の挙動をそのまま記載した。

## 1. 概要

TOML と YAML の比較・変換・差分出力を扱うクラス。`pyproject.toml` などの設定ファイルを参照ファイルと比較し、不足キーの補完（マージ）と差分レポートの生成を CLI から実行する用途を想定する。

## 2. コマンドライン構文

```
yklibpy-tomlop-zmain [ref_file [config_file]]
yklibpy-toml2yaml <src_file>
yklibpy-yaml2toml <input_file>
```

| 引数 | 説明 |
|------|------|
| `ref_file` | 参照（比較元）ファイル。省略時は何も実行しない |
| `config_file` | 比較先設定ファイル。省略時は `pyproject.toml` |
| `src_file`/`input_file` | 変換元ファイル。省略時は何も実行しない |

引数解析は位置ベース（`sys.argv` 直接参照）で、オプションは持たない。

## 3. サブコマンド別仕様

### 3.1 `yklibpy-tomlop-zmain`

`ref_file` が指定された場合のみ、参照ファイルと設定ファイルを準備し、参照ファイルの拡張子を YAML 用拡張子（`.yml`）へ変換したパスへ内部データを出力する。

現行実装の挙動として、差分計算・補完処理（`exec()` 相当）は呼び出しが無効化されているため、出力される内部データは空辞書であり、出力ファイルには空の内容が書き込まれる（§5）。

### 3.2 `yklibpy-toml2yaml`

`src_file` で指定した TOML を読み込み、YAML へ変換して `a.yaml`（カレントディレクトリ固定 — 現行実装の挙動）へ保存する。

### 3.3 `yklibpy-yaml2toml`

`input_file` で指定した YAML を読み込み、変換後の出力先パス（`.toml` 拡張子）を求めるところまでで終了する。**実際の TOML 書き出しは行われない**（現行実装の挙動。§5）。

## 4. ライブラリとしての公開インタフェース

| メソッド | 説明 |
|---------|------|
| `setup(ref_file, config_file) -> None` | 参照ファイルと設定ファイルの入出力オブジェクトを準備する。`config_file=None` を許容する |
| `compare_dict(dict1, dict2) -> bool` | 2 つの辞書が再帰的に完全一致するかを判定する |
| `merge_dict(dict1, dict2) -> dict` | 不足キーだけを `dict2` から `dict1` へ補完する（`dict1` を破壊的に変更して返す） |
| `diff_dict(dict1, dict2) -> str` | 2 つの辞書の差分を可読な文字列として返す（差分なしなら空文字） |
| `exec() -> None` | 参照ファイルとの差分を計算し、補完結果を `new_pyproject.toml`、差分を `diff_pyproject.toml` へ出力する |
| `read_toml_external(file_path) -> dict \| None` | 外部 TOML を読み込む。読み込み・パース失敗時はログ出力のうえ `None`（例外は伝播しない） |
| `write_toml_external(file_path, data) -> bool` | 辞書を外部 TOML へ書き出す。成功なら `True`、失敗時はログ出力のうえ `False` |
| `load_toml(ref_file) -> dict \| None` | 参照用 TOML を読み込む。未指定なら `None` |

## 5. 制約（現行実装の挙動）

- CLI（`yklibpy-tomlop-zmain`）から `exec()` は呼ばれない（呼び出しがコメントアウトされている）。差分計算・補完・出力という中核機能は、ライブラリとして `exec()` を直接呼んだ場合のみ動作する。
- `yklibpy-yaml2toml` は出力先パスを求めるだけで TOML を書き出さない（未完成の実装）。
- `yklibpy-toml2yaml` の出力先は `a.yaml` 固定で変更できない。

## 6. 作成・更新するファイル

| ファイル | 契機 | 内容 |
|---------|------|------|
| `<ref_file の拡張子を .yml に変えたパス>` | `yklibpy-tomlop-zmain`（`ref_file` 指定時） | 内部データ（現状は空）の YAML |
| `a.yaml` | `yklibpy-toml2yaml` | 変換元 TOML の内容を変換した YAML |
| `new_pyproject.toml` | `exec()`（ライブラリ利用時のみ） | 参照ファイルの不足キーを補完した設定 |
| `diff_pyproject.toml` | `exec()`（ライブラリ利用時のみ） | 差分レポート文字列 |

## 7. エラー処理・終了コード

| 事象 | 挙動 | 終了コード |
|------|------|-----------|
| CLI で引数省略（`ref_file`/`src_file`/`input_file` なし） | 何も実行せず正常終了する | `0` |
| `exec()` で比較先設定ファイルが未設定（`setup()` に `config_file=None` を渡した） | `ValueError`（メッセージ: `config_file_item is not set`） | ライブラリ利用のため規定しない（CLI 経由では到達しない） |
| `setup()` 未呼び出しで `exec()` を呼ぶ | `AttributeError` が呼び出し元へ伝播する | 同上 |
| 変換元ファイルの拡張子が未対応 | `ValueError` が伝播する（`fileitem` 参照） | 未捕捉のため Python 標準の挙動として `1` |
| 変換元ファイルが存在しない（`yklibpy-yaml2toml`） | `FileNotFoundError` が伝播する | 同上 `1` |
| TOML 読み込み失敗（`read_toml_external()`） | ログ出力のうえ `None` を返す（例外は伝播しない） | — |

## 8. 実装上の対応（参考）

本節は実装を拘束しない。

| 役割 | モジュール |
|------|-----------|
| 比較・変換・差分出力 | `yklibpy.tomlop.tomlop.Tomlop` |
| CLI エントリポイント | `yklibpy.tomlop.__init__`（`zmain`/`toml2yaml`/`yaml2toml` — 同名のインスタンスメソッドとは別物） |
| ファイル入出力の抽象化 | `yklibpy.tomlop.fileitem.FileItem` |
| YAML の読み書き | `yklibpy.common.util_yaml.UtilYaml` |
