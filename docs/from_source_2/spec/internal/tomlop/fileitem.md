# FileItem — 内部仕様書

**ファイル**: `src/yklibpy/tomlop/fileitem.py`  
**継承**: なし

## 概要

単一ファイルのパス、判定済みファイル種別、`Storex` を束ね、変換処理から簡潔に入出力できるようにする。

---

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `file_path` | `Path` | 確定済みファイルパス。 |
| `file_type` | `str` | `AppConfig` が判定した形式。 |
| `storex` | `Storex` | 入出力の委譲先。 |

---

## メソッド

### `setup(file_type_dict=AppConfig.file_type_dict) -> None` (classmethod)

`Storex` の共有拡張子対応表を設定する。

### `__init__(file, data=None) -> None`

入力からパスを構築し、形式を判定して `Storex` を生成する。

1. リストなら先頭要素を取り出し、残りの要素をパスへ連結する。単一値なら直接 `Path` 化する。
2. `AppConfig.get_file_type` で形式を判定し、未対応なら `ValueError` を送出する。
3. パスと初期データを指定して `Storex` を生成する。

### `get_file_type(file_path) -> str | None`

任意のパスを文字列化し、`AppConfig` の形式判定結果を返す。

### `set_data(data) -> None` / `output(data=None) -> None`

保持データの更新またはファイル出力を `Storex` へ委譲する。

### `get_name() -> str` / `get_path() -> Path`

ファイル名または完全パスを `Storex` から取得する。

### `with_suffix(suffix: str) -> Path`

保持パスの拡張子を差し替えた新しい `Path` を返す。

---

## 依存

| クラス/変数 | 用途 |
|-------------|------|
| `AppConfig` | ファイル形式の判定と既定対応表。 |
| `Storex` | データ保持と入出力。 |
| `Path` | パス構築。 |

## 設計上の注意

リスト入力時は `pop(0)` により呼び出し元のリストを破壊する。さらに先頭要素が文字列の場合、残りのパス要素を連結しないインデント構造になっており、複数の文字列要素からなるパスが欠落する。`Storex` へ渡すリストも同様に破壊されるが一時値である。
