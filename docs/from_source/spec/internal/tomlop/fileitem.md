# FileItem — 内部仕様書

**ファイル**: `src/yklibpy/tomlop/fileitem.py`
**継承**: なし

## 概要

ファイルパスと `Storex` を束ねる薄いラッパー。ファイルパス表現の違い（文字列/`Path`/配列）を吸収し、拡張子からファイル種別を自動判定して `Storex` を生成する。

---

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `file_path` | `Path` | 確定したファイルパス。 |
| `file_type` | `str` | `AppConfig.get_file_type` で判定したファイル種別。 |
| `storex` | `Storex` | 実際の入出力を担う `Storex` インスタンス。 |

---

## メソッド

### `setup(file_type_dict: dict[str, str] = AppConfig.file_type_dict) -> None` (classmethod)

`Storex` で使うファイル種別定義を初期化する（`Storex.set_file_type_dict` に委譲）。

### `__init__(file: str | Path | list[str] | list[Path], data: Any = None) -> None`

入力値からファイルパスを確定し、対応する `Storex` を作る。

```
処理フロー:
  1. file がリストの場合、先頭要素を pop(0) する
     - 先頭要素が str の場合: Path 化して file_path とし、残りの要素は結合されず破棄される
     - 先頭要素が Path の場合: それを起点に残りの要素を順に結合して file_path を組み立てる
  2. file が文字列/Path 単体の場合はそのまま Path 化する
  3. AppConfig.get_file_type でファイル種別を判定し、None なら ValueError
  4. Storex(file_type, [file_path], data) を生成して保持する
```

**Raises**: `ValueError` — 拡張子からファイル種別を判定できない場合。

### `get_file_type(file_path: str | Path | None) -> str | None`

ファイルパスから判定したファイル種別を返す（`AppConfig.get_file_type` への委譲）。

### `set_data(data: dict[str, Any]) -> None`

内部 `Storex` に保持するデータを更新する。

### `output(data: Any = None) -> None`

データを現在のファイルパスへ出力する（`Storex.output` への委譲）。

### `get_name() -> str`

ファイル名だけを返す。

### `get_path() -> Path`

ファイルの完全パスを返す。

### `with_suffix(suffix: str) -> Path`

同じファイルパスに別拡張子を付けた `Path` を返す。

---

## 依存

| クラス/変数 | 用途 |
|-------------|------|
| `AppConfig` | ファイル種別判定・既定の拡張子辞書 |
| `Storex` | 実際のファイル入出力 |

---

## 設計上の注意

`__init__()` はリスト引数を `pop(0)` で破壊的に消費する（`Storex.__init__` と同様のパターン）。呼び出し元がリストを使い回す場合は副作用に注意。

`list[str]` を渡した場合、先頭要素のみが `file_path` となり 2 番目以降の要素は結合されずに破棄される（残りの要素が結合されるのは先頭要素が `Path` の場合のみ）。同じ `pop(0)` パターンを使う `Storex.__init__` は要素の型によらず一律に残りを結合するため、両者で挙動が異なる。
