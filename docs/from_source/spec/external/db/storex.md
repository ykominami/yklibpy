# 外部仕様書 — `storex`

**対象クラス**: `yklibpy.db.storex.Storex`
**対応サブコマンド**: なし（ライブラリクラス）

本書は `docs/projects/def_ot_terms.md`（用語の定義）および `docs/projects/def_of_file_and_dir.md`（ディレクトリ/ファイル定義）を正とする方針で作成したが、本書作成時点で両ファイルは空である。そのため本書の記述はすべて「現行実装の挙動」に基づく。

## 未確定事項（本書作成にあたっての前提）

- 定義ドキュメント 2 件がいずれも空のため、ファイル種別・拡張子の対応も定義由来ではなく現行実装の挙動として記載した。異なる意図であればお知らせください。

## 1. 概要

ファイル種別（YAML/JSON/TOML/プレーンテキスト）に応じた読み書きを抽象化するストレージラッパー。保存先管理クラスが解決したパス要素列から保存先パスを組み立て、`load()`/`output()` で入出力を行う。

## 2. 前提条件

1. 拡張子解決（`get_ext_name()`）を使う場合は、事前に `set_file_type_dict()` でファイル種別と拡張子の対応辞書を設定しておくこと（未設定時の既定は空辞書）。`appconfig` の対応表（YAML: `.yml`、JSON: `.json`、TOML: `.toml`）を渡すのが標準的な使い方。

## 3. 公開インタフェース

### classmethod

| メソッド | 説明 |
|---------|------|
| `set_file_type_dict(file_type_dict) -> None` | 拡張子解決に使うファイル種別辞書をクラス全体へ設定する |
| `get_ext_name(file_type) -> str` | ファイル種別に対応する拡張子を返す |

### 生成

```python
Storex(file_type: str, file_name_array: list[Path] | list[str], data: Any = None)
```

`file_name_array` は呼び出し元で組み立て済みの完全なパス要素配列。先頭要素をトップディレクトリとして残りを順に結合し、保存先パスとする。**引数配列は破壊的に消費される**（先頭要素が取り除かれる）ため、呼び出し元で再利用しないこと。

### インスタンスメソッド

| メソッド | 説明 |
|---------|------|
| `load() -> Any` | 保存先ファイルを読み込み、種別に応じて復元した保持データを返す。ファイルが存在しない場合は何もせず現在の保持データを返す |
| `output(data: Any = None) -> None` | 保持データ（または指定データ）をファイルへ書き出す。親ディレクトリが無ければ作成する |
| `set_data(data) -> None` / `get_store() -> Any` | 保持データの差し替え/取得 |
| `get_value(key) -> Any` | 保持データ（辞書前提）からキーに対応する値を返す（キーが無ければ `None`） |
| `get_name() -> str` / `get_path() -> Path` | 保存先ファイル名/完全パスを返す |

### ファイル種別ごとの入出力形式

| 種別 | 読み込み | 書き出し |
|------|---------|---------|
| YAML | `yaml.safe_load`（空なら空辞書） | `yaml.dump`（`allow_unicode=True`） |
| JSON | `json.load` | `json.dump`（`ensure_ascii=False`、`indent=2`） |
| TOML | `toml.load` | `toml.dump` |
| 上記以外 | `{"_lines": <行の配列>}` として保持 | `str(data)` をそのまま書き込む |

入出力の文字コードは常に UTF-8。

## 4. 作成・更新するディレクトリ・ファイル

| 対象 | 契機 | 内容 |
|------|------|------|
| 保存先パスの親ディレクトリ | `output()` | 存在しなければ再帰的に作成する |
| 保存先ファイル | `output()` | 種別に応じた形式で上書き保存する |

## 5. エラー処理・終了コード

| 事象 | 挙動 |
|------|------|
| `get_ext_name()` で対応辞書に無い種別を指定 | `KeyError` が呼び出し元へ伝播する |
| `load()` で内容が種別として不正 | `yaml.YAMLError`/`json.JSONDecodeError`/`toml.TomlDecodeError` が呼び出し元へ伝播する |
| `output()` で書き込みに失敗 | `OSError` 等が呼び出し元へ伝播する |
| `load()` でファイルが存在しない | 例外を送出せず、現在の保持データを返す |

ライブラリクラスであり単体のコマンドとして起動される経路は無いため、終了コードは規定しない。

## 6. 実装上の対応（参考）

本節は実装を拘束しない。

| 役割 | モジュール |
|------|-----------|
| ストレージラッパー | `yklibpy.db.storex.Storex` |
| ファイル種別定数 | `yklibpy.config.appconfig.AppConfig` |
| 主な利用元 | `yklibpy.db.appstore.AppStore`/`yklibpy.tomlop.fileitem.FileItem` |
