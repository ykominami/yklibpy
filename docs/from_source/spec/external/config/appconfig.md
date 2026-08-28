# 外部仕様書 — `appconfig`

**対象クラス**: `yklibpy.config.appconfig.AppConfig`
**対応サブコマンド**: なし（ライブラリクラス・定数クラス）

本書は `docs/projects/def_ot_terms.md`（用語の定義）および `docs/projects/def_of_file_and_dir.md`（ディレクトリ/ファイル定義）を正とする方針で作成したが、本書作成時点で両ファイルは空である。そのため本書の記述はすべて「現行実装の挙動」に基づく。

## 未確定事項（本書作成にあたっての前提）

- 定義ドキュメント 2 件がいずれも空のため、定義由来の記述は存在せず、全記述を「現行実装の挙動」として扱った。異なる意図であればお知らせください。

## 1. 概要

アプリ全体で共有する設定キー名・ファイル種別・拡張子対応表・ディレクトリ/ファイル関連付けの初期定義を保持する定数クラス。ファイルアクセス系の全モジュールから参照される。継承して拡張することも想定されている。

## 2. 公開インタフェース

### 定数

| 定数名 | 値 | 説明 |
|--------|----|------|
| `FILE_TYPE_YAML`/`FILE_TYPE_JSON`/`FILE_TYPE_TOML` | `"YAML"`/`"JSON"`/`"TOML"` | ファイル種別識別子 |
| `DIR_TYPE` | `"DIRECTORY"` | ディレクトリ種別識別子 |
| `KIND_CONFIG`/`KIND_DB`/`KIND_FETCH` | `"config"`/`"db"`/`"fetch"` | 種別キー |
| `BASE_NAME_CONFIG`/`BASE_NAME_DB`/`BASE_NAME_FETCH` | `"config"`/`"db"`/`"fetch"` | 既定ベース名 |
| `PATH`/`FILE_TYPE`/`EXT_NAME`/`VALUE`/`DATE` | `"path"`/`"file_type"`/`"ext_name"`/`"value"`/`"date"` | 関連付け辞書の格納キー名 |
| `file_type_dict` | YAML: `.yml`、JSON: `.json`、TOML: `.toml` | 種別 → 拡張子の対応表 |
| `file_type_reverse_dict` | 上記の反転 | 拡張子 → 種別の対応表 |
| `file_synonym_dict` | `.yaml` → `.yml` | 拡張子の別名解決表 |
| `directory_assoc` | `config`/`db` とも空辞書 | ディレクトリ関連付けの既定枠（継承先で拡張する前提） |
| `file_assoc` | `config` 配下に `config`、`db` 配下に `db`/`fetch` の初期エントリ | ファイル関連付けの既定定義 |
| `fetch_item` | `date` キーのみ | 取得履歴の項目テンプレート |

### `get_file_type(file_path: str | None) -> str | None`（classmethod）

拡張子から内部で使うファイル種別名を返す。大文字小文字は区別せず、別名（`.yaml`）は解決したうえで判定する。判定できない場合と `None` 入力は `None` を返す。

## 3. 制約（現行実装の挙動）

`file_assoc`/`directory_assoc`/`file_type_dict` 等はクラス変数として定義されたミュータブルな辞書であり、保存先管理クラスはこれをコピーせず受け取って内部で書き換える。複数のインスタンス間で同じ辞書を共有すると変更が波及するため、必要に応じて利用側で `copy.deepcopy` すること。

## 4. エラー処理・終了コード

例外を送出する経路は無い（`get_file_type()` は判定不能時に `None` を返す）。ライブラリクラスであり単体のコマンドとして起動される経路は無いため、終了コードは規定しない。

## 5. 実装上の対応（参考）

本節は実装を拘束しない。

| 役割 | モジュール |
|------|-----------|
| 定数・初期定義 | `yklibpy.config.appconfig.AppConfig` |
| 主な利用元 | `yklibpy.db.appstore.AppStore`/`yklibpy.db.storex.Storex`/`yklibpy.tomlop.fileitem.FileItem` |
