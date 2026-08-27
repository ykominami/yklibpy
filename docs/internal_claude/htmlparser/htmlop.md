# HtmlOp — 内部仕様書

## モジュール

`yklibpy.htmlparser.htmlop`

## メソッドの実装詳細

### `get_anchor_under_b(child, cond) -> list[list[AnchorTagInfo | None]]`

- `cond is None` なら `child.find_all("b")`、あれば `child.find_all("b", cond)` で `b` 要素を列挙
- 各 `b` 要素に対して `get_anchor_all` を呼んだ結果のリストを返す（二次元リスト）

### `get_anchor_all(child) -> list[AnchorTagInfo | None]`

- `child.find_all("a")` で配下のアンカーをすべて取得し `get_anchor_tag_info` にマップする

### `get_anchor_tag_info(anchor_tag) -> AnchorTagInfo | None`

- `anchor_tag is None` なら `None` を返す
- `AnchorTagInfo(anchor_tag)` を生成して返す（`setup()` は呼ばない）

### `get_anchor_under_div(child, cond) -> None`

- 戻り値は `None`（ログ出力専用）
- `cond` の有無で `find_all` の引数が逆になっているバグがあり、`cond is None` のときに `find_all("div", cond)` を呼んでいる（本来は `find_all("div")`）

### `print_tag_info(assoc) -> None`

- `assoc["tag"]` と `assoc["mes_array"]` をデバッグログへ出力するユーティリティ

## 依存関係

- `yklibpy.common.loggerx.Loggerx`
- `yklibpy.htmlparser.misc.anchortaginfo.AnchorTagInfo`
