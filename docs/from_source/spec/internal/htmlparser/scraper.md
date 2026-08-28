# Scraper — 内部仕様書

**ファイル**: `src/yklibpy/htmlparser/scraper.py`
**継承**: なし

## 概要

HTML からリンク連想配列を構築するスクレイパーの基底クラス。ファイル読み込み・エンコーディング検出・重複排除の共通ロジックを提供し、サイト固有の抽出処理は `scrape()` をオーバーライドするサブクラスに委ねる（`CLAUDE.md` に記載の「Scraper パターン」の核）。

---

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `sequence` | `int` | （本クラス内では未使用気味の）処理対象の連番（出現回数の記録用に `_to_assoc()`/`_add_assoc()` へ渡す想定）。 |
| `links_assoc` | `dict[str, dict[str, Any]]` | 抽出結果のリンク連想配列。 |
| `info` | `dict[str, Info]` | 処理済みファイル名をキーにした `Info` キャッシュ。 |
| `append_count` | `int` | （未使用気味の）追加件数カウンタ。 |
| `no_append_count` | `int` | （未使用気味の）非追加件数カウンタ。 |

---

## メソッド

### `__init__(sequence: int) -> None`

抽出結果と中間情報を保持する内部状態を初期化する。

### `_to_assoc(title: str, url: str, sequence: int) -> dict[str, Any]` (classmethod)

タイトルと URL から標準的なリンク辞書（`title`/`url`/`sequence_array`）を組み立てる。`sequence_array` は `{sequence}` を要素に持つ `set`。

### `_add_assoc(links_assoc: dict[str, dict[str, Any]], key: str, sequence: int, value_dict: dict[str, Any]) -> bool` (classmethod)

キー単位でリンク辞書を追加し、重複時は `sequence_array` へ出現回数情報のみ追加する。

**Returns**: 新規追加なら `True`、既存キーへの追記なら `False`。

### `_extract_links_assoc_from_info(info: Info) -> Dict[str, Dict[str, Any]]`

`Info` を元に `scrape()` を実行し、結果の `links_assoc` を返す。

### `_parse_html_file(file_path: Path) -> Optional[BeautifulSoup]`

HTML ファイルを読み込み、`BeautifulSoup`（`html5lib` パーサ）へ変換する。

```
処理フロー:
  1. Util.detect_encoding でエンコーディングを推定（失敗時はログ出力して None を返す）
  2. 推定エンコーディングでファイルを開き BeautifulSoup(f, "html5lib") を生成
  3. ファイル未検出・その他の例外はいずれもログ出力のうえ None を返す
```

### `scrape(info: Info) -> None`

実際の抽出処理を行う拡張ポイント。基底クラスでは何もしない（`pass`）。サブクラスでオーバーライドする。

### `get_links_assoc_from_html(file_path: Path) -> Dict[str, Dict[str, Any]]`

HTML ファイルを解析し、抽出結果の連想配列を返す。同名ファイルが既に `self.info` にキャッシュ済みであれば再解析せず空の `{}` を返す。

---

## 依存

| クラス/変数 | 用途 |
|-------------|------|
| `Info` | 解析結果と DOM の保持 |
| `Util` | エンコーディング検出（`detect_encoding`） |
| `Loggerx` | エラーログ出力 |
| `bs4.BeautifulSoup` | HTML パース（`html5lib` パーサ使用、`lxml` は不使用） |

---

## 設計上の注意

- サイト固有スクレイパーはこのクラスを継承し `scrape()` を実装する想定（`CLAUDE.md` 記載のパターン）だが、本ファイル単体にはサブクラス例が含まれない。
- `get_links_assoc_from_html()` は「同名ファイルを既に処理済みなら再処理しない」というキャッシュ制御を行うが、同名で内容が異なる複数ファイルを扱うケースでは意図せず処理がスキップされる可能性がある。
- `_parse_html_file()` の外側 `try`/`except FileNotFoundError`/`except Exception` は、内側の 2 つの `try` ブロックがいずれも `except Exception` で先に例外を捕捉して `None` を返すため、実質的に到達不能なコードになっている。
