# Scraper — 内部仕様書

## モジュール

`yklibpy.htmlparser.scraper`

## インスタンス変数

| 変数名 | 型 | 役割 |
|--------|----|------|
| `sequence` | `int` | 処理対象の世代番号（ディレクトリ名由来） |
| `links_assoc` | `dict[str, dict[str, Any]]` | 抽出済みリンクの連想配列（キー = URL 等） |
| `info` | `dict[str, Info]` | ファイル名をキーとする解析済み `Info` キャッシュ |
| `append_count` | `int` | 新規追加数カウンタ |
| `no_append_count` | `int` | 重複スキップ数カウンタ |

## クラスメソッドの実装詳細

### `_to_assoc(title, url, sequence) -> dict`

```python
{"title": title, "url": url, "sequence_array": set([sequence])}
```

`sequence_array` は `set` のため同一リンクが複数ファイルに出現したとき重複なく記録できる。

### `_add_assoc(links_assoc, key, sequence, value_dict) -> bool`

- `key` が未登録なら `value_dict` を追加して `True` を返す
- 登録済みなら `link["sequence_array"].add(sequence)` だけ実行して `False` を返す
- 重複時に `ValueError` を送出するコードはコメントアウト済み

## インスタンスメソッドの実装詳細

### `_parse_html_file(file_path) -> Optional[BeautifulSoup]`

1. `Util.detect_encoding(file_path)` でエンコーディングを推定
2. `BeautifulSoup(f, "html5lib")` でパース（lxml ではなく html5lib を使用）
3. `FileNotFoundError` と一般 `Exception` をそれぞれ捕捉してログ出力後 `None` を返す

### `_extract_links_assoc_from_info(info) -> dict`

- `self.scrape(info)` を呼んで副作用（`links_assoc` への追記）を起動する
- 実行後 `self.links_assoc` を返す

### `get_links_assoc_from_html(file_path) -> dict`

- `file_path.name` が `self.info` にキャッシュ済みなら空辞書を返す（同一ファイルの二重処理防止）
- 未処理なら `_parse_html_file` → `Info` 生成 → `_extract_links_assoc_from_info` の順に処理する

### `scrape(info) -> None`

- 基底実装は `pass`。サブクラスで `self.links_assoc` へリンクを追記する処理を実装する

## 依存関係

- `pathlib.Path`, `typing`（標準ライブラリ）
- `bs4.BeautifulSoup`
- `yklibpy.common.info.Info`
- `yklibpy.common.loggerx.Loggerx`
- `yklibpy.common.util.Util`
