# 外部仕様書 — `command_gh_user`

**対象クラス**: `yklibpy.command.command_gh_user.CommandGhUser`
**対応サブコマンド**: なし（ライブラリクラス）

本書は `docs/projects/def_ot_terms.md`（用語の定義）および `docs/projects/def_of_file_and_dir.md`（ディレクトリ/ファイル定義）を正とする方針で作成したが、本書作成時点で両ファイルは空である。そのため本書の記述はすべて「現行実装の挙動」に基づく。

## 未確定事項（本書作成にあたっての前提）

- 定義ドキュメント 2 件がいずれも空のため、定義由来の記述は存在せず、全記述を「現行実装の挙動」として扱った。異なる意図であればお知らせください。

## 1. 概要

GitHub CLI（`gh`）を使い、現在ログイン中のユーザー名を取得するコマンドクラス（`command` の基底クラスを継承）。

## 2. 使用する外部コマンド

| コマンド | 用途 |
|---------|------|
| `gh api user --jq ".login"` | 認証済みユーザーのログイン名を取得する |

## 3. 前提条件

1. `gh`（GitHub CLI）がインストールされ、`PATH` から起動できること。
2. `gh auth login` 等で GitHub への認証が済んでいること。

## 4. 公開インタフェース

### `run() -> str`

`gh api user --jq ".login"` を実行し、出力を正規化（空白除去）したユーザー名を返す。出力が空の場合は空文字を返す。

## 5. エラー処理・終了コード

| 事象 | 挙動 |
|------|------|
| `gh` が非 `0` で終了（未認証・ネットワークエラー等） | `subprocess.CalledProcessError` が呼び出し元へ伝播する |
| `gh` がインストールされていない | `FileNotFoundError` が呼び出し元へ伝播する |
| 出力が空 | 例外にせず空文字を返す |

ライブラリクラスであり単体のコマンドとして起動される経路は無いため、終了コードは規定しない。

## 6. 実装上の対応（参考）

本節は実装を拘束しない。

| 役割 | モジュール |
|------|-----------|
| ユーザー名取得 | `yklibpy.command.command_gh_user.CommandGhUser.run` |
| コマンド実行基盤 | `yklibpy.command.command.Command.run_command_simple` |
| 出力の正規化 | `yklibpy.common.util.Util.normalize_string` |
