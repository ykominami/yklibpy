# AnchorTagx — 内部仕様書

**ファイル**: `src/yklibpy/htmlparser/misc/anchortagx.py`
**継承**: `Tagx`

## 概要

アンカー要素（`<a>`）に特化した `Tagx` の拡張。`href` 属性と表示テキストを抽出して保持する。

---

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `href` | `str` | アンカーの `href` 属性値。取得不可なら空文字。 |
| `text` | `str` | アンカーの表示テキスト（前後空白除去済み）。取得不可なら空文字。 |
| `mes_href` | `str` | デバッグ表示用の `href` メッセージ。 |
| `mes_text` | `str` | デバッグ表示用のテキストメッセージ。 |

---

## メソッド

### `__init__(anchor_tag: Optional[PageElement]) -> None`

`Tagx.__init__(anchor_tag, "anchor")` を呼び出したうえで、`href` と `text` を取り出して保持する。`self.tag` が `None` の場合は `href`/`text` は空文字のまま、`mes_href`/`mes_text` は設定されない。

### `show() -> str`

`href` と表示テキストを改行区切りで返す。

---

## 依存

| クラス/変数 | 用途 |
|-------------|------|
| `Tagx` | 基底クラス。タグ本体・型情報の保持 |

---

## 設計上の注意

`self.tag is None` の場合、`mes_href`/`mes_text` が未設定のままになるため、`show()` を呼び出すと `AttributeError` になる可能性がある（`Tagx.__init__` 側にも同様の未設定パターンがある）。
