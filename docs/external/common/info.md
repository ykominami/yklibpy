# Info — 外部仕様書

## 概要

`yklibpy.common.info.Info`

解析済み HTML（`BeautifulSoup` オブジェクト）と処理件数カウンタをひとまとめに保持するデータ容器。
`Scraper` がファイルごとの処理中間状態を引き渡す際に使用する。

## コンストラクタ

```python
Info(
    file_path: Path,
    name: str,
    soup: BeautifulSoup,
    append_count: int,
    no_append_count: int,
)
```

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `file_path` | `Path` | 解析元の HTML ファイルパス |
| `name` | `str` | ファイル識別名（通常はファイル名） |
| `soup` | `BeautifulSoup` | 解析済み DOM ツリー |
| `append_count` | `int` | 追加に成功したリンク件数 |
| `no_append_count` | `int` | 追加をスキップしたリンク件数 |

## 制約

- メソッドを持たないデータホルダーであり、フィールドへの直接アクセスを前提とする。
- インスタンスの生成後にフィールドを書き換えることは制限されていないが、`Scraper` の実装慣例として `append_count` と `no_append_count` は処理の進行に伴い加算される。

## 依存関係

- `bs4.BeautifulSoup`
