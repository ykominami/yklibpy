# AppConfig — 外部仕様書

## 概要

`yklibpy.config.appconfig.AppConfig`

アプリ全体で共有する設定キー・ファイル種別定義・ファイル関連付けテーブルを保持するクラス。
インスタンス化せず、クラス変数とクラスメソッドのみを使う。サブクラスで継承して拡張することも想定される。

## クラス定数

### ファイル種別

| 定数 | 値 |
|------|----|
| `FILE_TYPE_YAML` | `"YAML"` |
| `FILE_TYPE_JSON` | `"JSON"` |
| `FILE_TYPE_TOML` | `"TOML"` |

### ディレクトリ種別

| 定数 | 値 |
|------|----|
| `DIR_TYPE` | `"DIRECTORY"` |

### ファイル種別（kind）

| 定数 | 値 |
|------|----|
| `KIND_CONFIG` | `"config"` |
| `KIND_DB` | `"db"` |
| `KIND_FETCH` | `"fetch"` |

### ベース名

| 定数 | 値 |
|------|----|
| `BASE_NAME_CONFIG` | `"config"` |
| `BASE_NAME_DB` | `"db"` |
| `BASE_NAME_FETCH` | `"fetch"` |

### 辞書キー

| 定数 | 値 |
|------|----|
| `PATH` | `"path"` |
| `FILE_TYPE` | `"file_type"` |
| `EXT_NAME` | `"ext_name"` |
| `VALUE` | `"value"` |
| `DATE` | `"date"` |

## クラス変数

### `file_type_dict: dict[str, str]`

ファイル種別名から拡張子へのマッピング。

| キー | 値 |
|------|----|
| `"YAML"` | `".yml"` |
| `"JSON"` | `".json"` |
| `"TOML"` | `".toml"` |

### `file_type_reverse_dict: dict[str, str]`

`file_type_dict` のキーと値を入れ替えた逆引き辞書（`Util.swap_dict` で生成）。

### `file_synonym_dict: dict[str, str]`

拡張子の別名マッピング。現在は `".yaml"` → `".yml"` のみ定義。

### `directory_assoc: dict[str, dict[str, dict[str, Any]]]`

`KIND_CONFIG` / `KIND_DB` の 2 種別のディレクトリ定義テーブル。サブクラスで拡張する。

### `file_assoc: dict[str, dict[str, dict[str, Any]]]`

`KIND_CONFIG` / `KIND_DB` に対応するファイル定義テーブル。
デフォルトでは `config.yml`・`db.yml`・`fetch.yml` の 3 ファイルが定義される。

### `fetch_item: dict[str, str]`

取得履歴レコードのデフォルトフィールド定義。現在は `date` フィールドのみ。

## パブリック API

### `get_file_type(file_path: str | None) -> str | None`

拡張子から内部で使うファイル種別名（`"YAML"` / `"JSON"` / `"TOML"`）を返す。
- `.yaml` は `.yml` に正規化してから参照する。
- 未知の拡張子の場合は `None` を返す。

## 継承と拡張

`directory_assoc` と `file_assoc` はクラス変数であり、サブクラスでエントリを追加して拡張できる。

## 依存関係

- `yklibpy.common.util.Util`（`swap_dict` の使用）
