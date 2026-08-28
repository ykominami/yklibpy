# 外部仕様書 — `configprepare`

**対象クラス**: `yklibpy.htmlparser.configprepare.ConfigPrepare`
**対応サブコマンド**: なし（ライブラリクラス）

本書は `docs/projects/def_ot_terms.md`（用語の定義）および `docs/projects/def_of_file_and_dir.md`（ディレクトリ/ファイル定義）を正とする方針で作成したが、本書作成時点で両ファイルは空である。そのため本書の記述はすべて「現行実装の挙動」に基づく。

## 未確定事項（本書作成にあたっての前提）

- 定義ドキュメント 2 件がいずれも空のため、設定辞書の構造も現行実装が期待する形を本書で整理した。異なる意図であればお知らせください。

## 1. 概要

HTML パーサ関連設定（YAML 由来の連想配列）へのアクセスを、キー名を意識せず読み出せるように簡略化するアクセサクラス。

## 2. 公開インタフェース

### 生成

```python
ConfigPrepare(parent_file_path: Path, assoc: dict[str, Any])
```

### 設定辞書のフォーマット（現行実装が期待する構造）

```yaml
command:
  dir: <コマンド関連ファイルの配置ディレクトリ名>
  utility-category: [<category1>, <category2>]
  utility-root: <ユーティリティ探索の起点>
category-config-file-extname: <カテゴリ設定ファイルの拡張子>
category:
  htmlparser: <HTML パーサ用カテゴリ設定>
```

### アクセサ

| メソッド | 返す値 |
|---------|--------|
| `get(key)` | 指定キーに対応する設定値 |
| `get_command()` | `command` セクション全体 |
| `get_command_dir()` | `command.dir` |
| `get_category_config_file_extname()` | `category-config-file-extname` |
| `get_utility_category()` | `command.utility-category` |
| `get_utility_root()` | `command.utility-root` |
| `get_category()` | `category` セクション全体 |
| `get_htmlparser()` | `category.htmlparser` |

## 3. エラー処理・終了コード

| 事象 | 挙動 |
|------|------|
| 設定辞書に該当キーが無い | `KeyError` が呼び出し元へ伝播する（すべてのアクセサはキーの存在を検証しない） |

ライブラリクラスであり単体のコマンドとして起動される経路は無いため、終了コードは規定しない。

## 4. 実装上の対応（参考）

本節は実装を拘束しない。

| 役割 | モジュール |
|------|-----------|
| 設定アクセサ | `yklibpy.htmlparser.configprepare.ConfigPrepare` |
| 主な利用元 | `yklibpy.htmlparser.preparex.Preparex` |
