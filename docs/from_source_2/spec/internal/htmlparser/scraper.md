# Scraper — 内部仕様書

**ファイル**: `src/yklibpy/htmlparser/scraper.py`  
**継承**: なし

## 概要

HTML ファイルを BeautifulSoup へ変換し、ファイルごとの `Info` を介してリンク辞書を構築するスクレイパー基底クラスである。具体的な抽出規則は `scrape` のオーバーライドへ委譲する。

---

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `sequence` | `int` | 抽出元の系列番号。 |
| `links_assoc` | `dict[str, dict[str, Any]]` | 抽出済みリンク辞書。 |
| `info` | `dict[str, Info]` | ファイル名別の解析情報キャッシュ。 |
| `append_count` | `int` | 追加件数用カウンター。基底クラスでは未更新。 |
| `no_append_count` | `int` | 非追加件数用カウンター。基底クラスでは未更新。 |

---

## メソッド

### `__init__(sequence: int) -> None`

系列番号を保持し、抽出結果・解析情報・カウンターを初期化する。

### `_to_assoc(title: str, url: str, sequence: int) -> dict[str, Any]` (classmethod)

タイトル、URL、系列番号集合を持つ標準リンク辞書を生成する。

### `_add_assoc(links_assoc: dict[str, dict[str, Any]], key: str, sequence: int, value_dict: dict[str, Any]) -> bool` (classmethod)

未登録キーなら値を追加し、登録済みなら既存値の `sequence_array` に系列番号を加える。

**Returns**: 新規追加時は `True`、重複更新時は `False`。  
**Raises**: `KeyError` / `AttributeError` — 既存値に集合形式の `sequence_array` がない場合。

### `_extract_links_assoc_from_info(info: Info) -> Dict[str, Dict[str, Any]]`

`scrape` を実行し、インスタンスが保持するリンク辞書を返す。

### `_parse_html_file(file_path: Path) -> Optional[BeautifulSoup]`

文字コードを検出して HTML を読み込み、`html5lib` パーサーの BeautifulSoup オブジェクトを返す。

処理フロー:

1. `Util.detect_encoding` で文字コードを検出する。
2. 検出した文字コードでファイルを開く。
3. `BeautifulSoup(..., "html5lib")` で解析して返す。
4. いずれかの処理に失敗した場合はエラーを記録して `None` を返す。

### `scrape(info: Info) -> None`

具体的な抽出処理を実装する拡張ポイント。基底実装は何もしない。

### `get_links_assoc_from_html(file_path: Path) -> Dict[str, Dict[str, Any]]`

未処理のファイルを解析し、`Info` を作って抽出処理へ渡す。

処理フロー:

1. ファイル名が `info` キャッシュにないことを確認する。
2. HTML を解析し、成功時に `Info` を生成してキャッシュする。
3. `scrape` を介してリンク情報を抽出し、結果を返す。

## 依存

| クラス/変数 | 用途 |
|-------------|------|
| `BeautifulSoup` | HTML DOM の構築。 |
| `Info` | ファイルと DOM を抽出処理へ渡す中間情報。 |
| `Util.detect_encoding` | 入力ファイルの文字コード検出。 |
| `Loggerx` | 読み込み・解析失敗の記録。 |

## 設計上の注意

キャッシュキーはフルパスでなく `file_path.name` であるため、別ディレクトリの同名ファイルは同一と扱われる。例外は原則としてログ記録後に `None` へ変換され、呼び出し側から原因を型で判別できない。
