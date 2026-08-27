# 外部仕様書 — `command.__init__`

**対象**: コマンド API と疎通確認  
**コマンド**: `yklibpy-command-x` / `yklibpy-command-y`

## 未確定事項

正とされる2 定義文書は欠落し、代替候補も空です。以下は現行実装の挙動です。異なる意図であればお知らせください。

## 1. コマンドライン構文

```text
yklibpy-command-x
yklibpy-command-y
```

前者は `Hello from yklibpy.command!`、後者は `Y Hello from yklibpy.command!` を標準出力とデバッグログへ出します。引数は検査されません。

## 2. エラー処理・終了コード

| 事象 | 挙動 | 終了コード |
|---|---|---:|
| 正常 | メッセージを出力 | 0 |
| 未捕捉例外 | traceback を表示 | 1 |

## 3. 実装上の対応（参考）

本節は実装を拘束しません。`src/yklibpy/command/__init__.py` が担当し、`Command`、`CommandGhUser`、`FetchCount` も公開します。
