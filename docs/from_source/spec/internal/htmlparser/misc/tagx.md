# Tagx — 内部仕様書

**ファイル**: `src/yklibpy/htmlparser/misc/tagx.py`
**継承**: なし

## 概要

BeautifulSoup 要素（`PageElement`）から表示用情報（テキスト・タグ名・型）を取り出して保持する基底ラッパー。`AnchorTagx` などのより特化したラッパーの親クラスとしても使われる。

---

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `option` | `str` | 外部から設定される補助文字列（既定は空文字）。 |
| `tag` | `Optional[PageElement]` | 保持対象のタグ本体。 |
| `strx` | `str` | `tag` の文字列表現。 |
| `type` | `type` | `tag` の型オブジェクト。 |
| `mes_type` | `str` | デバッグ表示用の型メッセージ。 |
| `text` | `str` | `tag.get_text(strip=True)` の結果（`tag` が `get_text` を持つ場合のみ設定）。 |
| `mes_text` | `str` | デバッグ表示用のテキストメッセージ。 |
| `mes_name` | `str` | デバッグ表示用のタグ名メッセージ。 |

---

## メソッド

### `__init__(tag: Optional[PageElement], namex: str) -> None`

タグ本体とログ出力向けの文字列表現を初期化する。`tag` が `None` でない場合、`mes_text`/`mes_name` を設定する（`text` は `tag` が `get_text` を持つ場合のみ設定される）。

### `set_option(option: str) -> None`

外部で整形した補助文字列を保持する。

### `get_option() -> str`

保持している補助文字列を返す。

---

## 依存

なし（`bs4.element.PageElement` を型としてのみ参照）。

---

## 設計上の注意

`tag` が `None` の場合、`text`/`mes_text`/`mes_name` が未設定のままインスタンスが生成される。これらの属性へ後からアクセスすると `AttributeError` になるため、利用側では `tag is not None` を確認するか、事前に `hasattr` でガードする必要がある。
