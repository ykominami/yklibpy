# 外部仕様書 — `anchortaginfo`

**対象クラス**: `yklibpy.htmlparser.misc.anchortaginfo.AnchorTagInfo`
**対応サブコマンド**: なし（ライブラリクラス）

本書は `docs/projects/def_ot_terms.md`（用語の定義）および `docs/projects/def_of_file_and_dir.md`（ディレクトリ/ファイル定義）を正とする方針で作成したが、本書作成時点で両ファイルは空である。そのため本書の記述はすべて「現行実装の挙動」に基づく。

## 未確定事項（本書作成にあたっての前提）

- 定義ドキュメント 2 件がいずれも空のため、定義由来の記述は存在せず、全記述を「現行実装の挙動」として扱った。異なる意図であればお知らせください。

## 1. 概要

アンカー要素（`<a>`）本体と、その周辺ノード（親の親・次の兄弟等）の情報をまとめて保持するコンテナ。アンカー抽出処理が取り出したアンカーの周辺コンテキストを扱う際に使う。

## 2. 公開インタフェース

### 生成

```python
AnchorTagInfo(anchor_tag: Optional[PageElement])
```

生成時点では周辺ノード情報（`parent_parent`/`parent`/`next_sibling`）はすべて `None` で、`setup()` を呼ぶことで構築される。

### `setup() -> None`

アンカー要素の周辺ノード情報を構築する。アンカー要素が無い場合はすべて `None` のままにする。

| 属性 | 生成後の内容 |
|------|------------|
| `anchor` | アンカー本体のラッパー |
| `next_sibling` | 次の兄弟ノードのラッパー |
| `parent` | **次の兄弟ノード**のラッパー（属性名は `parent` だが親ノードではない。詳細は §3） |
| `parent_parent` | 親の親ノードのラッパー（親ノードが無い場合は `None`） |

## 3. 制約（現行実装の挙動）

`parent` 属性には親ノードではなく次の兄弟ノードが格納される（`next_sibling` と同じ値）。バグの可能性がある実装のため、`parent` を利用する際は実際の値を確認すること。

## 4. エラー処理・終了コード

例外を送出する経路は無い。ライブラリクラスであり単体のコマンドとして起動される経路は無いため、終了コードは規定しない。

## 5. 実装上の対応（参考）

本節は実装を拘束しない。

| 役割 | モジュール |
|------|-----------|
| アンカー周辺情報コンテナ | `yklibpy.htmlparser.misc.anchortaginfo.AnchorTagInfo` |
| アンカー本体のラッパー | `yklibpy.htmlparser.misc.anchortagx.AnchorTagx` |
| 周辺ノードのラッパー | `yklibpy.htmlparser.misc.tagx.Tagx` |
