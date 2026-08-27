# AppStore — 内部仕様書

**ファイル**: `src/yklibpy/db/appstore.py`
**継承**: なし

## 概要

OS ごとの規約（Windows: APPDATA/LOCALAPPDATA、Unix: XDG）に従って設定ファイル・DB ファイル・ディレクトリの保存先を解決し、`Storex` を介した入出力を統括するクラス。`CLAUDE.md` に記載の「Storage パターン」の中心的存在。ユーザー名単位でのファイル分離（マルチユーザー対応）もサポートする。

---

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `user` | `str \| None` | 正規化済みのユーザー名。空文字・空白のみは `None` に丸められる。 |
| `home_path` | `Path` | 実行環境のホームディレクトリ。 |
| `prog_name` | `str` | アプリケーション名（パス構築に使用）。 |
| `file_assoc` | `dict[str, dict[str, dict[str, Any]]]` | 種別（config/db）・ベース名ごとのファイル定義（`FILE_TYPE`/`EXT_NAME`/`PATH`/`VALUE`）。 |
| `directory_assoc` | `dict[str, dict[str, dict[str, Any]]]` | 種別ごとのディレクトリ定義。 |

---

## メソッド

### `__init__(prog_name: str, file_assoc: ..., user: str | None, directory_assoc: ... | None = None) -> None`

プログラム名と関連付け定義から保存先管理を初期化する。`user` は `Util.normalize_string`/`Util.is_empty` で正規化し、空なら `None` にする。初期化の最後に `set_ext_name()` を呼び拡張子情報を補完する。

### `set_ext_name() -> None`

`file_assoc` 内の各項目へ、`FILE_TYPE` から解決した拡張子（`Storex.get_ext_name`）を `EXT_NAME` として補完する。`KeyError` は握りつぶす。

### `prepare_config_file_and_db_file() -> None` / `prepare_config_file() -> None` / `prepare_db_file() -> None`

設定ファイル・DB ファイルの保存先 `Storex` をまとめて準備する（`prepare_file_level1()` への委譲）。

### `prepare_file_level1(kind: str) -> None` / `prepare_file_level2(kind: str, base_name: str) -> None`

指定種別の全ベース名、または単一のベース名について `Storex` を生成し `file_assoc[kind][base_name][PATH]` に登録する。`user` が設定されている場合はユーザー名をキーにしたネスト構造で保持する。

### `prepare_all_files(kind: str) -> None`

指定種別に属するすべてのファイル保存先を準備する（`prepare_file_level2()` のループ）。実装は `prepare_file_level1()` と完全に同一（コードの重複）であり、挙動に違いは無い。

### `prepare_config_directory_and_db_directory() -> None` / `prepare_config_directory() -> None` / `prepare_db_directory() -> None` / `prepare_directory(kind: str) -> None` / `prepare_all_directory() -> None`

設定用・DB 用のサブディレクトリをまとめて準備することを意図しているが、`prepare_sub_directory()`/`mkdir_db()` が `kind` を無視して常に `AppConfig.KIND_DB` を参照するため（詳細は「設計上の注意」）、`prepare_config_directory()` は意図通りに設定用ディレクトリを準備できない可能性がある。

### `prepare_sub_directory(kind: str, base_name: str) -> None`

単一のサブディレクトリを準備する（`mkdir_db()` を呼ぶだけ。`kind` は未使用）。

### `get_directory_assoc_from_config(base_name: str) -> OpResult[Any]` / `get_directory_assoc_from_db(base_name: str) -> OpResult[Any]`

設定用/DB 用ディレクトリ定義から対象項目を取得し、成功なら `OpResult.success`、`KeyError` なら `OpResult.from_exception` で返す。

### `load_file_db_all() -> None` / `load_file_db(base_name: str) -> None` / `load_file_config_all() -> None` / `load_file_config(base_name: str) -> None` / `load_file_all() -> None`

`file_assoc[kind][base_name][PATH]`（`Storex`）の `load()` を呼び、結果を `VALUE` に格納する。`user` の有無でネスト構造を切り替える。範囲（DB のみ/config のみ/全種別）によってメソッドが分かれている。

### `get_file_assoc_from_config(base_name: str) -> OpResult[Any]` / `get_file_assoc_from_db(base_name: str) -> OpResult[Any]`

