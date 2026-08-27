# UtilJson — 外部仕様書

## 概要

`yklibpy.common.util_json.UtilJson`

JSON の読み込みをまとめたクラスメソッド集。
エンコーディングは UTF-8 固定。

## パブリック API

### `load_file(file_name: str) -> Any`

JSON ファイルをパースして Python オブジェクトを返す。

**Raises**: `json.JSONDecodeError` — JSON として不正な場合。`FileNotFoundError` — ファイルが存在しない場合。

### `load_string(string: str) -> Any`

JSON 文字列をパースして Python オブジェクトへ変換する。

**Raises**: `json.JSONDecodeError` — JSON として不正な場合。

## 依存関係

- `json`（標準ライブラリ）
