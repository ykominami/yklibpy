# 外部仕様書 — `db.__init__`

**対象**: YAML DB ファクトリと疎通確認 CLI  
**コマンド**: `yklibpy-db-main` / `yklibpy-db-x` / `yklibpy-db-y`

## 未確定事項

正とされる2 定義文書は欠落し、代替候補 `docs/projects/def_of_file_and_dir.md` も空です。以下は現行実装の挙動です。異なる意図であればお知らせください。

## 1. コマンド仕様

`yklibpy-db-main` はカレントディレクトリの `db.yml` をロードし、メモリ上で `name: John` を設定しますが保存しません。`db-x` / `db-y` は各挨拶を出力します。引数は検査されません。

## 2. ライブラリ API

`get_or_create_db(kind, fname)` は `kind` が大文字小文字を問わず `yaml` の場合だけ `DbYaml` を返し、それ以外は `None` を返します。

## 3. エラー処理・終了コード

| 事象 | 挙動 | 終了コード |
|---|---|---:|
| 正常 | DBをロードまたは挨拶を出力 | 0 |
| 未対応DB種別 | ファクトリは `None` | API自体は異常終了しない |
| 未捕捉I/O・YAML例外 | 伝播 | CLIでは1 |

## 4. 実装上の対応（参考）

本節は実装を拘束しません。`src/yklibpy/db/__init__.py` が担当します。
