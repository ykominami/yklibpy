# HtmlOp — 外部仕様書

## 概要

`yklibpy.htmlparser.htmlop.HtmlOp`

BeautifulSoup 要素からアンカー情報を取り出す補助クラスメソッド集。
スクレイパーの `scrape` 実装内から呼び出す用途を想定する。

## パブリック API

### `get_anchor_under_b(child, cond=None) -> list[list[AnchorTagInfo | None]]`

`child` 要素配下の `<b>` 要素を検索し、各 `<b>` 配下のアンカー情報を配列の配列で返す。
`cond` が指定された場合は `find_all("b", cond)` の条件として渡す。

### `get_anchor_all(child) -> list[AnchorTagInfo | None]`

`child` 要素配下のすべての `<a>` 要素を取得し、それぞれを `AnchorTagInfo` へ変換して返す。

### `get_anchor_tag_info(anchor_tag) -> AnchorTagInfo | None`

単一のアンカー要素から `AnchorTagInfo` を生成して返す。
`anchor_tag` が `None` の場合は `None` を返す。

### `get_anchor_under_div(child, cond=None) -> None`

`child` 要素配下の `<div>` を検索し、各 `<div>` 配下のアンカー情報をデバッグログへ出力する。
戻り値はなく、デバッグ目的のメソッド。

### `print_tag_info(assoc) -> None`

アンカー情報辞書のタグと `mes_array` をデバッグログへ整形出力する。

## 依存関係

- `yklibpy.common.loggerx.Loggerx`
- `yklibpy.htmlparser.misc.anchortaginfo.AnchorTagInfo`
