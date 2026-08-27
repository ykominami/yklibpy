# 外部仕様書 — `Env`

**対象クラス**: `Env`  
**対応機能**: YAML 設定によるファイル探索

## 未確定事項（本書作成にあたっての前提）

- 正規の用語・ファイル定義2 文書が欠落し、`docs/projects` の代替候補も空です。YAML キーと配置は現行実装の挙動として記載します。異なる意図であればお知らせください。

## 1. 概要

YAML の `base_path`、パターン別 `dir`、`kind`、`files`、`mode` を使って対象ファイルを解決します。

## 2. 入出力仕様

`Env(config_path)` は UTF-8 YAML を読み、`base_path` の配列をパスへ変換します。`set_base_path(base_path)` は基準パスを指定した `Path` に置き換えます。`set_pattern(name)` で `assoc[name]` を選択し、`get_files()` は `kind: file` なら `files` 配列、その他なら指定ディレクトリ直下のファイルをソートして返します。`mode` 未指定時は `H3` です。`make_path()` は入力配列を変更します。

## 3. エラー処理・終了コード

| 事象 | 挙動 | 終了コード |
|---|---|---|
| 設定が空 | 空配列、`sequence=-1` | ライブラリのため該当なし |
| 必須キー欠落 | `KeyError` を伝播 | CLI 未捕捉時 `1` |
| `dir` 末尾が整数でない | `ValueError` を伝播 | CLI 未捕捉時 `1` |
| YAML/ファイル読み込み失敗 | PyYAML / OS 例外を伝播 | CLI 未捕捉時 `1` |

## 4. 実装上の対応（参考）

本節は実装を拘束しません。`src/yklibpy/common/env.py` が処理します。