読み込み済みの `VALUE` を取得する。`KeyError` 時は `OpResult.from_exception` で理由付きの失敗結果を返す。

### `get_file(user, kind, base_name, assoc) -> Storex | None`

`kind` に応じて `get_config_file()` または `get_db_file()` を呼び分ける。

### `get_config_file(user, key, assoc) -> Storex | None` / `get_db_file(user, key, assoc) -> Storex | None`

現在の OS（`sys.platform`）に応じて Windows 用/Unix 用のパス要素列を組み立て、`Storex` を生成する。

### `get_config_file_for_win` / `get_db_file_for_win` / `get_config_file_for_unix` / `get_db_file_for_unix`

各 OS・種別ごとのパス要素列（`list[str]`）を組み立てるヘルパー。Windows は `APPDATA`（設定）/`LOCALAPPDATA`（DB）環境変数、Unix は `~/.config`（設定）/`~/.local/share`（DB）を使う。`user` の有無でパスにユーザー名セグメントを挟むかどうかが変わる。

```
処理フロー（Windows 設定ファイルの例）:
  1. APPDATA 環境変数（未設定時は ~/AppData/Roaming）を取得
  2. ファイル名を "{base_name}{ext_name}" で組み立てる
  3. user が指定されていれば [top_dir, prog_name, user, file_name]、なければ [top_dir, prog_name, file_name] を返す
```

### `get_from_config(base_name: str, key: str) -> OpResult[Any]`

設定値辞書（`VALUE`）から指定キーの値を取り出す。`KeyError` 時は `OpResult.from_exception` を返すことを意図しているが、`self.user is None` の分岐では補足情報文字列の組み立て自体が `self.file_assoc[AppConfig.KIND_CONFIG][base_name]['path'].get_path()` を評価しており、元の `KeyError` の原因（`base_name` 欠落や `PATH` が `Storex` 化前の場合）によってはこの診断情報の構築中に別の `KeyError`/`AttributeError` が発生し、`OpResult` を返さずに例外が送出される場合がある。

### `output_config(key: str, data: dict[str, Any]) -> None` / `output_db(key: str, data: dict[str, Any]) -> None`

設定ファイル/DB ファイルへ辞書データを書き出す。`output_config()` は `VALUE` の更新と `Storex.output` の両方を行うが、`output_db()` は `Storex.output` のみを行い `VALUE` は更新しない（2 メソッドの実装は非対称）。

### `mkdir_db(key: str) -> None`

DB 用サブディレクトリを作成し、`directory_assoc[KIND_DB][key][PATH]` に登録する。作成先は Windows なら `LOCALAPPDATA`、それ以外なら `~/.local/share` 配下。

### `show(kind: str, base_name: str) -> None` / `show_config(base_name: str) -> None` / `show_db(base_name: str) -> None`

読み込み済みデータの内容をデバッグログへ出力する。

---

## 依存

| クラス/変数 | 用途 |
|-------------|------|
| `AppConfig` | 種別・キー名の定数（`KIND_CONFIG`/`KIND_DB`/`PATH`/`VALUE` 等） |
| `Storex` | 実ファイルの読み書き |
| `OpResult` | 例外を包んだ結果型での取得系メソッドの戻り値 |
| `Util` | ユーザー名の正規化・空判定 |
| `Loggerx` | デバッグログ出力 |

---

## 設計上の注意

- ほぼ全メソッドが `try/except KeyError: return None` のパターンで例外を握りつぶしており、設定ファイルの構造不整合が静かに無視される（呼び出し元は成功・失敗を区別できない）。一方で `get_*` 系の一部メソッドのみ `OpResult` を使って明示的にエラーを表現しており、エラーハンドリング方針がメソッドごとに一貫していない。
- `prepare_sub_directory()` は `kind` 引数を受け取るが使っておらず、`mkdir_db()` 内部で `AppConfig.KIND_DB` を直接参照している（設定用ディレクトリの準備にも同じ DB 用ロジックが使われる形跡があり、`KIND_CONFIG` 用の分岐が実装されていない可能性がある）。
- ネストした辞書（`file_assoc[kind][base_name][PATH][user]` 等）を直接操作するコードが多く、キー欠落時の挙動を把握するにはこの構造全体を追う必要がある。
