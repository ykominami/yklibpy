# 外部仕様書 — `cli.__init__`

**対象**: CLI 基盤の公開 API と疎通確認エントリポイント  
**コマンド**: `yklibpy-cli-x` / `yklibpy-cli-y`

## 未確定事項

正とされる `docs/project/def_of_terms.md` と `docs/project/def_of_file_and_dir.md` は存在せず、代替候補 `docs/projects/def_of_file_and_dir.md` も空です。したがって、以下は現行実装から確認した挙動であり、用語・配置規則は未確定です。異なる意図であればお知らせください。

## 1. 概要

`xmain` は `Hello from yklibpy.cli!`、`ymain` は `Y Hello from yklibpy.cli!` を標準出力へ出し、同じ文言をデバッグログへ記録します。

## 2. コマンドライン構文

```text
yklibpy-cli-x
yklibpy-cli-y
```

引数・オプションはありません。余分な引数は検査されません。

## 3. エラー処理・終了コード

| 事象 | 挙動 | 終了コード |
|---|---|---:|
| 正常 | メッセージを出力 | 0 |
| ログまたは出力の未捕捉例外 | traceback を表示して終了 | 1（Python 標準） |

## 4. 実装上の対応（参考）

本節は実装を拘束しません。`src/yklibpy/cli/__init__.py` の `xmain` / `ymain` が担当します。
