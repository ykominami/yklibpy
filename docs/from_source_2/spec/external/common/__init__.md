# 外部仕様書 — `common`

**対象**: `yklibpy.common` 公開 API

## 未確定事項（本書作成にあたっての前提）

- 正とされる `docs/project/def_of_terms.md` と `docs/project/def_of_file_and_dir.md` は存在しません。代替候補 `docs/projects/def_of_file_and_dir.md` と `def_ot_terms.md` も空です。このため用語・配置の定義適合性は未確認です。異なる意図であればお知らせください。

## 1. 概要

共通ユーティリティを `yklibpy.common` から公開し、`xmain()` / `ymain()` で疎通確認ログを出します。

## 2. 公開 API

`Env`、`Info`、`OpResult`、`SafeDict`、`Timex`、`Util`、`UtilJson`、`UtilYaml` を `__all__` で公開します。`Loggerx` は属性として参照できますが `__all__` の対象外です。

## 3. エラー処理・終了コード

| 事象 | 挙動 | 終了コード |
|---|---|---|
| import / 疎通確認成功 | ログを出して正常終了 | `0` |
| 未捕捉例外 | 呼び出し元へ伝播 | CLI 直接実行時は Python 標準の `1` |

## 4. 実装上の対応（参考）

本節は実装を拘束しません。`src/yklibpy/common/__init__.py` が再公開と疎通確認を担当します。
