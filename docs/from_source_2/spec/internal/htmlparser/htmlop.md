# HtmlOp — 内部仕様書

**ファイル**: `src/yklibpy/htmlparser/htmlop.py`  
**継承**: なし

## 概要

BeautifulSoup 互換要素を探索し、アンカー要素を `AnchorTagInfo` に変換またはログ出力するステートレスな補助クラスである。

---

## メソッド

### `get_anchor_under_b(child: Any, cond: Any = None) -> list[list[AnchorTagInfo | None]]` (classmethod)

`child` 配下の `b` 要素ごとにアンカー情報一覧を作る。

処理フロー:

1. 条件の有無に応じて `b` 要素を検索する。
2. 各 `b` 要素を `get_anchor_all` へ渡す。
3. 二次元配列として返す。

### `get_anchor_all(child: Any) -> list[AnchorTagInfo | None]` (classmethod)

配下の全 `a` 要素を `get_anchor_tag_info` で変換して返す。

### `get_anchor_tag_info(anchor_tag: Any) -> AnchorTagInfo | None` (classmethod)

アンカー要素が `None` でなければ `AnchorTagInfo` を生成する。

### `get_anchor_under_div(child: Any, cond: Any = None) -> None` (classmethod)

`div` 要素配下のアンカー情報を取得し、各情報を `print_tag_info` へ渡す。

処理フロー:

1. `div` 要素群を検索する。
2. 各 `div` からアンカー情報を取得する。
3. 各アンカー情報をログ出力処理へ渡す。

### `print_tag_info(assoc: Any) -> None` (classmethod)

辞書形式の `tag` と `mes_array` を取り出し、メッセージ配列を改行で連結してログへ出す。

**Raises**: `KeyError` / `TypeError` — 引数が期待する辞書構造でない場合。

## 依存

| クラス/変数 | 用途 |
|-------------|------|
| `AnchorTagInfo` | アンカー要素の情報表現。 |
| `Loggerx` | 探索結果とタグ情報の出力。 |

## 設計上の注意

`get_anchor_under_div` の条件分岐は、`cond is None` の場合に `find_all("div", cond)`、指定時に条件なし検索を行っており、意図と逆である可能性がある。また `print_tag_info` は `AnchorTagInfo` の公開属性ではなく辞書形式を前提とし、型注釈とも整合していない。
