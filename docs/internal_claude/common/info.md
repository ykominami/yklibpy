# Info — 内部仕様書

## モジュール

`yklibpy.common.info`

## インスタンス変数

| 変数名 | 型 | 役割 |
|--------|----|------|
| `file_path` | `Path` | 解析元 HTML ファイルのパス |
| `name` | `str` | ファイル名（`file_path.name` を想定） |
| `soup` | `BeautifulSoup` | 解析済みの DOM オブジェクト |
| `append_count` | `int` | 追加済みリンク数のカウンタ（呼び出し元が管理） |
| `no_append_count` | `int` | 重複スキップ数のカウンタ（呼び出し元が管理） |

## 実装詳細

- `__init__` は引数をそのまま代入するだけのデータクラスに相当する
- メソッド・プロパティは一切持たない純粋なデータ容器
- `append_count` / `no_append_count` は `Scraper` が `Info` を生成する時点では `0` を渡すが、後続処理で書き換えることも許容している

## 依存関係

- `pathlib.Path`
- `bs4.BeautifulSoup`
