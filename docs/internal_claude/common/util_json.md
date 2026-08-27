# UtilJson — 内部仕様書

## モジュール

`yklibpy.common.util_json`

## 実装詳細

### `load_file(file_name: str) -> Any`

- `open(file_name, "r", encoding="utf-8")` でファイルを開き `json.load` でパースする
- 引数が `str` のみで `Path` を受け付けない点に注意（`open` は内部で変換するため実害はないが型上の制約がある）

### `load_string(string: str) -> Any`

- `json.loads(string)` の薄いラッパー

## 依存関係

- `json`（標準ライブラリ）
