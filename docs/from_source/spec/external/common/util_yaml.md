# 外部仕様書 — `util_yaml`

**対象クラス**: `yklibpy.common.util_yaml.UtilYaml`
**対応サブコマンド**: なし（ライブラリクラス）

本書は `docs/projects/def_ot_terms.md`（用語の定義）および `docs/projects/def_of_file_and_dir.md`（ディレクトリ/ファイル定義）を正とする方針で作成したが、本書作成時点で両ファイルは空である。そのため本書の記述はすべて「現行実装の挙動」に基づく。

## 未確定事項（本書作成にあたっての前提）

- 定義ドキュメント 2 件がいずれも空のため、定義由来の記述は存在せず、全記述を「現行実装の挙動」として扱った。異なる意図であればお知らせください。

## 1. 概要

YAML の読み書きと、YAML 内に残る `!!python/object:...` 等の未知の Python オブジェクトタグを安全に無害化するカスタムコンストラクタ登録をまとめた補助クラス。すべて classmethod として提供する。

## 2. 公開インタフェース

### `safe_load(f: Any) -> Any`（classmethod）

`yaml.SafeLoader` を使って YAML を読み込む。カスタムタグの無害化が必要な場面では、事前にタグ登録（`_register_constructors()`。内部メソッドだが他モジュールから使われる — 現行実装の挙動）を済ませたうえで本メソッド系の読み込みを使う。

### `load_yaml(input_path: Path) -> dict[str, Any]`（classmethod）

YAML ファイルを UTF-8 で読み込み、辞書として返す。`yaml.FullLoader` を使う。読み込み結果が `None`（空ファイル等）の場合は空辞書を返す。

### `save_yaml(assoc: dict[Any, Any], output_path: Optional[Path] = None) -> str`（classmethod）

辞書を YAML 文字列へ変換して返す（`allow_unicode=True`、`sort_keys=False`）。`output_path` が指定されていれば同じ内容を UTF-8 でファイルへも保存する。

### `ignore_python_object_tag(loader: Any, node: Any) -> Any`（classmethod）

未知の Python オブジェクトタグを安全な値（辞書/配列/スカラー）へ変換するコンストラクタ関数。タグ登録時に使う。

## 3. 作成・更新するファイル

| ファイル | 契機 | 内容 |
|---------|------|------|
| `output_path` に指定したファイル | `save_yaml()` で `output_path` 指定時 | 辞書を変換した YAML（UTF-8） |

## 4. 制約（現行実装の挙動）

- 読み込みメソッドによって安全性レベルが異なる: `load_yaml()` は `yaml.FullLoader`、`safe_load()` は `yaml.SafeLoader` を使う。
- タグ登録はプロセス全体へ影響するグローバルな副作用であり、一度登録すると全呼び出しに効く。登録済みの場合、追加の登録要求（引数 `tags`）は無視される。

## 5. エラー処理・終了コード

| 事象 | 挙動 |
|------|------|
| `load_yaml()` の対象ファイルが存在しない | `FileNotFoundError` が呼び出し元へ伝播する |
| YAML として不正な内容 | `yaml.YAMLError` が呼び出し元へ伝播する |
| `save_yaml()` の保存先へ書き込めない | `OSError` が呼び出し元へ伝播する |

ライブラリクラスであり単体のコマンドとして起動される経路は無いため、終了コードは規定しない。

## 6. 実装上の対応（参考）

本節は実装を拘束しない。

| 役割 | モジュール |
|------|-----------|
| YAML 読み書き・タグ無害化 | `yklibpy.common.util_yaml.UtilYaml` |
| 主な利用元 | `yklibpy.db.db_yaml.DbYaml`（読み込み時のタグ無害化） |
