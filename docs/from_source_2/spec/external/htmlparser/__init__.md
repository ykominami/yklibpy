# 外部仕様書 — `htmlparser`

**対象**: `yklibpy.htmlparser` 公開 API

## 未確定事項（本書作成にあたっての前提）

`docs/project/def_of_terms.md` と `docs/project/def_of_file_and_dir.md` は存在せず、`docs/projects/def_of_file_and_dir.md` にも有効な定義がないため、用語・配置・値形式は現行実装を根拠とします。異なる意図であればお知らせください。

## 1. 概要

HTML の解析、リンク抽出、進捗値、関連ファイル準備を行うライブラリ API を公開します。

## 2. 公開 API

| 名前 | 用途 |
|---|---|
| `App` | 複数 HTML の処理を統括します。 |
| `Scraper` | HTML 読み込みとリンク抽出の基底機能です。 |
| `Preparex` | ディレクトリ準備とファイル列挙を行います。 |
| `Progress` | 進捗値を保持します。 |
| `HtmlOp` | DOM からアンカー情報を取得します。 |

`xmain()` と `ymain()` はログへ疎通確認メッセージを出力しますが、`__all__` には含まれません。

## 3. エラー処理・終了コード

本モジュールは CLI の終了コードを定義しません。インポートエラーまたは公開関数から伝播した未捕捉例外でプロセスが終了する場合、Python 標準の終了コード `1` です。

## 4. 実装上の対応（参考）

本節は実装を拘束しません。`src/yklibpy/htmlparser/__init__.py` が公開名を再エクスポートします。
