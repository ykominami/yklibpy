# 外部仕様書 — `preparex`

**対象クラス**: `yklibpy.htmlparser.preparex.Preparex`
**対応サブコマンド**: なし（ライブラリクラス）

本書は `docs/projects/def_ot_terms.md`（用語の定義）および `docs/projects/def_of_file_and_dir.md`（ディレクトリ/ファイル定義）を正とする方針で作成したが、本書作成時点で両ファイルは空である。そのため本書の記述はすべて「現行実装の挙動」に基づく。

## 未確定事項（本書作成にあたっての前提）

- 定義ドキュメント 2 件がいずれも空のため、作成されるディレクトリ構成も定義由来ではなく現行実装の挙動として記載した。異なる意図であればお知らせください。

## 1. 概要

設定情報からスクレイピング関連ディレクトリ（コマンド用・HTML パーサ用）を作成し、対象ファイル名の列挙・検索を行うクラス。コンストラクタがディレクトリ作成とディレクトリ走査の副作用を持つ点が特徴。

## 2. 公開インタフェース

### 生成

```python
Preparex(top_dir: str, category: str, config_parent_dir: str, assoc: dict[str, Any])
```

`assoc` は `configprepare` 参照のフォーマットに従う設定辞書。生成時に §3 のディレクトリを作成し、`top_dir` 配下をカテゴリ設定ファイルの拡張子で走査する。

### メソッド

| メソッド | 説明 |
|---------|------|
| `list_files_containing(path, search_string) -> list[Path]` | 指定ディレクトリ直下で名前に `search_string` を含むファイルを列挙する。`path` が存在しない、またはディレクトリでない場合は空配列 |
| `list_files(path, name) -> list[Path]` | 上記の薄いラッパー（デバッグログ付き） |
| `list_htmlparser_files(name) -> list[Path]` | HTML パーサ出力ディレクトリから対象ファイルを列挙する |
| `list_bat1_files(name) -> list[Path]` | コマンド関連ディレクトリから対象ファイルを列挙する |
| `list_utility_files(name, suffix) -> list[str]` | ユーティリティカテゴリ一覧から `"{name}-{category}{suffix}"` 形式のファイル名候補を組み立てる |

## 3. 作成・更新するディレクトリ

生成時に以下を `mkdir -p` 相当（`parents=True, exist_ok=True`）で作成する。

```
<top_dir>/<command.dir>/     # コマンド関連ファイルの配置ディレクトリ
<top_dir>/<category>/        # HTML パーサ出力ディレクトリ
```

## 4. エラー処理・終了コード

| 事象 | 挙動 |
|------|------|
| 設定辞書に必要なキーが無い | `KeyError` が呼び出し元へ伝播する（`configprepare` 参照） |
| `top_dir` がディレクトリでない | `ValueError` が呼び出し元へ伝播する（走査処理由来） |
| ディレクトリを作成できない | `OSError` が呼び出し元へ伝播する |

ライブラリクラスであり単体のコマンドとして起動される経路は無いため、終了コードは規定しない。

## 5. 実装上の対応（参考）

本節は実装を拘束しない。

| 役割 | モジュール |
|------|-----------|
| ディレクトリ準備・ファイル列挙 | `yklibpy.htmlparser.preparex.Preparex` |
| 設定値の読み出し | `yklibpy.htmlparser.configprepare.ConfigPrepare` |
| パス探索・候補名組み立て | `yklibpy.common.util.Util` |
