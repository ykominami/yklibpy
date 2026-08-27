# Result — 内部仕様書

**ファイル**: `src/yklibpy/common/util.py`  
**継承**: なし（`Util` の入れ子クラス）

## 概要

URL 検証の成否、入力 URL、理由、解析済み URL を保持する可変データコンテナです。

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `success` | `bool` | 検証成否です。 |
| `url` | `str` | 検証対象 URL です。 |
| `reason` | `str` | 判定理由です。 |
| `parsed` | `ParseResult | None` | `urlparse` の結果です。 |

## メソッド

### `__init__(success: bool, url: str, reason: str, parsed: ParseResult | None) -> None`

URL 検証結果の各値を保持します。

## 依存

| クラス/変数 | 用途 |
|-------------|------|
| `urllib.parse.ParseResult` | URL 解析結果を表します。 |
| [`util_module.md`](util_module.md) | 同一モジュールの共通定義を参照します。 |
