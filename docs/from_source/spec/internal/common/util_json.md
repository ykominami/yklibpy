# UtilJson — 内部仕様書

**ファイル**: `src/yklibpy/common/util_json.py`
**継承**: なし

## 概要

JSON の読み込み処理（ファイル/文字列）をまとめた補助クラス。状態を持たず、すべて `classmethod` として提供する。

---

## メソッド

### `load_file(file_name: str) -> Any` (classmethod)

JSON ファイルを UTF-8 で読み込み、パース結果を返す。

### `load_string(string: str) -> Any` (classmethod)

JSON 文字列をパースして Python オブジェクトへ変換する。

---

## 依存

なし（標準の `json` のみ）。

---

## 設計上の注意

書き込み側の処理は持たない（読み込み専用）。書き込みが必要な場合は `Storex`/`FileItem` を使う。
