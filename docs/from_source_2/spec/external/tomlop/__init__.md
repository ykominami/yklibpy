# 外部仕様書 — `tomlop.__init__`

**対象**: TOML/YAML 操作 API と疎通確認  
**コマンド**: `yklibpy-tomlop-x` / `yklibpy-tomlop-y`

## 未確定事項

正とされる2 定義文書は欠落し、代替候補も空です。以下は現行実装です。異なる意図であればお知らせください。

## 1. コマンドライン構文

```text
yklibpy-tomlop-x
yklibpy-tomlop-y
```

`x` は挨拶を標準出力とログへ、`y` はログだけへ出します。引数は検査されません。

## 2. エラー処理・終了コード

正常時は0です。未捕捉例外はPython標準により1です。

## 3. 実装上の対応（参考）

本節は実装を拘束しません。`src/yklibpy/tomlop/__init__.py` が担当します。
