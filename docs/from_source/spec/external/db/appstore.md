# 外部仕様書 — `appstore`

**対象クラス**: `yklibpy.db.appstore.AppStore`
**対応サブコマンド**: なし（ライブラリクラス）

本書は `docs/projects/def_ot_terms.md`（用語の定義）および `docs/projects/def_of_file_and_dir.md`（ディレクトリ/ファイル定義）を正とする方針で作成したが、本書作成時点で両ファイルは空である。そのため本書の記述（保存先レイアウトを含む）はすべて「現行実装の挙動」に基づく。

## 未確定事項（本書作成にあたっての前提）

- 定義ドキュメント 2 件がいずれも空のため、保存先ディレクトリレイアウトは定義由来ではなく現行実装の挙動として記載した。異なる意図であればお知らせください。

## 1. 概要

OS ごとの規約（Windows: `APPDATA`/`LOCALAPPDATA`、Unix: XDG 相当のパス）に従って設定ファイル・DB ファイル・ディレクトリの保存先を解決し、ストレージラッパー（`storex` 参照）を介した入出力を統括するクラス。ユーザー名単位でのファイル分離（マルチユーザー対応）もサポートする。

## 2. 公開インタフェース

### 生成

```python
AppStore(prog_name: str, file_assoc: dict, user: str | None, directory_assoc: dict | None = None)
```

- `prog_name` — アプリケーション名（保存先パスのセグメントになる）。
- `file_assoc` — 種別（`config`/`db`）・ベース名ごとのファイル定義。`appconfig` の初期定義（またはその拡張）を渡す。**渡した辞書はコピーされず内部で書き換えられる**（拡張子の補完等）ため、複数インスタンスで同じ辞書を共有する場合は事前に深いコピーを取ること。
- `user` — ユーザー名。空文字・空白のみは `None` に正規化される。
- `directory_assoc` — 種別ごとのディレクトリ定義（省略時は空辞書）。

### 保存先レイアウト（現行実装の挙動）

```
# Windows（環境変数未設定時は ~/AppData/Roaming・~/AppData/Local へフォールバック）
%APPDATA%/<prog_name>/[<user>/]<base_name><ext_name>        # 設定ファイル
%LOCALAPPDATA%/<prog_name>/[<user>/]<base_name><ext_name>   # DB ファイル
%LOCALAPPDATA%/<prog_name>/<key>/                            # DB 用サブディレクトリ

# Unix 系
~/.config/<prog_name>/[<user>/]<base_name><ext_name>        # 設定ファイル
~/.local/share/<prog_name>/[<user>/]<base_name><ext_name>   # DB ファイル
~/.local/share/<prog_name>/<key>/                            # DB 用サブディレクトリ
```

`[<user>/]` はユーザー名指定時のみ挟まる。`<ext_name>` はファイル種別から解決した拡張子（YAML なら `.yml` 等）。

### 準備系メソッド

| メソッド | 説明 |
|---------|------|
| `prepare_config_file_and_db_file()` / `prepare_config_file()` / `prepare_db_file()` | 種別ごとの全ベース名について保存先ストレージオブジェクトを生成・登録する |
| `prepare_all_files(kind)` / `prepare_file_level1(kind)` / `prepare_file_level2(kind, base_name)` | 範囲を絞った同上の処理 |
| `prepare_config_directory_and_db_directory()` ほかディレクトリ準備系 | 登録済みディレクトリ定義のサブディレクトリを作成する（§4 の制約あり） |

### 入出力系メソッド

| メソッド | 説明 |
|---------|------|
| `load_file_db(base_name)` / `load_file_config(base_name)` / `load_file_db_all()` / `load_file_config_all()` / `load_file_all()` | 保存先ファイルを読み込み、読み込み済み値として内部に保持する |
| `get_file_assoc_from_db(base_name)` / `get_file_assoc_from_config(base_name)` -> `OpResult[Any]` | **読み込み済みの値**を結果型（`opresult` 参照）で返す。未ロードの場合は失敗（`ok=False`）になる |
| `get_from_config(base_name, key)` -> `OpResult[Any]` | 設定値辞書から指定キーの値を取り出す |
| `get_directory_assoc_from_config(base_name)` / `get_directory_assoc_from_db(base_name)` -> `OpResult[Any]` | ディレクトリ定義から対象項目を返す |
| `output_config(key, data)` / `output_db(key, data)` | 設定/DB ファイルへ辞書データを書き出す |
| `mkdir_db(key)` | DB 用サブディレクトリを作成し、ディレクトリ定義へ登録する |
| `show(kind, base_name)` / `show_config(base_name)` / `show_db(base_name)` | 読み込み済みデータの内容をデバッグログへ出力する |

## 3. 前提条件

1. `file_assoc` の各エントリにはファイル種別が設定されており、拡張子解決の対応辞書（`storex` 参照の `set_file_type_dict()`）が設定済みであること（未設定の場合、拡張子補完は静かにスキップされる）。
2. 取得系（`get_file_assoc_from_*`）を使う前に、対応する `load_file_*` で読み込みを済ませておくこと。DB ファイルが存在していても、未ロードなら取得は失敗（`ok=False`）になる。
3. ファイル入出力の前に `prepare_*` 系で保存先ストレージオブジェクトを登録しておくこと。

## 4. 制約（現行実装の挙動）

- ほとんどのメソッドは内部のキー欠落（`KeyError`）を握りつぶして `None` を返すため、呼び出し元は成功と失敗を区別できない。明示的に失敗を返すのは結果型を返す取得系のみ。
- ディレクトリ準備系は種別引数に関わらず常に DB 用のロジック（`mkdir_db()`）で処理されるため、設定用ディレクトリを DB 用と別の場所に準備することはできない。
- `output_config()` は内部の読み込み済み値も更新するが、`output_db()` はファイル書き出しのみを行う（両者は非対称）。
- `get_from_config()` はユーザー名未指定時の失敗診断文字列の組み立て中に内部構造を参照するため、失敗の原因によっては結果型を返さず `KeyError`/`AttributeError` がそのまま送出される場合がある。

## 5. エラー処理・終了コード

| 事象 | 挙動 |
|------|------|
| 準備系・読み込み系・出力系での内部キー欠落 | 例外を伝播せず `None` を返して終了する（ログにも出ない） |
| 取得系（結果型を返すメソッド）でのキー欠落 | `ok=False` の結果を返す（例外は伝播しない。ただし `get_from_config()` は上記 §4 の例外あり） |
| ファイル書き込み失敗（`output_*`） | `OSError` 等が呼び出し元へ伝播する |

ライブラリクラスであり単体のコマンドとして起動される経路は無いため、終了コードは規定しない。

## 6. 実装上の対応（参考）

本節は実装を拘束しない。

| 役割 | モジュール |
|------|-----------|
| 保存先解決・入出力統括 | `yklibpy.db.appstore.AppStore` |
| 実ファイルの読み書き | `yklibpy.db.storex.Storex` |
| 種別・キー名の定数 | `yklibpy.config.appconfig.AppConfig` |
| 取得系の結果型 | `yklibpy.common.opresult.OpResult` |
