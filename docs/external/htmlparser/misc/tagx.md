# Tagx — 外部仕様書

## 概要

`yklibpy.htmlparser.misc.tagx.Tagx`

BeautifulSoup の `PageElement` から表示用情報（テキスト・タグ名・型）を抜き出して保持するラッパー。
`AnchorTagx` の基底クラスとして機能し、スクレイパーのデバッグ出力を統一する。

## コンストラクタ

```python
Tagx(tag: Optional[PageElement], namex: str)
```

`tag` が `None` の場合は最低限のフィールドのみ初期化する。
`namex` はデバッグ用ラベル（`"anchor"` / `"parent"` など）として出力メッセージに埋め込まれる。

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `option` | `str` | 外部で整形した補助文字列（初期値は空文字） |
| `tag` | `PageElement \| None` | 元の BeautifulSoup 要素 |
| `strx` | `str` | `str(tag)` によるタグの文字列表現 |
| `type` | `type` | `type(tag)` による型情報 |
| `mes_type` | `str` | 型情報のデバッグ用表示文字列 |
| `text` | `str` | タグのテキスト内容（`tag` が非 `None` かつ `get_text` を持つ場合） |
| `mes_text` | `str` | テキスト内容のデバッグ用表示文字列 |
| `mes_name` | `str` | タグ名のデバッグ用表示文字列 |

## パブリック API

### `set_option(option: str) -> None`

外部で整形した補助文字列を保持する。価格表示など追加情報の付与に使用する。

### `get_option() -> str`

保持している補助文字列を返す。

## 依存関係

- `bs4.element.PageElement`
