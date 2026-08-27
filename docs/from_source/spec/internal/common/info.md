# Info — 内部仕様書

**ファイル**: `src/yklibpy/common/info.py`
**継承**: なし

## 概要

解析済み HTML（`BeautifulSoup`）と件数カウンタ用のフィールドをひとまとめに保持するだけの単純なデータコンテナ。ただし現状のコードでは件数カウンタは常に `0` で生成され、事後に更新されることも無い（詳細は「設計上の注意」）。

---

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `file_path` | `Path` | 解析対象だった HTML ファイルのパス。 |
| `name` | `str` | ファイル名。 |
| `soup` | `BeautifulSoup` | 解析済みの DOM。 |
| `append_count` | `int` | 追加件数を表す想定のフィールド。ただし現状は唯一の生成箇所で常に `0` を渡されており、`Info` に値を更新するメソッドも存在しないため実質未使用（詳細は「設計上の注意」）。 |
| `no_append_count` | `int` | 追加されなかった件数を表す想定のフィールド。ただし現状は唯一の生成箇所で常に `0` を渡されており、`Info` に値を更新するメソッドも存在しないため実質未使用（詳細は「設計上の注意」）。 |

---

## メソッド

### `__init__(file_path: Path, name: str, soup: BeautifulSoup, append_count: int, no_append_count: int) -> None`

入力ファイルと DOM、件数カウンタを初期化する。単純な値の保持のみを行う。

---

## 依存

| クラス/変数 | 用途 |
|-------------|------|
| `bs4.BeautifulSoup` | 保持する DOM の型 |

---

## 設計上の注意

`Scraper.get_links_assoc_from_html` から生成され、`self.info` に保存されるキャッシュ用オブジェクトとして使われる。唯一の生成箇所（`scraper.py` の `Info(file_path, file_path.name, soup, 0, 0)`）では `append_count`/`no_append_count` が常に `0` で渡されており、`Info` 自体に値を更新するメソッドも存在しないため、現状の呼び出し経路ではこの 2 つのフィールドは常に `0` のまま変化しない。
