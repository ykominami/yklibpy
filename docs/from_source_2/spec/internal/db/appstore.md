# AppStore — 内部仕様書

**ファイル**: `src/yklibpy/db/appstore.py`  
**継承**: なし

## 概要

設定・DB の関連付け定義を保持し、OS とユーザーに応じた保存先の解決、`Storex` の構築、値とディレクトリの入出力を統括する。

---

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `user` | `str \| None` | 正規化済みユーザー識別子。 |
| `home_path` | `Path` | ホームディレクトリ。 |
| `prog_name` | `str` | 保存先階層に使うプログラム名。 |
| `file_assoc` | `dict[str, dict[str, dict[str, Any]]]` | 種別・ベース名別のファイル定義と値。 |
| `directory_assoc` | `dict[str, dict[str, dict[str, Any]]]` | ディレクトリ定義と解決済みパス。 |

---

## メソッド

### `__init__(prog_name, file_assoc, user, directory_assoc=None) -> None`

ユーザーを正規化し、関連付けとホームを保持して、各ファイル定義へ拡張子を補完する。

### `set_ext_name() -> None`

全ファイル定義のファイル種別を `Storex.get_ext_name` で拡張子へ変換する。定義欠落時は処理を打ち切る。

### `prepare_config_file_and_db_file() -> None`

設定ファイルと DB ファイルの準備を順に実行する。

### `prepare_config_file() -> None` / `prepare_db_file() -> None`

対応する種別を `prepare_file_level1` へ委譲する。

### `prepare_file_level1(kind: str) -> None`

種別配下の全ベース名を `prepare_file_level2` で準備する。

### `prepare_file_level2(kind: str, base_name: str) -> None`

定義から `Storex` を生成し、ユーザー有無に応じた `PATH` スロットへ格納する。

### `prepare_all_files(kind: str) -> None`

指定種別の全ファイル保存先を再構築する。

### `prepare_config_directory_and_db_directory() -> None`

設定用と DB 用のディレクトリ準備を順に実行する。

### `prepare_config_directory() -> None` / `prepare_db_directory() -> None`

各種別を `prepare_directory` へ委譲する。

### `prepare_directory(kind: str) -> None`

種別配下の全ベース名を `prepare_sub_directory` で準備する。

### `prepare_all_directory() -> None`

登録されたすべてのディレクトリ種別を準備する。

### `prepare_sub_directory(kind: str, base_name: str) -> None`

`mkdir_db(base_name)` を呼ぶ。`kind` は使用しない。

### `get_directory_assoc_from_config(base_name) -> OpResult[Any]`

設定用ディレクトリ定義をユーザー階層に応じて取得し、成功または診断付き失敗として返す。

### `get_directory_assoc_from_db(base_name) -> OpResult[Any]`

DB 用ディレクトリ定義を同様に取得する。

### `load_file_db_all() -> None` / `load_file_config_all() -> None`

対応種別の全 `Storex` を読み、ユーザー階層に応じて `VALUE` へ格納する。

### `load_file_db(base_name) -> None` / `load_file_config(base_name) -> None`

対応種別の単一ファイルを読み、`VALUE` へ格納する。

### `load_file_all() -> None`

全種別・全ベース名の保存先を読み込み、関連付けへ反映する。

### `get_file_assoc_from_config(base_name) -> OpResult[Any>` / `get_file_assoc_from_db(base_name) -> OpResult[Any]`

読み込み済みの設定値または DB 値を返し、キー不足は説明付き失敗に変換する。

### `get_file(user, kind, base_name, assoc) -> Storex | None`

設定種別なら `get_config_file`、それ以外は `get_db_file` へ振り分ける。

### `get_config_file(user, key, assoc) -> Storex | None` / `get_db_file(user, key, assoc) -> Storex | None`

OS 別のパス要素を求め、定義されたファイル種別の `Storex` を作る。

### `get_config_file_for_win(user, base_name, ext_name) -> list[str]`

`APPDATA`（未設定時はホーム配下）を起点とする設定パス要素を返す。

### `get_db_file_for_win(user, base_name, ext_name) -> list[str]`

`LOCALAPPDATA` を起点とする DB パス要素を返す。

### `get_config_file_for_unix(user, base_name, ext_name) -> list[str]`

`~/.config/<prog_name>/...` のパス要素を返す。

### `get_db_file_for_unix(user, base_name, ext_name) -> list[str]`

`~/.local/share/<prog_name>/...` のパス要素を返す。

### `get_from_config(base_name, key) -> OpResult[Any]`

読み込み済み設定辞書からキーを取得し、キー不足を詳細な失敗結果に変換する。

### `output_config(key, data) -> None` / `output_db(key, data) -> None`

ユーザー有無に応じた `Storex` へ辞書を書き出す。設定出力は関連付けの値も更新するが、DB 出力は更新しない。

### `mkdir_db(key: str) -> None`

OS 別データルート配下に `<prog_name>/<key>` を作り、DB ディレクトリ関連付けへパスを保存する。

### `show(kind, base_name) -> None`

読み込み済み辞書の各キーと値をデバッグログへ出す。

### `show_config(base_name) -> None` / `show_db(base_name) -> None`

設定または DB 種別の表示を `show` へ委譲する。

---

## 依存

| クラス/変数 | 用途 |
|-------------|------|
| `AppConfig` | 関連付け辞書のキーと種別定数。 |
| `Storex` | 実ファイルの入出力。 |
| `OpResult` | 取得失敗を値として返す。 |
| `Util.normalize_string` / `Util.is_empty` | ユーザー識別子の正規化。 |
| `Path`, `os.environ`, `sys.platform` | OS 別保存先の構築。 |
| `Loggerx` | 詳細デバッグログ。 |

## 設計上の注意

多数のメソッドが `KeyError` を握りつぶして部分初期化を許すため、呼び出し側は準備完了を戻り値で判定できない。関連付け辞書はユーザー有無で値の形が変わり、静的な型保証が弱い。`prepare_sub_directory` の `kind` は未使用で、常に DB ディレクトリを作る。`get_file` は設定以外の未知種別も DB として扱う。ログには設定値全体が含まれる場合がある。
