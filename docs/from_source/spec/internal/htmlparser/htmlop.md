# HtmlOp — 内部仕様書

**ファイル**: `src/yklibpy/htmlparser/htmlop.py`
**継承**: なし

## 概要

BeautifulSoup 要素からアンカー（`<a>`）情報を取り出すための補助処理をまとめた、状態を持たない静的ヘルパークラス。

---

## メソッド

### `get_anchor_under_b(child: Any, cond: Any = None) -> list[list[AnchorTagInfo | None]]` (classmethod)

`b` 要素配下のアンカー情報を配列で返す。`cond` が指定されていれば `find_all("b", cond)` で絞り込む。各 `b` タグごとに `get_anchor_all()` を適用した二重配列を返す。

### `get_anchor_all(child: Any) -> list[AnchorTagInfo | None]` (classmethod)

要素配下のすべてのアンカーを `AnchorTagInfo` へ変換する。

### `get_anchor_tag_info(anchor_tag: Any) -> AnchorTagInfo | None` (classmethod)

単一のアンカー要素から `AnchorTagInfo` を作成する。`anchor_tag` が `None` の場合は `None` を返す。

### `get_anchor_under_div(child: Any, cond: Any = None) -> None` (classmethod)

`div` 要素配下のアンカー情報をログへ出力する（戻り値なし、デバッグ用）。

### `print_tag_info(assoc: Any) -> None` (classmethod)

アンカー情報辞書（`tag`/`mes_array` キーを持つ辞書想定）の内容をデバッグログへ整形出力する。

---

## 依存

| クラス/変数 | 用途 |
|-------------|------|
| `AnchorTagInfo` | アンカー情報の変換先 |
| `Loggerx` | デバッグログ出力 |

---

## 設計上の注意

- `get_anchor_under_b()` の `cond is None` 分岐と `get_anchor_under_div()` の `cond is None` 分岐は条件と処理の対応が逆になっている（`get_anchor_under_div()` では `cond is None` のとき `find_all("div", cond)` を呼び、`cond` 指定時に `find_all("div")` を呼んでおり、`cond` の効果が反映されない）。呼び出し側で `cond` を使う場合は挙動を要確認。
- `print_tag_info()` は `assoc["tag"]`/`assoc["mes_array"]` という辞書形式を期待するが、他メソッドが返す `AnchorTagInfo` はオブジェクトであり辞書ではない。呼び出し経路が整合していない可能性がある。
