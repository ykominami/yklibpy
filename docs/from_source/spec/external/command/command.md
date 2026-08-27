# 外部仕様書 — `command`

**対象クラス**: `yklibpy.command.command.Command`
**対応サブコマンド**: なし（ライブラリクラス・継承用基底クラス）

本書は `docs/projects/def_ot_terms.md`（用語の定義）および `docs/projects/def_of_file_and_dir.md`（ディレクトリ/ファイル定義）を正とする方針で作成したが、本書作成時点で両ファイルは空である。そのため本書の記述はすべて「現行実装の挙動」に基づく。

## 未確定事項（本書作成にあたっての前提）

- 定義ドキュメント 2 件がいずれも空のため、取得履歴 DB のフォーマットも定義由来ではなく現行実装の挙動として記載した。異なる意図であればお知らせください。

## 1. 概要

外部コマンド（サブプロセス）の実行と、取得回数（実行世代）の管理を提供する基底クラス。サービス固有のコマンド実行クラスの基底として使う。

## 2. 公開インタフェース

### `run_command(command, shell=False, encoding="utf-8", timeout=None) -> tuple[str, int]`

コマンドを実行し、標準出力と終了コードのタプルを返す。標準出力に指定エンコーディングとして不正なバイト列が含まれていても例外にせず、置換文字（U+FFFD）に置き換えて継続する。

### `run_command_simple(command, shell=False) -> str`

終了コードを検査しながらコマンドを実行し、標準出力を返す。コマンドが非 `0` で終了した場合は例外になる（§5）。

### `run_command_simple_with_count(appstore, command, shell=False, *, force=False, verbose=False) -> str`

取得回数に応じてコマンド実行を制御し、必要時のみ出力を返す。

```
処理フロー:
  1. 実行世代番号を採番し、取得履歴 DB へ記録する（get_next_count）
  2. 世代番号が 1（初回）または force=True のときだけ実際にコマンドを実行し出力を得る
     （それ以外は空文字を返す）
  3. verbose=True なら取得履歴 DB の内容をデバッグログへ出力する
```

### `get_next_count(appstore: AppStore) -> int`

保存済みの実行履歴から次の実行世代番号を採番し、タイムスタンプ付きで DB へ書き戻したうえで返す。履歴が無い場合は `1` から開始する。

### 取得履歴 DB のフォーマット（現行実装の挙動）

保存先は `appstore` が解決する DB ファイル（ベース名 `fetch`、YAML 形式）。内容は連番文字列をキー、JST の ISO 8601 タイムスタンプを値とする辞書。

```yaml
"1": "2026-07-14T12:34:56.789012+09:00"
"2": "2026-07-14T13:00:00.000000+09:00"
```

## 3. 前提条件

1. `run_command_simple_with_count()`/`get_next_count()` を使う場合、渡す保存先管理オブジェクト側で `fetch` DB の保存先準備と読み込みが済んでいること。**未ロードの場合は「履歴なし」と判定され、既存の世代履歴がファイルごと上書きされて失われる**（現行実装の挙動）。

## 4. 制約（現行実装の挙動）

- `run_command_simple_with_count()` は、コマンドを実際に実行しない場合でも履歴カウントを進めて DB へ書き戻す。呼び出しのたびに世代番号が増える。
- 履歴辞書のキーのうち数値化できないものは無視され、数値化できるキーが 1 つも無い場合は次番号 `1` として扱われる。

## 5. エラー処理・終了コード

| 事象 | 挙動 |
|------|------|
| `run_command()` で `timeout` を超過 | `subprocess.TimeoutExpired` が呼び出し元へ伝播する（出力・タイムアウト値を詰め直した新規例外。出力が無い場合は空文字、タイムアウト値未指定は `0.0`） |
| `run_command()` でその他のサブプロセスエラー | `subprocess.SubprocessError` がそのまま再送出される |
| `run_command_simple()` でコマンドが非 `0` 終了 | ログ出力のうえ `subprocess.CalledProcessError` が呼び出し元へ伝播する |
| 実行対象コマンドが存在しない | `FileNotFoundError` が呼び出し元へ伝播する（`shell=False` の場合） |

ライブラリクラスであり単体のコマンドとして起動される経路は無いため、終了コードは規定しない。

## 6. 実装上の対応（参考）

本節は実装を拘束しない。

| 役割 | モジュール |
|------|-----------|
| コマンド実行・世代管理 | `yklibpy.command.command.Command` |
| 取得履歴 DB の読み書き | `yklibpy.db.appstore.AppStore` |
| タイムスタンプ生成 | `yklibpy.common.timex.Timex` |
| ベース名・種別の定数 | `yklibpy.config.appconfig.AppConfig` |
