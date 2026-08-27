# Info — 内部仕様書

**ファイル**: `src/yklibpy/common/info.py`  
**継承**: なし

## 概要

解析対象ファイル、BeautifulSoup DOM、追加・非追加件数を一つの処理コンテキストとして保持します。

---

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `file_path` | `Path` | 解析元ファイルのパスです。 |
| `name` | `str` | 対象を識別する名前です。 |
| `soup` | `BeautifulSoup` | 解析済み HTML DOM です。 |
| `append_count` | `int` | 追加対象となった件数です。 |
| `no_append_count` | `int` | 追加されなかった件数です。 |

---

## メソッド

### `__init__(file_path: Path, name: str, soup: BeautifulSoup, append_count: int, no_append_count: int) -> None`

入力情報と集計カウンターをそのまま保持します。

## 依存

| クラス/変数 | 用途 |
|-------------|------|
| `Path` | 入力ファイル位置を表します。 |
| `BeautifulSoup` | 解析済み HTML を保持します。 |
