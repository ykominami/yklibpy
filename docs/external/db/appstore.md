# AppStore — 外部仕様書

## 概要

`yklibpy.db.appstore.AppStore`

設定ファイルと DB ファイルの保存先解決・生成・入出力を統括するクラス。
OS（Windows / Unix 系）のディレクトリ規約に従ってパスを決定し、`Storex` オブジェクトとして管理する。

## 保存先規約

| OS | 設定ファイル (`KIND_CONFIG`) | DB ファイル (`KIND_DB`) |
|----|-----------------------------|------------------------|
| Windows | `%APPDATA%\{prog_name}\` | `%LOCALAPPDATA%\{prog_name}\` |
| Unix | `~/.config/{prog_name}/` | `~/.local/share/{prog_name}/` |

`user` が指定された場合はパスにユーザー名のサブディレクトリが追加される。

## コンストラクタ

```python
AppStore(
    prog_name: str,
    file_assoc: dict[str, dict[str, dict[str, Any]]],
    user: str | None,
    directory_assoc: dict[str, dict[str, dict[str, Any]]] | None = None,
)
```

`user` は `Util.normalize_string` で正規化し、空白のみの場合は `None` として扱う。
初期化の最後に `set_ext_name` を呼び出して `file_assoc` 内の拡張子情報を補完する。

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `prog_name` | `str` | アプリ名（ディレクトリ名として使用） |
| `file_assoc` | `dict` | ファイル定義テーブル（`AppConfig.file_assoc` を継承したもの） |
| `directory_assoc` | `dict` | ディレクトリ定義テーブル |
| `user` | `str \| None` | ユーザー名（マルチユーザー対応時に使用） |
| `home_path` | `Path` | ホームディレクトリ |

## パブリック API

### ファイル準備

| メソッド | 説明 |
|----------|------|
| `prepare_config_file_and_db_file()` | 設定ファイルと DB ファイルをまとめて準備する |
| `prepare_config_file()` | `KIND_CONFIG` のファイルを準備する |
| `prepare_db_file()` | `KIND_DB` のファイルを準備する |
| `prepare_all_files(kind)` | 指定種別のすべてのファイルを再準備する |

### ディレクトリ準備

| メソッド | 説明 |
|----------|------|
| `prepare_config_directory_and_db_directory()` | 設定用・DB 用ディレクトリをまとめて準備する |
| `prepare_config_directory()` | `KIND_CONFIG` のディレクトリを準備する |
| `prepare_db_directory()` | `KIND_DB` のディレクトリを準備する |
| `prepare_all_directory()` | 全種別のディレクトリを準備する |
| `mkdir_db(key)` | DB 用サブディレクトリを作成し、パスを `directory_assoc` へ保存する |

### ファイル読み込み

| メソッド | 説明 |
|----------|------|
| `load_file_all()` | 全ファイルを読み込み、`VALUE` フィールドへ反映する |
| `load_file_db_all()` | DB 種別の全ファイルを読み込む |
| `load_file_db(base_name)` | 指定した DB ファイルを読み込む |
| `load_file_config_all()` | 設定種別の全ファイルを読み込む |
| `load_file_config(base_name)` | 指定した設定ファイルを読み込む |

### 値取得

| メソッド | 説明 |
|----------|------|
| `get_file_assoc_from_config(base_name)` | 設定ファイルから読み込んだ値を返す |
| `get_file_assoc_from_db(base_name)` | DB ファイルから読み込んだ値を返す |
| `get_from_config(base_name, key)` | 設定値辞書から指定キーの値を取り出す |
| `get_directory_assoc_from_config(base_name)` | 設定用ディレクトリ定義から対象項目を返す |
| `get_directory_assoc_from_db(base_name)` | DB 用ディレクトリ定義から対象項目を返す |

### ファイル書き出し

| メソッド | 説明 |
|----------|------|
| `output_config(key, data)` | 設定ファイルへ辞書データを書き出す |
| `output_db(key, data)` | DB ファイルへ辞書データを書き出す |

### デバッグ

| メソッド | 説明 |
|----------|------|
| `show(kind, base_name)` | 読み込み済みデータの内容をデバッグログへ出力する |
| `show_config(base_name)` | 設定データの内容を表示する |
| `show_db(base_name)` | DB データの内容を表示する |

## 制約

- `prepare_*_file` を呼び出した後でなければ `load_*` や `output_*` は正しく動作しない。
- `user` はコンストラクタ時にのみ設定される。後から変更する手段は提供されていない。

## 依存関係

- `yklibpy.common.loggerx.Loggerx`
- `yklibpy.common.util.Util`
- `yklibpy.config.appconfig.AppConfig`
- `yklibpy.db.storex.Storex`
