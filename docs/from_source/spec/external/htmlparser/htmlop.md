# 外部仕様書 — `htmlop`

**対象クラス**: `yklibpy.htmlparser.htmlop.HtmlOp`
**対応サブコマンド**: なし（ライブラリクラス）

本書は `docs/projects/def_ot_terms.md`（用語の定義）および `docs/projects/def_of_file_and_dir.md`（ディレクトリ/ファイル定義）を正とする方針で作成したが、本書作成時点で両ファイルは空である。そのため本書の記述はすべて「現行実装の挙動」に基づく。

## 未確定事項（本書作成にあたっての前提）

- 定義ドキュメント 2 件がいずれも空のため、定義由来の記述は存在せず、全記述を「現行実装の挙動」として扱った。異なる意図であればお知らせください。

## 1. 概要

BeautifulSoup 要素からアンカー（`<a>`）情報を取り出すための補助処理をまとめた、状態を持たない静的ヘルパークラス。すべて classmethod として提供する。

## 2. 公開インタフェース

| メソッド | 説明 |
|---------|------|
| `get_anchor_under_b(child, cond=None) -> list[list[AnchorTagInfo \| None]]` | `b` 要素配下のアンカー情報を `b` タグごとの二重配列で返す。`cond` 指定時は `b` タグの絞り込み条件として使う |
| `get_anchor_all(child) -> list[AnchorTagInfo \| None]` | 要素配下のすべてのアンカーをアンカー情報オブジェクトへ変換する |
| `get_anchor_tag_info(anchor_tag) -> AnchorTagInfo \| None` | 単一のアンカー要素からアンカー情報オブジェクトを作成する。`None` 入力は `None` を返す |
| `get_anchor_under_div(child, cond=None) -> None` | `div` 要素配下のアンカー情報をデバッグログへ出力する（戻り値なし） |
| `print_tag_info(assoc) -> None` | `tag`/`mes_array` キーを持つ辞書の内容をデバッグログへ整形出力する |

## 3. 制約（現行実装の挙動）

- `get_anchor_under_div()` は `cond` の分岐が逆になっており、`cond` を指定しても絞り込みに反映されない。`cond` を使う場合は挙動を要確認。
- `print_tag_info()` は辞書形式（`tag`/`mes_array` キー）を期待するが、他メソッドが返すのはアンカー情報オブジェクトであり、そのまま渡すと `TypeError` になる。呼び出し経路の整合は利用側の責任。

## 4. エラー処理・終了コード

| 事象 | 挙動 |
|------|------|
| `print_tag_info()` に辞書以外を渡した | `TypeError` が呼び出し元へ伝播する |
| `find_all` を持たない要素を渡した | `AttributeError` が呼び出し元へ伝播する |

ライブラリクラスであり単体のコマンドとして起動される経路は無いため、終了コードは規定しない。

## 5. 実装上の対応（参考）

本節は実装を拘束しない。

| 役割 | モジュール |
|------|-----------|
| アンカー抽出ヘルパー | `yklibpy.htmlparser.htmlop.HtmlOp` |
| アンカー情報の変換先 | `yklibpy.htmlparser.misc.anchortaginfo.AnchorTagInfo` |
