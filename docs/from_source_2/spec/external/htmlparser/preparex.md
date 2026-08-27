# 外部仕様書 — `Preparex`

**対象クラス**: `yklibpy.htmlparser.Preparex`

## 未確定事項（本書作成にあたっての前提）

配置・命名の定義2 文書が欠落しているため、以下は現行実装の挙動です。異なる意図であればお知らせください。

## 1. 概要・作成物

`Preparex(top_dir, category, config_parent_dir, assoc)` は `<top_dir>/<assoc.command.dir>/` と `<top_dir>/<category>/` を再帰作成します。設定には `command.dir`、`command.utility-category`、`category-config-file-extname` が必要です。

`list_files_containing` は指定ディレクトリ直下のみから名前部分一致の通常ファイルを列挙し、不正なディレクトリには空リストを返します。他の `list_*` API は同処理の用途別ラッパーです。

## 2. エラー処理・終了コード

キー欠落は `KeyError`、作成失敗は `OSError`、探索例外は伝播します。不正な列挙先では異常終了しません。CLI 終了コードは定義せず、未捕捉なら `1` です。

## 3. 実装上の対応（参考）

本節は実装を拘束しません。`src/yklibpy/htmlparser/preparex.py` に対応します。
