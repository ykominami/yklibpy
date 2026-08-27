# 外部仕様書 — `ConfigPrepare`

**対象クラス**: `yklibpy.htmlparser.configprepare.ConfigPrepare`

## 未確定事項（本書作成にあたっての前提）

設定スキーマの正となる定義文書が欠落しています。以下のキー構造は現行実装の挙動です。異なる意図であればお知らせください。

## 1. 概要

設定辞書の既知キーへ直接アクセスする薄いラッパーです。

## 2. 設定キーと API

| API | 参照キー |
|---|---|
| `get(key)` | `<key>` |
| `get_command()` | `command` |
| `get_command_dir()` | `command.dir` |
| `get_category_config_file_extname()` | `category-config-file-extname` |
| `get_utility_category()` | `command.utility-category` |
| `get_utility_root()` | `command.utility-root` |
| `get_category()` | `category` |
| `get_htmlparser()` | `category.htmlparser` |

値の型・必須性・値域は検証しません。

## 3. エラー処理・終了コード

キー欠落時は `KeyError` が伝播します。CLI の終了コードは定義せず、未捕捉なら Python 標準の終了コード `1` です。

## 4. 実装上の対応（参考）

本節は実装を拘束しません。実装は `src/yklibpy/htmlparser/configprepare.py` です。
