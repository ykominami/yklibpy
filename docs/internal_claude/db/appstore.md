# AppStore — 内部仕様書

## モジュール

`yklibpy.db.appstore`

## インスタンス変数

| 変数名 | 型 | 役割 |
|--------|----|------|
| `user` | `str \| None` | 正規化済みユーザー名。空文字は `None` に変換される |
| `home_path` | `Path` | `Path.home()` で取得したホームディレクトリ |
| `prog_name` | `str` | アプリ名（ファイルパスの一部として使われる） |
| `file_assoc` | `dict[str, dict[str, dict[str, Any]]]` | ファイル管理辞書（`AppConfig.file_assoc` 相当） |
| `directory_assoc` | `dict[str, dict[str, dict[str, Any]]]` | ディレクトリ管理辞書 |

## `__init__` の処理フロー

1. `Util.normalize_string(user)` でユーザー名を正規化、空なら `None` へ
2. 各変数を初期化
3. `set_ext_name()` を呼んで `file_assoc` 内の各エントリへ拡張子を補完

## `set_ext_name` の実装詳細

- `file_assoc[kind][base_name][FILE_TYPE]` でファイル種別を取得
- `Storex.get_ext_name(file_type)` で拡張子を取得し `file_assoc[kind][base_name][EXT_NAME]` へ書き込む

## `prepare_file_level2` の実装詳細

- `get_file(user, kind, base_name, file_item_assoc)` で `Storex` インスタンスを生成
- `user` が `None` でない場合：`file_assoc[kind][base_name][PATH][user] = storex`
- `user` が `None` の場合：`file_assoc[kind][base_name][PATH] = storex`（辞書ではなく直接代入）

## ファイルパス解決ロジック

| OS | 設定ファイル | DB ファイル |
|----|------------|------------|
| Windows | `%APPDATA%/<prog>/<user?>/<base><ext>` | `%LOCALAPPDATA%/<prog>/<user?>/<base><ext>` |
| Unix | `~/.config/<prog>/<user?>/<base><ext>` | `~/.local/share/<prog>/<user?>/<base><ext>` |

`user` が `None` の場合はパス要素からユーザー名が省かれる。

## `load_file_db_all` / `load_file_config_all` の実装詳細

- `user` が `None` でない場合：`file_assoc[kind][base_name][VALUE][user] = storex.load()`
- `user` が `None` の場合：`file_assoc[kind][base_name][VALUE] = storex.load()`

## `output_db` / `output_config` の実装詳細

- `user` の有無で `PATH` の参照先が異なる（`PATH[user]` vs `PATH` 直接）
- `Storex.output(data)` を呼んでファイル書き込みを行う

## `mkdir_db` の実装詳細

- OS に応じてベースディレクトリを決定し `{base}/{prog}/{key}` のパスを `mkdir(parents=True, exist_ok=True)` で作成
- 作成した `dir_path` を `directory_assoc[KIND_DB][key][PATH]` に格納

## 依存関係

- `os`, `sys`, `pathlib.Path`（標準ライブラリ）
- `yklibpy.common.loggerx.Loggerx`
- `yklibpy.common.util.Util`
- `yklibpy.config.appconfig.AppConfig`
- `yklibpy.db.storex.Storex`
