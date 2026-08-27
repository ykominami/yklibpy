# Tagx — 内部仕様書

**ファイル**: `src/yklibpy/htmlparser/misc/tagx.py`  
**継承**: なし

## 概要

BeautifulSoup の `PageElement` を保持し、型、タグ名、テキスト等をログ表示しやすい文字列へ変換する汎用ラッパーである。

---

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `option` | `str` | 呼び出し側が設定する補助文字列。 |
| `tag` | `Optional[PageElement]` | 元のタグまたはノード。 |
| `strx` | `str` | 元ノードの文字列表現。 |
| `type` | `type` | 元ノードの実行時型。 |
| `mes_type` | `str` | 型情報の表示用文字列。 |
| `text` | `str` | タグの表示テキスト。対応要素の場合のみ生成。 |
| `mes_text` | `str` | テキストの表示用文字列。タグが存在する場合のみ生成。 |
| `mes_name` | `str` | タグ名の表示用文字列。タグが存在する場合のみ生成。 |

---

## メソッド

### `__init__(tag: Optional[PageElement], namex: str) -> None`

元ノードの基本情報を保持し、対応する属性の有無に応じてテキストとタグ名の表示文字列を作る。

処理フロー:

1. 補助文字列、元ノード、文字列表現、型情報を初期化する。
2. ノードが `get_text` を持てば表示テキストを取得する。
3. ノードが `name` を持てばタグ名を表示用文字列へ変換する。

### `set_option(option: str) -> None`

外部で整形した補助文字列を保持する。

### `get_option() -> str`

保持中の補助文字列を返す。

## 依存

| クラス/変数 | 用途 |
|-------------|------|
| `PageElement` | BeautifulSoup ノードの型表現。 |

## 設計上の注意

`mes_type` は実際の `tag` ではなくラベル文字列 `namex` の型を表示するため、常に文字列型を示す。`tag is None` の場合は `mes_text` と `mes_name` が存在しない。
