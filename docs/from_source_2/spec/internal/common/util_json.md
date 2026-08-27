# UtilJson — 内部仕様書

**ファイル**: `src/yklibpy/common/util_json.py`  
**継承**: なし

## 概要

JSON ファイルまたは文字列を Python オブジェクトへ変換する薄いラッパーです。

---

## メソッド

### `load_file(file_name: str) -> Any` (classmethod)

UTF-8 の JSON ファイルを開いてパース結果を返します。

**Raises**: `OSError` — ファイルを開けない場合。  
**Raises**: `json.JSONDecodeError` — JSON が不正な場合。

### `load_string(string: str) -> Any` (classmethod)

JSON 文字列をパースして返します。

**Raises**: `json.JSONDecodeError` — JSON が不正な場合。

## 依存

| クラス/変数 | 用途 |
|-------------|------|
| `json` | JSON のデコードを担当します。 |
