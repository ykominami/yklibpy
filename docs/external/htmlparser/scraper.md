# Scraper — 外部仕様書

## 概要

`yklibpy.htmlparser.scraper.Scraper`

HTML ファイルからリンク連想配列を構築するスクレイパーの基底クラス。
サイト固有の抽出ロジックはサブクラスで `scrape` をオーバーライドして実装する。

## コンストラクタ

```python
Scraper(sequence: int)
```

`sequence` はデータセット（ディレクトリ連番）の識別子。抽出結果に紐付けられる。

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `sequence` | `int` | 現在処理中のデータセット番号 |
| `links_assoc` | `dict[str, dict[str, Any]]` | 抽出したリンクの連想配列（URL をキーとする） |
| `info` | `dict[str, Info]` | ファイル名をキーとした処理済み `Info` のキャッシュ |
| `append_count` | `int` | 追加に成功したリンク件数 |
| `no_append_count` | `int` | 追加をスキップしたリンク件数 |

## パブリック API

### `scrape(info: Info) -> None`

**サブクラスで実装する拡張ポイント。** 基底クラスの実装は何もしない。
`info.soup` を解析して `self.links_assoc` へエントリを追加する。

### `get_links_assoc_from_html(file_path: Path) -> Dict[str, Dict[str, Any]]`

HTML ファイルを解析し、抽出結果のリンク連想配列を返す。
同じファイルが `self.info` にキャッシュされている場合は再解析しない。

## クラスメソッド（内部ユーティリティ）

### `_to_assoc(title, url, sequence) -> dict[str, Any]`

タイトル・URL・出現ディレクトリ番号から標準的なリンク辞書を組み立てる。
`sequence_array` は `set` として格納される。

### `_add_assoc(links_assoc, key, sequence, value_dict) -> bool`

`key` が未登録の場合はエントリを追加して `True` を返す。
既登録の場合は `sequence_array` に番号を追加するだけで `False` を返す（重複排除）。

## HTML パーサ

BeautifulSoup に `html5lib` パーサを使用する。`lxml` は使用しない。
エンコーディングは `chardet` で自動推定する。

## 依存関係

- `bs4.BeautifulSoup`
- `yklibpy.common.info.Info`
- `yklibpy.common.loggerx.Loggerx`
- `yklibpy.common.util.Util`
